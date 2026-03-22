"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import dynamic from "next/dynamic";

const STLViewer = dynamic(() => import("../components/STLViewer"), { ssr: false });

const NAV_LINK = { color: "var(--muted)" as const, textDecoration: "none" as const, fontSize: 14, fontWeight: 500 };
const MONO = { fontFamily: "var(--font-geist-mono), monospace" as const };

const AVAILABLE_MODELS = [
  { id: "claude-opus-4-6",  label: "Claude Opus 4.6",       tag: "LLM Baseline" },
  { id: "zoo-ml-ephant",    label: "Zoo / ML-ephant",        tag: "Commercial"   },
  { id: "gemini-2.5-flash", label: "Gemini 2.5 Flash",       tag: "LLM Baseline" },
  { id: "gpt-5",            label: "GPT-5",                   tag: "LLM Baseline" },
];

const UNAVAILABLE_MODELS = [
  { id: "text2cadquery-qwen", label: "Text-to-CadQuery (Qwen 3B)", tag: "Academic", reason: "GPU runner offline" },
];

type ModelResult = {
  status: "loading" | "done" | "error";
  code?: string;
  outputType?: string;
  stlBase64?: string;
  stlUrl?: string;
  latency?: number;
  error?: string;
};

const EXAMPLE_PROMPTS = [
  "A cylinder 20mm diameter, 50mm tall",
  "A rectangular plate 60 × 40 × 5mm with four M4 holes at the corners (5mm from each edge)",
  "An L-shaped bracket with 40mm arms, 5mm thick, 30mm tall",
  "A spur gear with 20 teeth, module 2, 10mm thick, 8mm center bore",
];

