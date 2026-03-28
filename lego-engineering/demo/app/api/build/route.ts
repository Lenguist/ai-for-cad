import { NextRequest } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { appendFileSync, mkdirSync, readFileSync } from "fs";
import path from "path";

const PROJECT_ROOT = path.resolve(process.cwd(), "..");
const LOGS_DIR = path.join(PROJECT_ROOT, "agent", "logs");
const BUILDS_LOG = path.join(LOGS_DIR, "builds.jsonl");

// If MODAL_TOOL_URL is set, use Modal (Vercel-compatible).
// Otherwise fall back to spawning python3 locally (dev / Railway).
const MODAL_TOOL_URL = process.env.MODAL_TOOL_URL;

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

// ── Tool execution ─────────────────────────────────────────────────────────────

type ToolResponse = {
  result: unknown;
  assembly: { bricks: unknown[] };
  ldr_content: string | null;
  sim_result: unknown | null;
};

async function runModalTool(
  fn: string,
  args: Record<string, unknown>,
  assembly: { bricks: unknown[] },
): Promise<ToolResponse> {
  const res = await fetch(MODAL_TOOL_URL!, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fn, args, assembly }),
  });
  if (!res.ok) throw new Error(`Modal tool error: ${res.status} ${await res.text()}`);
  return res.json();
}

async function runLocalTool(
  fn: string,
  args: Record<string, unknown>,
): Promise<unknown> {
  const { spawn } = await import("child_process");
  const TOOL_RUNNER = path.join(PROJECT_ROOT, "agent", "tool_runner.py");
  return new Promise((resolve, reject) => {
    const command = JSON.stringify({ fn, args });
    const proc = spawn("python3", [TOOL_RUNNER], { cwd: PROJECT_ROOT });
    let stdout = "";
    let stderr = "";
    proc.stdin.write(command);
    proc.stdin.end();
    proc.stdout.on("data", (d: Buffer) => { stdout += d.toString(); });
    proc.stderr.on("data", (d: Buffer) => { stderr += d.toString(); });
    proc.on("close", (code: number) => {
      if (code !== 0 && !stdout) {
        reject(new Error(stderr || `Tool runner exited ${code}`));
        return;
      }
      try {
        resolve(JSON.parse(stdout.trim()));
      } catch {
        reject(new Error(`Tool output parse error: ${stdout}`));
      }
    });
  });
}

// ── Logging ────────────────────────────────────────────────────────────────────

function writeBuildLog(entry: object) {
  try {
    mkdirSync(LOGS_DIR, { recursive: true });
    appendFileSync(BUILDS_LOG, JSON.stringify(entry) + "\n", "utf8");
  } catch { /* best-effort */ }
}

// ── Tool definitions for Claude ───────────────────────────────────────────────

const TOOLS: Anthropic.Tool[] = [
  {
    name: "search_parts",
    description: "Search available parts by name, type, or keyword. Returns matching parts with specs.",
    input_schema: {
      type: "object" as const,
      properties: {
        query: { type: "string", description: "Search query, e.g. '2x4 brick', 'plate', '1x'" },
      },
      required: ["query"],
    },
  },
  {
    name: "place",
    description: "Add one or more bricks to the current assembly. Returns ok or errors.",
    input_schema: {
      type: "object" as const,
      properties: {
        spec: {
          description: "Single brick dict or array of brick dicts. Each brick: {id, type, pos:[x,y,layer], rot:0|90|180|270, color:int}",
          oneOf: [
            {
              type: "object",
              properties: {
                id: { type: "string" },
                type: { type: "string", description: "Brick type from parts DB, e.g. '2x4', 'plate-1x2'" },
                pos: { type: "array", items: { type: "integer" }, minItems: 3, maxItems: 3, description: "[stud_x, stud_y, layer]" },
                rot: { type: "integer", enum: [0, 90, 180, 270], description: "Rotation in degrees" },
                color: { type: "integer", description: "LDraw color: 4=red, 1=blue, 2=green, 14=yellow, 15=white, 0=black" },
              },
              required: ["id", "type", "pos"],
            },
            { type: "array", items: { type: "object" } },
          ],
        },
      },
      required: ["spec"],
    },
  },
  {
    name: "remove",
    description: "Remove a brick from the assembly by its id.",
    input_schema: {
      type: "object" as const,
      properties: {
        brick_id: { type: "string", description: "The 'id' of the brick to remove" },
      },
      required: ["brick_id"],
    },
  },
  {
    name: "clear",
    description: "Clear the entire assembly and start fresh.",
    input_schema: { type: "object" as const, properties: {} },
  },
  {
    name: "inspect",
    description: "Return the current assembly state: brick list, error list, brick count.",
    input_schema: { type: "object" as const, properties: {} },
  },
  {
    name: "simulate",
    description: "Validate the assembly. Level 1=semantic only, 2=semantic+physical overlap+support check.",
    input_schema: {
      type: "object" as const,
      properties: {
        level: { type: "integer", enum: [1, 2], description: "Validation level (default 2)" },
      },
    },
  },
  {
    name: "save",
    description: "Compile and save the assembly as an LDraw file. The website viewer auto-updates. Always call this last.",
    input_schema: { type: "object" as const, properties: {} },
  },
];

