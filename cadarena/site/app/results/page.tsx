import Link from "next/link";
import resultsData from "../data/results.json";

const MODEL_LABELS: Record<string, string> = {
  "claude-opus-4-6": "Claude Opus 4.6",
  "zoo-ml-ephant": "Zoo ML-ephant",
  "gemini-2.5-flash": "Gemini 2.5 Flash",
  "gpt-5": "GPT-5",
  "text2cadquery-qwen": "Text2CadQuery (Qwen 3B)",
};

const MODEL_TAGS: Record<string, string> = {
  "claude-opus-4-6": "LLM Baseline",
  "zoo-ml-ephant": "Commercial",
  "gemini-2.5-flash": "LLM Baseline",
  "gpt-5": "LLM Baseline",
  "text2cadquery-qwen": "Academic",
};

const MODELS = ["claude-opus-4-6", "zoo-ml-ephant", "gemini-2.5-flash", "gpt-5", "text2cadquery-qwen"];
const TIERS = [1, 2, 3, 4];
const TIER_LABELS = ["", "Simple Primitives", "Single Part with Features", "Multi-Feature Parts", "Complex Functional"];

export default function ResultsPage() {
  const results = resultsData.results;

  // Build lookup: model → prompt_id → result
  const lookup: Record<string, Record<string, (typeof results)[0]>> = {};
  for (const r of results) {
    if (!lookup[r.model_id]) lookup[r.model_id] = {};
    lookup[r.model_id][r.prompt_id] = r;
  }

  // Get unique prompt ids per tier
  const promptsByTier: Record<number, string[]> = {};
  for (const t of TIERS) {
    const prefix = `t${t}_`;
    const ids = [...new Set(results.filter((r) => r.prompt_id.startsWith(prefix)).map((r) => r.prompt_id))].sort();
    promptsByTier[t] = ids;
  }

  // Summary stats per model
  const summary = MODELS.map((m) => {
    const rs = results.filter((r) => r.model_id === m);
    const ok = rs.filter((r) => r.success).length;
    const total = rs.length;
    const avgLat = rs.reduce((a, b) => a + b.latency_s, 0) / (total || 1);
    const tierOk: number[] = TIERS.map((t) => {
      const tr = rs.filter((r) => r.tier === t);
      return tr.filter((r) => r.success).length;
    });
    return { model: m, ok, total, avgLat, tierOk };
  });

  return (
    <div style={{ background: "var(--background)", minHeight: "100vh" }}>
      {/* Nav */}
      <nav style={{ borderBottom: "1px solid var(--border)", position: "sticky", top: 0, zIndex: 50, backdropFilter: "blur(12px)", background: "rgba(55,105,160,0.92)" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <Link href="/" style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 18, fontWeight: 700, color: "var(--accent)", textDecoration: "none", letterSpacing: "-0.02em" }}>
            CAD Arena
          </Link>
          <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
            <Link href="/results" style={{ color: "var(--foreground)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}>Results</Link>
            <Link href="/try" style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}>Try</Link>
            <Link href="/methods" style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}>Methods</Link>
            <a href="https://github.com/Lenguist/ai-for-cad" style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}>GitHub →</a>
          </div>
        </div>
      </nav>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "48px 24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
          <h1 style={{ fontSize: 32, fontWeight: 800, color: "var(--foreground)", letterSpacing: "-0.02em", margin: 0 }}>
            Benchmark Results
          </h1>
          <span style={{
            fontFamily: "var(--font-geist-mono), monospace",
            fontSize: 11, fontWeight: 700, letterSpacing: "0.08em",
            padding: "4px 10px", borderRadius: 4,
            background: "rgba(255,255,255,0.1)", color: "rgba(255,255,255,0.6)",
          }}>
            STATIC
          </span>
        </div>
        <p style={{ color: "var(--muted)", fontSize: 15, marginBottom: 8, lineHeight: 1.6 }}>
          20 hand-selected prompts run once across 5 models, results reviewed manually.
          This is a fixed snapshot — not a live leaderboard.
          Click any cell to see the generated code and 3D rendering.
        </p>
        <p style={{ color: "var(--muted)", fontSize: 13, marginBottom: 40 }}>
          See <Link href="/methods" style={{ color: "var(--accent)", textDecoration: "none" }}>Methods</Link> for
          how each model was run and scored.
        </p>

        {/* Summary row */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 12, marginBottom: 40 }}>
          {summary.map((s) => (
            <div key={s.model} style={{ background: "rgba(0,0,0,0.12)", border: "1px solid var(--border)", padding: "18px 20px" }}>
              <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 6 }}>
                <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 9, color: "rgba(255,255,255,0.5)", background: "rgba(255,255,255,0.1)", padding: "1px 5px", letterSpacing: "0.08em" }}>{MODEL_TAGS[s.model]}</span>
              </div>
              <div style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.08em", marginBottom: 6 }}>
                {MODEL_LABELS[s.model]}
              </div>
              <div style={{ fontSize: 28, fontWeight: 800, color: "var(--foreground)", letterSpacing: "-0.02em" }}>
                {Math.round((s.ok / s.total) * 100)}%
              </div>
              <div style={{ fontSize: 12, color: "var(--muted)", marginTop: 4 }}>
                {s.ok}/{s.total} · {s.avgLat.toFixed(1)}s avg
              </div>
            </div>
          ))}
        </div>

        {/* Results grid by tier */}
        {TIERS.map((tier) => (
          <div key={tier} style={{ marginBottom: 40 }}>
            <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 12 }}>
              <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.1em" }}>
                TIER {tier}
              </span>
              <span style={{ fontSize: 14, color: "rgba(255,255,255,0.7)" }}>{TIER_LABELS[tier]}</span>
            </div>

            <div style={{ border: "1px solid var(--border)", overflow: "hidden" }}>
              {/* Header */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr repeat(5, 110px)", background: "rgba(0,0,0,0.2)" }}>
                <div style={{ padding: "10px 16px", fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.08em" }}>PROMPT</div>
                {MODELS.map((m) => (
                  <div key={m} style={{ padding: "10px 12px", fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.08em", borderLeft: "1px solid var(--border)", textAlign: "center" }}>
                    {MODEL_LABELS[m].split(" ")[0]}
                  </div>
                ))}
              </div>

              {/* Rows */}
              {promptsByTier[tier].map((pid, i) => {
                const prompt = results.find((r) => r.prompt_id === pid)?.prompt || pid;
                return (
                  <div key={pid} style={{ display: "grid", gridTemplateColumns: "1fr repeat(5, 110px)", borderTop: "1px solid var(--border)", background: i % 2 === 0 ? "rgba(0,0,0,0.05)" : "transparent" }}>
                    {/* Prompt text */}
                    <div style={{ padding: "12px 16px", fontSize: 13, color: "rgba(255,255,255,0.8)", lineHeight: 1.4 }}>
                      <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", marginRight: 8 }}>{pid}</span>
                      {prompt.length > 80 ? prompt.slice(0, 80) + "…" : prompt}
                    </div>

                    {/* Model cells */}
                    {MODELS.map((m) => {
                      const r = lookup[m]?.[pid];
                      if (!r) return <div key={m} style={{ borderLeft: "1px solid var(--border)", display: "flex", alignItems: "center", justifyContent: "center" }}><span style={{ color: "var(--muted)", fontSize: 12 }}>—</span></div>;

                      const ok = r.success;
                      const hasStl = !!r.stl_url;
                      const hasCode = !!r.code;

                      return (
                        <Link
                          key={m}
                          href={`/results/${m}/${pid}`}
                          style={{
                            borderLeft: "1px solid var(--border)",
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            justifyContent: "center",
                            padding: "10px 8px",
                            gap: 4,
                            textDecoration: "none",
                            background: ok ? "rgba(255,255,255,0.04)" : "rgba(255,0,0,0.04)",
                            cursor: "pointer",
                            transition: "background 0.15s",
                          }}
                        >
                          <span style={{ fontSize: 18 }}>{ok ? "✓" : "✗"}</span>
                          <div style={{ display: "flex", gap: 4 }}>
                            {hasStl && <span style={{ fontSize: 9, background: "rgba(255,255,255,0.15)", padding: "1px 5px", fontFamily: "var(--font-geist-mono), monospace", color: "rgba(255,255,255,0.7)" }}>3D</span>}
                            {hasCode && <span style={{ fontSize: 9, background: "rgba(255,255,255,0.15)", padding: "1px 5px", fontFamily: "var(--font-geist-mono), monospace", color: "rgba(255,255,255,0.7)" }}>{(r as { output_type?: string }).output_type === "kcl" ? "KCL" : "PY"}</span>}
                          </div>
                        </Link>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          </div>
        ))}

        {/* Legend */}
        <div style={{ display: "flex", gap: 24, color: "var(--muted)", fontSize: 13, marginTop: 8 }}>
          <span>✓ = executed successfully</span>
          <span>✗ = failed</span>
          <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11 }}>3D</span><span>= 3D render available</span>
          <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11 }}>PY</span><span>= source code available</span>
        </div>
      </div>
    </div>
  );
}