export default function TryPage() {
  const [prompt, setPrompt] = useState("");
  const [selectedModels, setSelectedModels] = useState<Set<string>>(
    new Set(AVAILABLE_MODELS.map((m) => m.id))
  );
  const [results, setResults] = useState<Record<string, ModelResult>>({});
  const [isGenerating, setIsGenerating] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  // Clean up blob URLs on unmount
  useEffect(() => {
    return () => {
      Object.values(results).forEach((r) => {
        if (r.stlUrl) URL.revokeObjectURL(r.stlUrl);
      });
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  function toggleModel(id: string) {
    setSelectedModels((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        if (next.size === 1) return prev; // keep at least one
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }

  async function handleGenerate() {
    if (!prompt.trim() || isGenerating) return;

    // Reset results with loading state for selected models
    const initial: Record<string, ModelResult> = {};
    for (const id of selectedModels) initial[id] = { status: "loading" };
    setResults(initial);
    setIsGenerating(true);

    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const resp = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, models: [...selectedModels] }),
        signal: controller.signal,
      });

      if (!resp.ok || !resp.body) throw new Error("API error");

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const data = JSON.parse(line.slice(6)) as {
              modelId: string;
              code?: string;
              outputType?: string;
              stlBase64?: string;
              latency: number;
              error?: string;
            };

            let stlUrl: string | undefined;
            if (data.stlBase64) {
              const bytes = Uint8Array.from(atob(data.stlBase64), (c) => c.charCodeAt(0));
              const blob = new Blob([bytes], { type: "model/stl" });
              stlUrl = URL.createObjectURL(blob);
            }

            setResults((prev) => ({
              ...prev,
              [data.modelId]: {
                status: data.error ? "error" : "done",
                code: data.code,
                outputType: data.outputType,
                stlBase64: data.stlBase64,
                stlUrl,
                latency: data.latency,
                error: data.error,
              },
            }));
          } catch {
            // malformed SSE line, skip
          }
        }
      }
    } catch (e) {
      if ((e as Error).name !== "AbortError") {
        console.error("Generate error:", e);
      }
    } finally {
      setIsGenerating(false);
      abortRef.current = null;
    }
  }

  const anyResults = Object.keys(results).length > 0;

  return (
    <div style={{ background: "var(--background)", minHeight: "100vh" }}>
      {/* Nav */}
      <nav style={{ borderBottom: "1px solid var(--border)", position: "sticky", top: 0, zIndex: 50, backdropFilter: "blur(12px)", background: "rgba(55,105,160,0.92)" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <Link href="/" style={{ ...MONO, fontSize: 18, fontWeight: 700, color: "var(--accent)", textDecoration: "none", letterSpacing: "-0.02em" }}>
            CAD Arena
          </Link>
          <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
            <Link href="/results" style={NAV_LINK}>Results</Link>
            <Link href="/try" style={{ ...NAV_LINK, color: "var(--foreground)" }}>Try</Link>
            <Link href="/methods" style={NAV_LINK}>Methods</Link>
            <a href="https://github.com/Lenguist/ai-for-cad" style={NAV_LINK}>GitHub →</a>
          </div>
        </div>
      </nav>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "48px 24px 80px" }}>
        {/* Header */}
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <h1 style={{ fontSize: 32, fontWeight: 800, letterSpacing: "-0.02em", margin: 0 }}>Try It</h1>
          <span style={{ ...MONO, fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", padding: "4px 10px", borderRadius: 4, background: "rgba(96,165,250,0.15)", color: "#60a5fa" }}>
            DYNAMIC
          </span>
        </div>
        <p style={{ color: "var(--muted)", fontSize: 15, marginBottom: 40, lineHeight: 1.6 }}>
          Enter any prompt and get live results from all models. Same pipeline as the{" "}
          <Link href="/results" style={{ color: "var(--accent)", textDecoration: "none" }}>static benchmark</Link>.
        </p>

        {/* Input area */}
        <div style={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12, padding: 28, marginBottom: 24 }}>
          <label style={{ ...MONO, fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", color: "var(--muted)", display: "block", marginBottom: 10 }}>
            PROMPT
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) handleGenerate(); }}
            placeholder="Describe a mechanical part in plain English, e.g. &quot;A cylinder 20mm diameter, 50mm tall&quot;"
            rows={3}
            style={{
              width: "100%",
              background: "var(--background)",
              border: "1px solid var(--border)",
              borderRadius: 8,
              padding: "14px 16px",
              color: "var(--foreground)",
              fontSize: 15,
              lineHeight: 1.6,
              resize: "vertical",
              outline: "none",
              boxSizing: "border-box",
              ...MONO,
            }}
          />

          {/* Example prompts */}
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 10 }}>
            <span style={{ fontSize: 12, color: "var(--muted)", alignSelf: "center" }}>Examples:</span>
            {EXAMPLE_PROMPTS.map((ex) => (
              <button
                key={ex}
                onClick={() => setPrompt(ex)}
                style={{
                  background: "rgba(255,255,255,0.07)",
                  border: "1px solid var(--border)",
                  borderRadius: 5,
                  padding: "4px 10px",
                  color: "var(--muted)",
                  fontSize: 12,
                  cursor: "pointer",
                  ...MONO,
                }}
              >
                {ex.length > 40 ? ex.slice(0, 40) + "…" : ex}
              </button>
            ))}
          </div>
        </div>

        {/* Model selection */}
        <div style={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 12, padding: 28, marginBottom: 24 }}>
          <label style={{ ...MONO, fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", color: "var(--muted)", display: "block", marginBottom: 14 }}>
            MODELS
          </label>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {AVAILABLE_MODELS.map((m) => {
              const selected = selectedModels.has(m.id);
              return (
                <button
                  key={m.id}
                  onClick={() => toggleModel(m.id)}
                  style={{
                    padding: "8px 16px",
                    borderRadius: 8,
                    border: selected ? "1px solid rgba(255,255,255,0.5)" : "1px solid var(--border)",
                    background: selected ? "rgba(255,255,255,0.12)" : "transparent",
                    color: selected ? "var(--foreground)" : "var(--muted)",
                    cursor: "pointer",
                    fontSize: 13,
                    fontWeight: selected ? 600 : 400,
                    transition: "all 0.15s",
                  }}
                >
                  {selected ? "✓ " : ""}{m.label}
                  <span style={{ ...MONO, fontSize: 10, marginLeft: 6, opacity: 0.6 }}>{m.tag}</span>
                </button>
              );
            })}
            {UNAVAILABLE_MODELS.map((m) => (
              <button
                key={m.id}
                disabled
                title={m.reason}
                style={{
                  padding: "8px 16px",
                  borderRadius: 8,
                  border: "1px solid var(--border)",
                  background: "transparent",
                  color: "rgba(255,255,255,0.25)",
                  cursor: "not-allowed",
                  fontSize: 13,
                  opacity: 0.5,
                }}
              >
                {m.label}
                <span style={{ ...MONO, fontSize: 10, marginLeft: 6 }}>{m.reason}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Generate button */}
        <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 48 }}>
          <button
            onClick={handleGenerate}
            disabled={!prompt.trim() || isGenerating || selectedModels.size === 0}
            style={{
              background: prompt.trim() && !isGenerating ? "rgba(255,255,255,0.9)" : "rgba(255,255,255,0.2)",
              color: prompt.trim() && !isGenerating ? "#3568a0" : "rgba(255,255,255,0.4)",
              border: "none",
              borderRadius: 8,
              padding: "12px 32px",
              fontSize: 15,
              fontWeight: 700,
              cursor: prompt.trim() && !isGenerating ? "pointer" : "not-allowed",
              transition: "all 0.15s",
            }}
          >
            {isGenerating ? "Generating…" : "Generate →"}
          </button>
          {isGenerating && (
            <span style={{ color: "var(--muted)", fontSize: 13 }}>
              Running {selectedModels.size} model{selectedModels.size > 1 ? "s" : ""} in parallel…
            </span>
          )}
          <span style={{ color: "var(--muted)", fontSize: 12, marginLeft: "auto" }}>
            ⌘ + Enter to generate
          </span>
        </div>

        {/* Results */}
        {anyResults && (
          <div>
            <div style={{ ...MONO, fontSize: 11, fontWeight: 700, letterSpacing: "0.1em", color: "var(--muted)", marginBottom: 16 }}>
              RESULTS
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: 16 }}>
              {AVAILABLE_MODELS.filter((m) => results[m.id]).map((m) => {
                const r = results[m.id];
                return (
                  <div
                    key={m.id}
                    style={{
                      background: "var(--card)",
                      border: r.status === "error" ? "1px solid rgba(248,113,113,0.3)" : "1px solid var(--border)",
                      borderRadius: 12,
                      overflow: "hidden",
                    }}
                  >
                    {/* Card header */}
                    <div style={{ padding: "14px 18px", borderBottom: "1px solid var(--border)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: 14 }}>{m.label}</div>
                        <div style={{ ...MONO, fontSize: 11, color: "var(--muted)" }}>{m.tag}</div>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        {r.status === "loading" && (
                          <span style={{ ...MONO, fontSize: 12, color: "var(--muted)", animation: "pulse 1.5s infinite" }}>⟳ running…</span>
                        )}
                        {r.status === "done" && (
                          <>
                            <span style={{ fontSize: 16 }}>✓</span>
                            {r.latency && <span style={{ ...MONO, fontSize: 11, color: "var(--muted)" }}>{r.latency.toFixed(1)}s</span>}
                            {r.outputType && (
                              <span style={{ ...MONO, fontSize: 10, padding: "2px 6px", background: "rgba(255,255,255,0.12)", borderRadius: 4 }}>
                                {r.outputType === "kcl" ? "KCL" : "PY"}
                              </span>
                            )}
                          </>
                        )}
                        {r.status === "error" && (
                          <span style={{ fontSize: 16, color: "#f87171" }}>✗</span>
                        )}
                      </div>
                    </div>

                    {/* 3D viewer for Zoo when STL available */}
                    {r.status === "done" && r.stlUrl && (
                      <div style={{ borderBottom: "1px solid var(--border)" }}>
                        <STLViewer url={r.stlUrl} width={320} height={220} />
                      </div>
                    )}

                    {/* Code or error */}
                    <div style={{ maxHeight: 280, overflow: "auto" }}>
                      {r.status === "loading" && (
                        <div style={{ padding: 24, color: "var(--muted)", fontSize: 13, textAlign: "center" }}>
                          Waiting for response…
                        </div>
                      )}
                      {r.status === "error" && (
                        <div style={{ padding: 16, color: "#f87171", fontSize: 12, lineHeight: 1.6, ...MONO }}>
                          {r.error}
                        </div>
                      )}
                      {r.status === "done" && r.code && (
                        <pre style={{
                          margin: 0,
                          padding: "14px 16px",
                          fontSize: 11,
                          lineHeight: 1.6,
                          color: "rgba(255,255,255,0.8)",
                          overflowX: "auto",
                          background: "transparent",
                          ...MONO,
                        }}>
                          {r.code}
                        </pre>
                      )}
                      {r.status === "done" && !r.code && !r.error && (
                        <div style={{ padding: 16, color: "var(--muted)", fontSize: 13 }}>No code returned.</div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Note */}
            <p style={{ marginTop: 20, fontSize: 13, color: "var(--muted)", lineHeight: 1.6 }}>
              <strong style={{ color: "var(--foreground)" }}>Note:</strong> Code is shown as-is from the model.
              3D rendering is available for Zoo (returns geometry directly).
              For CadQuery models, code must be executed in a Python environment — execution runner coming soon.
            </p>
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </div>
  );
}
