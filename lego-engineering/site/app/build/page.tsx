"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import dynamic from "next/dynamic";
import Nav from "../components/Nav";

// ─── Drag-to-resize divider ───────────────────────────────────────────────────

function HDivider({ onDrag }: { onDrag: (dx: number) => void }) {
  const onMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    let lastX = e.clientX;
    const move = (ev: MouseEvent) => { onDrag(ev.clientX - lastX); lastX = ev.clientX; };
    const up = () => { window.removeEventListener("mousemove", move); window.removeEventListener("mouseup", up); };
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);
  };
  return (
    <div
      onMouseDown={onMouseDown}
      style={{
        width: 5, cursor: "col-resize", flexShrink: 0,
        background: "var(--border)", transition: "background 0.15s",
        zIndex: 10,
      }}
      onMouseEnter={(e) => (e.currentTarget.style.background = "var(--accent)")}
      onMouseLeave={(e) => (e.currentTarget.style.background = "var(--border)")}
    />
  );
}

function VDivider({ onDrag }: { onDrag: (dy: number) => void }) {
  const onMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    let lastY = e.clientY;
    const move = (ev: MouseEvent) => { onDrag(ev.clientY - lastY); lastY = ev.clientY; };
    const up = () => { window.removeEventListener("mousemove", move); window.removeEventListener("mouseup", up); };
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);
  };
  return (
    <div
      onMouseDown={onMouseDown}
      style={{
        height: 5, cursor: "row-resize", flexShrink: 0,
        background: "var(--border)", transition: "background 0.15s",
        zIndex: 10,
      }}
      onMouseEnter={(e) => (e.currentTarget.style.background = "var(--accent)")}
      onMouseLeave={(e) => (e.currentTarget.style.background = "var(--border)")}
    />
  );
}

const AssemblyViewer = dynamic(() => import("../components/AssemblyViewer"), { ssr: false });

// ─── Types ────────────────────────────────────────────────────────────────────

type Part = { id: string; name: string; category: string; description?: string; [key: string]: unknown };

type TraceEvent =
  | { type: "start"; text: string }
  | { type: "text"; text: string }
  | { type: "tool_call"; name: string; input: unknown }
  | { type: "tool_result"; name: string; result: unknown }
  | { type: "done"; text: string }
  | { type: "error"; text: string };
// ldr / sim events are intercepted in the SSE loop and never added to events[]

type SimResult = { ok: boolean; brick_count: number; error_count: number; summary: string };

// ─── Parts panel ─────────────────────────────────────────────────────────────