function buildSystemPrompt(selectedParts: string[]): string {
  const partsStr = selectedParts.length > 0
    ? selectedParts.map((p) => `  - ${p}`).join("\n")
    : "  (all standard bricks available)";

  return `You are MechE-Claude, an AI LEGO assembly agent. You build LEGO assemblies from natural language prompts using tool calls.

## Available parts (user selected):
${partsStr}

## Coordinate system:
- pos = [stud_x, stud_y, layer]. Layer 0 = ground. Layer increases upward.
- pos is ALWAYS the minimum-stud corner (min stud_x, min stud_y) regardless of rotation.
- Each stud = 1 unit. Bricks connect when studs align.
- rot = 0/90/180/270 (rotation around vertical axis)
- rot=0: brick spans [pos_x .. pos_x+width-1] in X and [pos_y .. pos_y+depth-1] in Y
- rot=90/270: axes swap — brick spans [pos_x .. pos_x+depth-1] in X and [pos_y .. pos_y+width-1] in Y
- rot=180: same footprint as rot=0 (just flipped)
- Example: 2x4 brick at pos=[0,0], rot=90 spans stud_x 0..3 and stud_y 0..1

## Standard brick sizes (width_studs × depth_studs):
- 1x1, 1x2, 1x3, 1x4, 1x6, 1x8
- 2x2, 2x3, 2x4, 2x6, 2x8
- plates: plate-1x1, plate-1x2, plate-1x4, plate-2x2, plate-2x4, etc.

## LDraw colors: 0=black, 1=blue, 2=green, 4=red, 7=lightgray, 14=yellow, 15=white, 25=orange, 72=darkgray

## Workflow:
1. Search parts if needed
2. Plan the structure (think step by step)
3. Place bricks in batches (can place many at once)
4. Run simulate(2) to check for errors — fix any before proceeding
5. Save when done

## Rules:
- Every brick needs a unique id string (e.g. "base_1", "step_2")
- Fix all validation errors before saving
- Think about support: non-ground bricks need at least one stud below them
- For a staircase: each step is offset in both X/Y and Z
- Always save() at the end so the user sees the result`;
}

// ── POST handler ───────────────────────────────────────────────────────────────

export async function POST(req: NextRequest) {
  const { prompt, selectedParts } = await req.json();
  if (!prompt) return new Response("Missing prompt", { status: 400 });

  const useModal = !!MODAL_TOOL_URL;
  const buildId = `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
  const tsStart = Date.now();

  // In-memory assembly state (valid for the lifetime of this request)
  let assembly: { bricks: unknown[] } = { bricks: [] };

  // For local mode: clear the shared workspace file
  if (!useModal) {
    await runLocalTool("clear", {});
  }

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      const events: object[] = [];

      const send = (event: object) => {
        events.push(event);
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(event)}\n\n`));
      };

      const messages: Anthropic.MessageParam[] = [{ role: "user", content: prompt }];
      let succeeded = false;

      try {
        send({ type: "start", text: `Building: "${prompt}"` });

        let iterations = 0;
        const MAX_ITERATIONS = 20;

        while (iterations < MAX_ITERATIONS) {
          iterations++;

          const response = await client.messages.create({
            model: "claude-sonnet-4-6",
            max_tokens: 4096,
            system: buildSystemPrompt(selectedParts || []),
            tools: TOOLS,
            messages,
          });

          for (const block of response.content) {
            if (block.type === "text" && block.text) {
              send({ type: "text", text: block.text });
            }
          }

          const toolUseBlocks = response.content.filter((b) => b.type === "tool_use");
          if (toolUseBlocks.length === 0 || response.stop_reason === "end_turn") {
            succeeded = true;
            send({ type: "done", text: "Build complete." });
            break;
          }

          const toolResults: Anthropic.ToolResultBlockParam[] = [];

          for (const block of toolUseBlocks) {
            if (block.type !== "tool_use") continue;

            send({ type: "tool_call", name: block.name, input: block.input });

            let toolResult: unknown;
            try {
              if (useModal) {
                const modalResp = await runModalTool(
                  block.name,
                  block.input as Record<string, unknown>,
                  assembly,
                );
                assembly = modalResp.assembly;
                toolResult = modalResp.result;

                // If save() returned LDR content, stream it to the client
                if (block.name === "save" && modalResp.ldr_content) {
                  send({ type: "ldr", content: modalResp.ldr_content });
                }
                if (modalResp.sim_result) {
                  send({ type: "sim", result: modalResp.sim_result });
                }
              } else {
                toolResult = await runLocalTool(
                  block.name,
                  block.input as Record<string, unknown>,
                );
              }
            } catch (err) {
              toolResult = { error: String(err) };
            }

            send({ type: "tool_result", name: block.name, result: toolResult });

            toolResults.push({
              type: "tool_result",
              tool_use_id: block.id,
              content: JSON.stringify(toolResult),
            });
          }

          messages.push({ role: "assistant", content: response.content });
          messages.push({ role: "user", content: toolResults });

          if (response.stop_reason === "end_turn") {
            succeeded = true;
            send({ type: "done", text: "Build complete." });
            break;
          }
        }

        if (iterations >= MAX_ITERATIONS) {
          send({ type: "error", text: "Max iterations reached." });
        }
      } catch (err) {
        send({ type: "error", text: String(err) });
      } finally {
        controller.close();

        // Read final assembly for log (local mode only; Modal mode has it in-memory)
        let finalAssembly: unknown = useModal ? assembly : null;
        if (!useModal) {
          try {
            const ASSEMBLY_JSON = path.join(PROJECT_ROOT, "agent", "workspace", "assembly.json");
            finalAssembly = JSON.parse(readFileSync(ASSEMBLY_JSON, "utf8"));
          } catch { /* ok */ }
        }

        writeBuildLog({
          id: buildId,
          ts: tsStart,
          duration_ms: Date.now() - tsStart,
          mode: useModal ? "modal" : "local",
          prompt,
          selected_parts: selectedParts || [],
          succeeded,
          final_assembly: finalAssembly,
          llm_trace: { system: buildSystemPrompt(selectedParts || []), messages },
          events,
        });
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
