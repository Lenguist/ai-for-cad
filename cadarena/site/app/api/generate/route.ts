import Anthropic from "@anthropic-ai/sdk";
import OpenAI from "openai";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { Redis } from "@upstash/redis";

export const runtime = "nodejs";
export const maxDuration = 120;

const SYSTEM_PROMPT = `You are an expert CAD engineer specializing in CadQuery, a Python library for parametric 3D solid modeling.

Your task: generate CadQuery Python code that models the part described by the user.

STRICT REQUIREMENTS:
1. Start with: import cadquery as cq
2. Assign the final shape to a variable named exactly: result
3. \`result\` must be a cadquery.Workplane object
4. Use ONLY cadquery and the Python standard library — no numpy, scipy, or other dependencies
5. Output ONLY the raw Python code — no explanations, no markdown, no code fences

CADQUERY BASICS (use these patterns):
- Box:        result = cq.Workplane("XY").box(length, width, height)
- Cylinder:   result = cq.Workplane("XY").cylinder(height, radius)
- Sphere:     result = cq.Workplane("XY").sphere(radius)
- Hole:       .faces(">Z").workplane().hole(diameter)
- Shell:      .shell(-thickness)
- Union:      a.union(b)
- Cut:        a.cut(b)
- Fillet:     .edges("|Z").fillet(radius)
- Chamfer:    .edges("|Z").chamfer(length)
- Polar holes: .workplane().polarArray(radius, 0, 360, count).hole(diameter)
- Rect array: .workplane().rarray(xSpacing, ySpacing, xCount, yCount).hole(diameter)`;

function extractCode(text: string): string {
  const fenced = text.match(/```(?:python)?\s*\n([\s\S]*?)```/);
  if (fenced) return fenced[1].trim();
  return text.trim();
}

async function generateClaude(prompt: string): Promise<{ code: string; outputType: string }> {
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  const resp = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 4096,
    system: SYSTEM_PROMPT,
    messages: [{ role: "user", content: prompt }],
  });
  const raw = resp.content[0].type === "text" ? resp.content[0].text : "";
  return { code: extractCode(raw), outputType: "cadquery" };
}

async function generateGPT(prompt: string): Promise<{ code: string; outputType: string }> {
  const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  const resp = await client.chat.completions.create({
    model: "gpt-5",
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      { role: "user", content: prompt },
    ],
    max_completion_tokens: 4096,
  });
  const raw = resp.choices[0].message.content ?? "";
  return { code: extractCode(raw), outputType: "cadquery" };
}

async function generateGemini(prompt: string): Promise<{ code: string; outputType: string }> {
  const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);
  const model = genAI.getGenerativeModel({
    model: "gemini-2.5-flash",
    systemInstruction: SYSTEM_PROMPT,
  });
  const resp = await model.generateContent(prompt);
  const raw = resp.response.text();
  return { code: extractCode(raw), outputType: "cadquery" };
}

async function generateZoo(prompt: string): Promise<{ code: string; outputType: string; stlBase64?: string }> {
  const token = process.env.ZOO_API_TOKEN;
  const headers = {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };

  const createResp = await fetch("https://api.zoo.dev/ai/text-to-cad/stl", {
    method: "POST",
    headers,
    body: JSON.stringify({ prompt }),
  });
  if (!createResp.ok) throw new Error(`Zoo API error: ${createResp.status}`);
  const job = await createResp.json() as { id: string };
  const jobId = job.id;

  // Poll up to 50s
  for (let i = 0; i < 17; i++) {
    await new Promise((r) => setTimeout(r, 3000));
    const statusResp = await fetch(`https://api.zoo.dev/user/text-to-cad/${jobId}`, { headers });
    if (!statusResp.ok) throw new Error(`Zoo poll error: ${statusResp.status}`);
    const data = await statusResp.json() as {
      status: string;
      code?: string;
      outputs?: Record<string, string>;
      error?: string;
    };

    if (data.status === "completed") {
      const outputs = data.outputs ?? {};
      const stlKey = Object.keys(outputs).find((k) => k.endsWith(".stl"));
      let stlBase64: string | undefined;
      if (stlKey) {
        // Zoo returns URL-safe base64 — normalize it
        const raw = outputs[stlKey].replace(/-/g, "+").replace(/_/g, "/");
        const padded = raw + "=".repeat((4 - (raw.length % 4)) % 4);
        stlBase64 = padded;
      }
      return { code: data.code ?? "", outputType: "kcl", stlBase64 };
    }
    if (data.status === "failed" || data.status === "cancelled") {
      throw new Error(`Zoo job ${data.status}: ${data.error ?? "unknown"}`);
    }
  }
  throw new Error("Zoo: timeout after 51s");
}

// ── CadQuery execution via Modal ──────────────────────────────────────────────

async function executeCadQuery(code: string): Promise<string | undefined> {
  const url = process.env.MODAL_EXECUTOR_URL;
  if (!url) return undefined; // graceful degradation — show code only
  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
      signal: AbortSignal.timeout(55_000), // stay under Vercel's 60s limit
    });
    if (!resp.ok) return undefined;
    const data = await resp.json() as { stlBase64?: string; error?: string };
    return data.stlBase64 ?? undefined;
  } catch {
    return undefined;
  }
}

type ModelResult = {
  modelId: string;
  code?: string;
  outputType?: string;
  stlBase64?: string;
  latency: number;
  error?: string;
};

function logPrompt(prompt: string, models: string[]) {
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url || !token) return;
  const redis = new Redis({ url, token });
  redis.rpush("cad-arena:prompts", JSON.stringify({
    prompt,
    models,
    ts: new Date().toISOString(),
  })).catch(() => {});
}

export async function POST(req: Request) {
  const { prompt, models } = await req.json() as { prompt: string; models: string[] };

  if (!prompt?.trim()) {
    return Response.json({ error: "prompt required" }, { status: 400 });
  }

  logPrompt(prompt, models);

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      const send = (data: ModelResult) => {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`));
      };

      await Promise.all(
        models.map(async (modelId: string) => {
          const t0 = Date.now();
          try {
            let result: { code: string; outputType: string; stlBase64?: string };
            switch (modelId) {
              case "claude-opus-4-6":
      case "claude-sonnet-4-6":  result = await generateClaude(prompt); break;
              case "gpt-5":             result = await generateGPT(prompt); break;
              case "gemini-2.5-flash":  result = await generateGemini(prompt); break;
              case "zoo-ml-ephant":     result = await generateZoo(prompt); break;
              default: throw new Error(`Unknown model: ${modelId}`);
            }
            // For LLM models (CadQuery output): execute via Modal to get STL
            if (result.outputType === "cadquery" && result.code && !result.stlBase64) {
              result.stlBase64 = await executeCadQuery(result.code);
            }
            send({ modelId, ...result, latency: (Date.now() - t0) / 1000 });
          } catch (e) {
            send({ modelId, error: String(e), latency: (Date.now() - t0) / 1000 });
          }
        })
      );

      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      "X-Accel-Buffering": "no",
    },
  });
}