function PartsPanel({
  selected,
  onToggle,
  onSelectAll,
  onClearAll,
}: {
  selected: Set<string>;
  onToggle: (id: string) => void;
  onSelectAll: () => void;
  onClearAll: () => void;
}) {
  const [parts, setParts] = useState<Part[]>([]);
  const [q, setQ] = useState("");

  useEffect(() => {
    fetch(`/api/parts?q=${encodeURIComponent(q)}&category=all`)
      .then((r) => r.json())
      .then((d) => setParts(d.parts));
  }, [q]);

  // Also load bricks.json
  const [bricks, setBricks] = useState<{ id: string; description: string }[]>([]);
  useEffect(() => {
    fetch("/data/bricks.json")
      .catch(() => null)
      .then(async (r) => {
        if (!r) return;
        const data = await r.json();
        setBricks(Object.entries(data).map(([id, def]: [string, any]) => ({
          id,
          description: def.description,
        })));
      });
  }, []);

  const allItems: Part[] = [
    ...bricks.map((b) => ({ id: b.id, name: b.description, category: "brick" })),
    ...parts,
  ].filter(
    (item) =>
      !q || item.id.toLowerCase().includes(q.toLowerCase()) || item.name?.toLowerCase().includes(q.toLowerCase())
  );

  const allIds = allItems.map((p) => p.id);
  const allSelected = allIds.length > 0 && allIds.every((id) => selected.has(id));

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", overflow: "hidden" }}>
      <div style={{ padding: "8px 12px", borderBottom: "1px solid var(--border)", display: "flex", gap: 6 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="search parts..."
          style={{
            flex: 1, padding: "5px 8px", background: "var(--panel-dark)",
            border: "1px solid var(--border-light)", borderRadius: 3,
            color: "var(--fg)", fontSize: 11, fontFamily: "monospace",
          }}
        />
      </div>
      <div style={{ padding: "6px 12px", borderBottom: "1px solid var(--border)", display: "flex", gap: 6, alignItems: "center" }}>
        <button
          onClick={allSelected ? onClearAll : onSelectAll}
          style={{
            padding: "3px 8px", fontSize: 10, borderRadius: 3, cursor: "pointer",
            border: "1px solid var(--border-light)",
            background: allSelected ? "var(--accent)" : "var(--border)",
            color: allSelected ? "#fff" : "var(--muted-light)",
            fontFamily: "monospace",
          }}
        >
          {allSelected ? "deselect all" : "select all"}
        </button>
        <span style={{ fontSize: 10, color: "var(--muted)", fontFamily: "monospace" }}>
          {selected.size}/{allItems.length}
        </span>
      </div>
      <div style={{ flex: 1, overflowY: "auto" }}>
        {allItems.map((p) => (
          <label
            key={p.id}
            style={{
              display: "flex", alignItems: "center", gap: 8,
              padding: "5px 12px", cursor: "pointer", borderBottom: "1px solid #0a1e38",
              background: selected.has(p.id) ? "rgba(126,184,232,0.08)" : "transparent",
            }}
          >
            <input
              type="checkbox"
              checked={selected.has(p.id)}
              onChange={() => onToggle(p.id)}
              style={{ accentColor: "var(--blue)" }}
            />
            <div>
              <div style={{ fontFamily: "monospace", fontSize: 11, color: "var(--blue)" }}>{p.id}</div>
              <div style={{ fontSize: 10, color: "var(--muted)" }}>{p.name || (p.description as string)}</div>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
}

// ─── Terminal panel ───────────────────────────────────────────────────────────

function Terminal({ events }: { events: TraceEvent[] }) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [events]);

  if (events.length === 0) {
    return (
      <div style={{
        flex: 1, display: "flex", alignItems: "center", justifyContent: "center",
        color: "var(--muted)", fontFamily: "monospace", fontSize: 12,
      }}>
        ← select parts, enter a prompt, click Build
      </div>
    );
  }

  return (
    <div style={{ flex: 1, overflowY: "auto", padding: "12px 16px", fontFamily: "monospace", fontSize: 12 }}>
      {events.map((ev, i) => {
        if (ev.type === "start") return (
          <div key={i} style={{ color: "var(--muted)", marginBottom: 8 }}>
            ▸ {ev.text}
          </div>
        );
        if (ev.type === "text") return (
          <div key={i} style={{ color: "var(--fg)", marginBottom: 4, lineHeight: 1.6, whiteSpace: "pre-wrap" }}>
            {ev.text}
          </div>
        );
        if (ev.type === "tool_call") {
          const inp = ev.input as any;
          if (ev.name === "place") {
            const bricks: any[] = Array.isArray(inp.spec) ? inp.spec : [inp.spec];
            const COLOR_NAMES: Record<number, string> = { 0: "black", 1: "blue", 2: "green", 4: "red", 7: "lgray", 14: "yellow", 15: "white", 25: "orange", 72: "dgray" };
            return (
              <div key={i} style={{ marginBottom: 6 }}>
                <span style={{ color: "#4caf50" }}>⚙ place</span>
                <span style={{ color: "var(--muted)", marginLeft: 6, fontSize: 10 }}>{bricks.length} brick{bricks.length !== 1 ? "s" : ""}</span>
                <div style={{ marginTop: 4, display: "flex", flexDirection: "column", gap: 2 }}>
                  {bricks.map((b: any, bi: number) => (
                    <div key={bi} style={{ display: "flex", gap: 12, padding: "2px 8px", background: "rgba(255,255,255,0.03)", borderRadius: 2, fontSize: 11 }}>
                      <span style={{ color: "var(--blue)", minWidth: 80 }}>{b.id}</span>
                      <span style={{ color: "#e0e0e0", minWidth: 60 }}>{b.type}</span>
                      <span style={{ color: "var(--muted)" }}>pos [{b.pos?.join(", ")}]</span>
                      {b.rot ? <span style={{ color: "var(--muted)" }}>rot {b.rot}°</span> : null}
                      <span style={{ color: "var(--muted)" }}>{COLOR_NAMES[b.color] ?? `color ${b.color}`}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          }
          return (
            <div key={i} style={{ marginBottom: 4 }}>
              <span style={{ color: "#4caf50" }}>⚙ {ev.name}</span>
              <span style={{ color: "var(--muted)", marginLeft: 8, fontSize: 11 }}>
                {Object.keys(inp).length > 0 ? JSON.stringify(inp) : ""}
              </span>
            </div>
          );
        }
        if (ev.type === "tool_result") {
          const result = ev.result as any;
          const isOk = result?.ok !== false && !result?.error;
          return (
            <div key={i} style={{
              marginBottom: 8, padding: "4px 8px", borderRadius: 3,
              background: isOk ? "rgba(76,175,80,0.08)" : "rgba(233,69,96,0.08)",
              borderLeft: `2px solid ${isOk ? "#4caf50" : "#e94560"}`,
            }}>
              {result?.error && <span style={{ color: "#e94560" }}>✗ {result.error}</span>}
              {result?.summary && <span style={{ color: isOk ? "#4caf50" : "#e94560" }}>{result.summary}</span>}
              {result?.placed && <span style={{ color: "#4caf50" }}>✓ placed {result.placed.join(", ")}</span>}
              {result?.brick_count !== undefined && !result?.summary && (
                <span style={{ color: "var(--muted)" }}>{result.brick_count} bricks</span>
              )}
              {result?.results && (
                <span style={{ color: "var(--muted)" }}>
                  {(result.results as any[]).map((p: any) => p.id).join(", ")}
                </span>
              )}
            </div>
          );
        }
        if (ev.type === "done") return (
          <div key={i} style={{ color: "#4caf50", marginTop: 8, fontWeight: 700 }}>
            ✓ {ev.text}
          </div>
        );
        if (ev.type === "error") return (
          <div key={i} style={{ color: "#e94560", marginTop: 8 }}>
            ✗ {ev.text}
          </div>
        );
        return null;
      })}
      <div ref={bottomRef} />
    </div>
  );
}

// ─── Main page ────────────────────────────────────────────────────────────────

export default function BuildPage() {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [allPartIds, setAllPartIds] = useState<string[]>([]);
  const [prompt, setPrompt] = useState("");
  const [events, setEvents] = useState<TraceEvent[]>([]);
  const [building, setBuilding] = useState(false);
  const [version, setVersion] = useState(0);
  const [sim, setSim] = useState<SimResult | null>(null);
  const [ldrExists, setLdrExists] = useState(false);
  const prevSimRef = useRef("");
  // Blob URL for LDR content received via SSE (Modal/Vercel path)
  const [ldrBlobUrl, setLdrBlobUrl] = useState<string | null>(null);
  const ldrBlobRef = useRef<string | null>(null);

  // Panel sizes
  const [col1W, setCol1W] = useState(220);
  const [col3W, setCol3W] = useState(380);
  const [jsonH, setJsonH] = useState(180);
  const col1WRef = useRef(220);
  const col3WRef = useRef(380);
  const jsonHRef = useRef(180);

  // Load all part IDs for "select all"
  useEffect(() => {
    Promise.all([
      fetch("/api/parts?category=all").then((r) => r.json()),
      fetch("/data/bricks.json").catch(() => ({ ok: false })).then(async (r: any) => {
        if (!r.ok) return {};
        return r.json();
      }),
    ]).then(([technic, bricks]) => {
      const ids = [
        ...Object.keys(bricks || {}),
        ...(technic.parts || []).map((p: Part) => p.id),
      ];
      setAllPartIds(ids);
    });
  }, []);

  const togglePart = (id: string) =>
    setSelected((s) => { const n = new Set(s); n.has(id) ? n.delete(id) : n.add(id); return n; });

  const selectAll = () => setSelected(new Set(allPartIds));
  const clearAll = () => setSelected(new Set());

  // Poll ready.json (written by save() AFTER the LDR is flushed) to trigger viewer refresh
  useEffect(() => {
    const poll = async () => {
      try {
        // ready.json is written by save() only after assembly.ldr is written
        const r = await fetch(`/workspace/ready.json?t=${Date.now()}`);
        if (!r.ok) return;
        const ready = await r.json();
        const key = String(ready.ts);
        if (key !== prevSimRef.current) {
          prevSimRef.current = key;
          setVersion((v) => v + 1);
          setLdrExists(true);
          // Also fetch sim_result for display
          const sr = await fetch(`/workspace/sim_result.json?t=${Date.now()}`);
          if (sr.ok) setSim(await sr.json());
        }
      } catch { /* no file yet */ }
    };
    poll();
    const id = setInterval(poll, 1000);
    return () => clearInterval(id);
  }, []);

  // Run build
  const handleBuild = useCallback(async () => {
    if (!prompt.trim() || building) return;
    setBuilding(true);
    setEvents([]);

    try {
      const res = await fetch("/api/build", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: prompt.trim(),
          selectedParts: selected.size > 0 ? [...selected] : [],
        }),
      });

      if (!res.body) throw new Error("No response body");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop() ?? "";
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const ev = JSON.parse(line.slice(6));
              // Intercept ldr/sim — update viewer state directly, don't add to trace
              if (ev.type === "ldr" && ev.content) {
                const blob = new Blob([ev.content], { type: "text/plain" });
                const url = URL.createObjectURL(blob);
                if (ldrBlobRef.current) URL.revokeObjectURL(ldrBlobRef.current);
                ldrBlobRef.current = url;
                setLdrBlobUrl(url);
                setLdrExists(true);
                setVersion((v) => v + 1);
              } else if (ev.type === "sim" && ev.result) {
                setSim(ev.result as SimResult);
              } else {
                setEvents((prev) => [...prev, ev]);
              }
            } catch { /* skip malformed */ }
          }
        }
      }
    } catch (err) {
      setEvents((prev) => [...prev, { type: "error", text: String(err) }]);
    } finally {
      setBuilding(false);
    }
  }, [prompt, selected, building]);

  return (
    <div style={{ background: "var(--bg)", height: "100vh", display: "flex", flexDirection: "column", overflow: "hidden" }}>
      <Nav />
      <div style={{ display: "flex", flex: 1, overflow: "hidden", minHeight: 0 }}>

        {/* ── Col 1: Parts selector ─────────────────────────────── */}
        <div style={{
          width: col1W, background: "var(--panel)",
          display: "flex", flexDirection: "column", flexShrink: 0, minWidth: 120,
        }}>
          <div style={{ padding: "8px 12px", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ fontSize: 11, color: "var(--muted)", fontFamily: "monospace" }}>parts</span>
          </div>
          <PartsPanel
            selected={selected}
            onToggle={togglePart}
            onSelectAll={selectAll}
            onClearAll={clearAll}
          />
        </div>

        <HDivider onDrag={(dx) => {
          col1WRef.current = Math.max(120, Math.min(500, col1WRef.current + dx));
          setCol1W(col1WRef.current);
        }} />

        {/* ── Col 2: Prompt + Terminal ──────────────────────────── */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0, minHeight: 0 }}>

          {/* Prompt bar */}
          <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--border)", display: "flex", gap: 8 }}>
            <input
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleBuild()}
              placeholder='e.g. "build a 3-step staircase" or "make a simple house"'
              disabled={building}
              style={{
                flex: 1, padding: "7px 10px", background: "var(--panel-dark)",
                border: "1px solid var(--border-light)", borderRadius: 4,
                color: "var(--fg)", fontSize: 13, fontFamily: "monospace",
                opacity: building ? 0.6 : 1,
              }}
            />
            <button
              onClick={handleBuild}
              disabled={building || !prompt.trim()}
              style={{
                padding: "7px 18px", background: building ? "var(--border)" : "var(--accent)",
                border: "none", borderRadius: 4, color: "#fff", fontSize: 13,
                fontWeight: 700, cursor: building ? "wait" : "pointer",
                opacity: building || !prompt.trim() ? 0.6 : 1,
                whiteSpace: "nowrap",
              }}
            >
              {building ? "building..." : "Build →"}
            </button>
          </div>

          {/* Terminal trace */}
          <div style={{ flex: 1, overflowY: "hidden", display: "flex", flexDirection: "column", minHeight: 0 }}>
            <div style={{ padding: "6px 14px", borderBottom: "1px solid var(--border)", fontSize: 10, color: "var(--muted)", fontFamily: "monospace", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              agent trace
              {building && <span style={{ marginLeft: 8, color: "#4caf50", animation: "pulse 1s infinite" }}>● live</span>}
            </div>
            <Terminal events={events} />
          </div>
        </div>

        <HDivider onDrag={(dx) => {
          col3WRef.current = Math.max(200, Math.min(800, col3WRef.current - dx));
          setCol3W(col3WRef.current);
        }} />

        {/* ── Col 3: 3D viewer + status ─────────────────────────── */}
        <div style={{
          width: col3W,
          display: "flex", flexDirection: "column", flexShrink: 0, minWidth: 200,
        }}>
          {/* 3D Viewer */}
          <div style={{ flex: 1, position: "relative", minHeight: 0 }}>
            {ldrExists ? (
              <AssemblyViewer
                ldrUrl={ldrBlobUrl ?? "/workspace/assembly.ldr"}
                version={version}
              />
            ) : (
              <div style={{
                width: "100%", height: "100%", display: "flex", alignItems: "center",
                justifyContent: "center", flexDirection: "column", gap: 8,
                color: "var(--muted)", fontFamily: "monospace", fontSize: 12,
              }}>
                <div>no assembly yet</div>
              </div>
            )}
            <div style={{
              position: "absolute", bottom: 8, left: 10, right: 10,
              fontSize: 10, color: "rgba(255,255,255,0.25)", fontFamily: "monospace",
              display: "flex", justifyContent: "space-between",
            }}>
              <span>drag · scroll</span>
              {sim && (
                <span style={{ color: sim.ok ? "#4caf50" : "#e94560" }}>
                  {sim.brick_count} bricks · {sim.ok ? "valid" : `${sim.error_count} err`}
                </span>
              )}
            </div>
          </div>

          <VDivider onDrag={(dy) => {
            jsonHRef.current = Math.max(60, Math.min(500, jsonHRef.current - dy));
            setJsonH(jsonHRef.current);
          }} />

          {/* Assembly JSON */}
          <div style={{ height: jsonH, display: "flex", flexDirection: "column" }}>
            <div style={{ padding: "5px 10px", borderBottom: "1px solid var(--border)", fontSize: 10, color: "var(--muted)", fontFamily: "monospace", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              assembly json
            </div>
            <AssemblyJSON events={events} />
          </div>
        </div>

      </div>
    </div>
  );
}

// ─── Assembly JSON viewer ─────────────────────────────────────────────────────

function AssemblyJSON({ events }: { events: TraceEvent[] }) {
  // Accumulate all successfully placed bricks from place call pairs
  const bricks: any[] = [];
  const clearedAt: number[] = [];

  events.forEach((ev, i) => {
    if (ev.type === "tool_call" && (ev as any).name === "clear") clearedAt.push(i);
  });

  const lastClear = clearedAt[clearedAt.length - 1] ?? -1;

  events.forEach((ev, i) => {
    if (i <= lastClear) return;
    if (ev.type === "tool_result" && (ev as any).name === "place") {
      const result = (ev as any).result;
      if (!result?.ok) return;
      // Find the matching place call just before this result
      const callIdx = events.slice(0, i).map((e, j) => ({ e, j })).reverse()
        .find(({ e }) => e.type === "tool_call" && (e as any).name === "place")?.j;
      if (callIdx == null) return;
      const spec = ((events[callIdx] as any).input as any).spec;
      const newBricks = Array.isArray(spec) ? spec : [spec];
      bricks.push(...newBricks);
    }
  });

  const hasSave = events.some((e) => e.type === "tool_call" && (e as any).name === "save");

  if (bricks.length === 0) {
    return (
      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", color: "var(--muted)", fontFamily: "monospace", fontSize: 11 }}>
        assembly code appears here
      </div>
    );
  }

  return (
    <pre style={{
      flex: 1, overflowY: "auto", margin: 0, padding: "8px 10px",
      fontSize: 10, color: "var(--muted-light)", fontFamily: "monospace",
      background: "transparent", lineHeight: 1.5,
    }}>
      {JSON.stringify({ bricks, saved: hasSave }, null, 2)}
    </pre>
  );
}
