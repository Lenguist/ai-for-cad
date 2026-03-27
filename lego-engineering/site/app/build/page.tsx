"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import dynamic from "next/dynamic";
import Nav from "../components/Nav";

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
        if (ev.type === "tool_call") return (
          <div key={i} style={{ marginBottom: 4 }}>
            <span style={{ color: "#4caf50" }}>⚙ {ev.name}</span>
            <span style={{ color: "var(--muted)", marginLeft: 8 }}>
              {JSON.stringify(ev.input).slice(0, 120)}
            </span>
          </div>
        );
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

  // Poll sim results
  useEffect(() => {
    const poll = async () => {
      try {
        const r = await fetch(`/workspace/sim_result.json?t=${Date.now()}`);
        if (!r.ok) return;
        const data = await r.json();
        const json = JSON.stringify(data);
        if (json !== prevSimRef.current) {
          prevSimRef.current = json;
          setSim(data);
          setVersion((v) => v + 1);
          setLdrExists(true);
        }
      } catch { /* no file yet */ }
    };
    poll();
    const id = setInterval(poll, 2000);
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
              setEvents((prev) => [...prev, ev]);
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
          width: 220, background: "var(--panel)", borderRight: "1px solid var(--border)",
          display: "flex", flexDirection: "column", flexShrink: 0,
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

        {/* ── Col 3: 3D viewer + status ─────────────────────────── */}
        <div style={{
          width: 380, borderLeft: "1px solid var(--border)",
          display: "flex", flexDirection: "column", flexShrink: 0,
        }}>
          {/* 3D Viewer */}
          <div style={{ flex: 1, position: "relative", minHeight: 0 }}>
            {ldrExists ? (
              <AssemblyViewer ldrUrl="/workspace/assembly.ldr" version={version} />
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

          {/* Assembly JSON */}
          <div style={{ height: 180, borderTop: "1px solid var(--border)", display: "flex", flexDirection: "column" }}>
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
  // Extract the last place call's input as the "code"
  const placeCalls = events.filter((e) => e.type === "tool_call" && (e as any).name === "place");
  const saveCalls = events.filter((e) => e.type === "tool_call" && (e as any).name === "save");
  const inspectResults = events.filter((e) => e.type === "tool_result" && (e as any).name === "inspect");

  // Show the last inspect result (full assembly state) if save was called
  const lastInspect = inspectResults[inspectResults.length - 1] as any;
  const hasSave = saveCalls.length > 0;

  if (!hasSave && placeCalls.length === 0) {
    return (
      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", color: "var(--muted)", fontFamily: "monospace", fontSize: 11 }}>
        assembly code appears here
      </div>
    );
  }

  const displayData = hasSave && lastInspect?.result
    ? { bricks: (lastInspect.result as any).bricks }
    : { last_place: (placeCalls[placeCalls.length - 1] as any)?.input };

  return (
    <pre style={{
      flex: 1, overflowY: "auto", margin: 0, padding: "8px 10px",
      fontSize: 10, color: "var(--muted-light)", fontFamily: "monospace",
      background: "transparent", lineHeight: 1.5,
    }}>
      {JSON.stringify(displayData, null, 2)}
    </pre>
  );
}
