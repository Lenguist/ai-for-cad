import { notFound } from "next/navigation";
import Link from "next/link";
import resultsData from "../../../data/results.json";
import STLViewer from "../../../components/STLViewer";

const MODEL_LABELS: Record<string, string> = {
  "claude-opus-4-6": "Claude Opus 4.6",
  "zoo-ml-ephant": "Zoo ML-ephant",
  "gemini-2.5-flash": "Gemini 2.5 Flash",
  "gpt-5": "GPT-5",
};

const MODELS = ["claude-opus-4-6", "zoo-ml-ephant", "gemini-2.5-flash", "gpt-5"];
const TIER_LABELS = ["", "Basic primitives", "Multi-feature parts", "Assemblies", "Complex geometry"];

export function generateStaticParams() {
  return resultsData.results.map((r) => ({
    model: r.model_id,
    prompt: r.prompt_id,
  }));
}

export default async function ResultDetailPage({
  params,
}: {
  params: Promise<{ model: string; prompt: string }>;
}) {
  const { model, prompt: promptId } = await params;
  const r = resultsData.results.find((x) => x.model_id === model && x.prompt_id === promptId);
  if (!r) notFound();

  // Find same prompt results for other models
  const otherResults = MODELS.filter((m) => m !== model)
    .map((m) => resultsData.results.find((x) => x.model_id === m && x.prompt_id === promptId))
    .filter(Boolean) as typeof resultsData.results;

  return (
    <div style={{ background: "var(--background)", minHeight: "100vh" }}>
      {/* Nav */}
      <nav style={{ borderBottom: "1px solid var(--border)", position: "sticky", top: 0, zIndex: 50, backdropFilter: "blur(12px)", background: "rgba(55,105,160,0.92)" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <Link href="/" style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 18, fontWeight: 700, color: "var(--accent)", textDecoration: "none", letterSpacing: "-0.02em" }}>
            CAD Arena
          </Link>
          <div style={{ display: "flex", gap: 20, alignItems: "center" }}>
            <Link href="/results" style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}>
              ← All results
            </Link>
          </div>
        </div>
      </nav>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "40px 24px" }}>
        {/* Header */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 12 }}>
            <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.1em" }}>
              TIER {r.tier} · {TIER_LABELS[r.tier].toUpperCase()}
            </span>
            <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)" }}>·</span>
            <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.08em" }}>
              {promptId}
            </span>
          </div>
          <p style={{ fontSize: 18, color: "var(--foreground)", lineHeight: 1.5, maxWidth: 800, fontWeight: 500 }}>
            {r.prompt}
          </p>
        </div>

        {/* Model comparison bar */}
        <div style={{ display: "flex", gap: 8, marginBottom: 32, flexWrap: "wrap" }}>
          {MODELS.map((m) => {
            const mr = resultsData.results.find((x) => x.model_id === m && x.prompt_id === promptId);
            const isActive = m === model;
            const ok = mr?.success;
            return (
              <Link
                key={m}
                href={`/results/${m}/${promptId}`}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                  padding: "7px 14px",
                  border: isActive ? "1px solid rgba(255,255,255,0.7)" : "1px solid var(--border)",
                  background: isActive ? "rgba(255,255,255,0.15)" : "rgba(0,0,0,0.1)",
                  textDecoration: "none",
                  fontSize: 13,
                  color: isActive ? "var(--foreground)" : "var(--muted)",
                  fontFamily: "var(--font-geist-mono), monospace",
                }}
              >
                <span>{ok ? "✓" : mr ? "✗" : "—"}</span>
                <span>{MODEL_LABELS[m]}</span>
              </Link>
            );
          })}
        </div>

        {/* Main content: 3D + code side by side */}
        <div style={{ display: "grid", gridTemplateColumns: r.stl_url ? "1fr 1fr" : "1fr", gap: 20, marginBottom: 32 }}>
          {/* 3D viewer */}
          {r.stl_url && (
            <div style={{ border: "1px solid var(--border)", overflow: "hidden" }}>
              <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--border)", background: "rgba(0,0,0,0.15)", fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.08em" }}>
                3D RENDER · {MODEL_LABELS[model]}
              </div>
              <STLViewer url={r.stl_url} width={500} height={380} />
            </div>
          )}

          {/* Code */}
          {r.code ? (
            <div style={{ border: "1px solid var(--border)", overflow: "hidden", display: "flex", flexDirection: "column" }}>
              <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--border)", background: "rgba(0,0,0,0.15)", fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.08em", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                  <span style={{ background: "rgba(255,255,255,0.15)", color: "rgba(255,255,255,0.9)", padding: "2px 7px", fontSize: 10, letterSpacing: "0.08em" }}>
                    {(r as { language?: string }).language?.toUpperCase() ?? "SOURCE"}
                  </span>
                  <span>SOURCE</span>
                </div>
                <span style={{ color: r.success ? "rgba(255,255,255,0.7)" : "rgba(255,100,100,0.8)" }}>
                  {r.success ? "✓ executed" : `✗ ${r.error?.slice(0, 60) || "failed"}`}
                </span>
              </div>
              <pre style={{ margin: 0, padding: "16px", fontSize: 12, lineHeight: 1.6, color: "rgba(255,255,255,0.88)", background: "rgba(0,0,0,0.15)", overflowX: "auto", overflowY: "auto", flex: 1, fontFamily: "var(--font-geist-mono), monospace", maxHeight: 380 }}>
                {r.code}
              </pre>
            </div>
          ) : (
            <div style={{ border: "1px solid var(--border)", padding: "24px", background: "rgba(0,0,0,0.1)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <div style={{ textAlign: "center", color: "var(--muted)" }}>
                <div style={{ fontSize: 32, marginBottom: 8 }}>✗</div>
                <div style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 12 }}>
                  {r.error ? r.error.slice(0, 120) : "No code generated"}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Compare with other models */}
        {otherResults.length > 0 && (
          <div>
            <div style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", letterSpacing: "0.1em", marginBottom: 14 }}>
              COMPARE · SAME PROMPT
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
              {otherResults.map((or) => (
                <Link
                  key={or.model_id}
                  href={`/results/${or.model_id}/${promptId}`}
                  style={{ border: "1px solid var(--border)", overflow: "hidden", textDecoration: "none", display: "block" }}
                >
                  <div style={{ padding: "10px 14px", background: "rgba(0,0,0,0.15)", borderBottom: "1px solid var(--border)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)" }}>
                      {MODEL_LABELS[or.model_id]}
                    </span>
                    <span style={{ fontSize: 13, color: or.success ? "rgba(255,255,255,0.8)" : "rgba(255,100,100,0.7)" }}>
                      {or.success ? "✓" : "✗"}
                    </span>
                  </div>
                  {or.stl_url ? (
                    <STLViewer url={or.stl_url} width={300} height={180} />
                  ) : (
                    <div style={{ height: 180, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.1)" }}>
                      <span style={{ color: "var(--muted)", fontFamily: "var(--font-geist-mono), monospace", fontSize: 12 }}>
                        {or.error ? or.error.slice(0, 60) : "no output"}
                      </span>
                    </div>
                  )}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
