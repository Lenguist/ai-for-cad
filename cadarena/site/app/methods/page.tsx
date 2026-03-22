import Link from "next/link";

const NAV_STYLE = { color: "var(--muted)" as const, textDecoration: "none" as const, fontSize: 14, fontWeight: 500 };

const SECTION_HEAD = { fontSize: 22, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" as const };
const MONO = { fontFamily: "var(--font-geist-mono), monospace" as const };

const MODEL_DETAILS = [
  {
    name: "Claude Opus 4.6",
    tag: "LLM Baseline",
    api: "Anthropic API",
    output: "CadQuery Python",
    score: "95% (19/20)",
    notes: [
      "Prompted zero-shot with a system message instructing CadQuery output.",
      "Code executed locally via Python subprocess with 30s timeout.",
      "1 failure: OpenCASCADE geometry crash on countersunk hole edge case.",
    ],
  },
  {
    name: "Zoo / ML-ephant",
    tag: "Commercial",
    api: "KittyCAD API",
    output: "KCL (Zoo's geometry language)",
    score: "95% (19/20)",
    notes: [
      "Submitted prompt to the ML-ephant text-to-CAD endpoint.",
      "Validated by checking STL file existence in the job response.",
      "KCL source code captured from the `code` field in the job status response.",
      "1 failure: timeout on helical spring computation.",
    ],
  },
  {
    name: "Gemini 2.5 Flash",
    tag: "LLM Baseline",
    api: "Google Generative AI API",
    output: "CadQuery Python",
    score: "70% (14/20)",
    notes: [
      "Prompted zero-shot, same system message as Claude.",
      "Free-tier API hit rate limits after ~7 prompts; exponential backoff applied.",
      "Failures include hallucinated CadQuery methods (.gear(), .cutExtrude()) and wrong variable names.",
      "Score likely reflects free-tier quality, not the model's ceiling.",
    ],
  },
  {
    name: "GPT-5",
    tag: "LLM Baseline",
    api: "OpenAI API",
    output: "CadQuery Python",
    score: "60% (12/20)",
    notes: [
      "Prompted zero-shot, same system message as Claude.",
      "2048 token output limit causes silent truncation on Tier 3–4 prompts.",
      "All 5 Tier 4 failures are due to truncated code, not model reasoning.",
      "Increasing max_tokens would likely improve T3–T4 scores.",
    ],
  },
  {
    name: "Text-to-CadQuery (Qwen 3B)",
    tag: "Academic",
    api: "Self-hosted on Modal GPU",
    output: "CadQuery Python",
    score: "70% (14/20)",
    notes: [
      "Fine-tuned Qwen 3B model from the Text-to-CadQuery paper (arXiv 2025).",
      "Run on Modal A10G GPU via a custom inference endpoint.",
      "Model was trained on normalized 0–1 unit coordinates, not millimeters.",
      "Geometry shapes are correct but all dimensions are scaled to 0–1 range.",
      "Post-processing to rescale units has not been applied yet.",
    ],
  },
];

export default function MethodsPage() {
  return (
    <div style={{ background: "var(--background)", minHeight: "100vh" }}>
      {/* Nav */}
      <nav style={{ borderBottom: "1px solid var(--border)", position: "sticky", top: 0, zIndex: 50, backdropFilter: "blur(12px)", background: "rgba(55,105,160,0.92)" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <Link href="/" style={{ ...MONO, fontSize: 18, fontWeight: 700, color: "var(--accent)", textDecoration: "none", letterSpacing: "-0.02em" }}>
            CAD Arena
          </Link>
          <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
            <Link href="/results" style={NAV_STYLE}>Results</Link>
            <Link href="/try" style={NAV_STYLE}>Try</Link>
            <Link href="/methods" style={{ ...NAV_STYLE, color: "var(--foreground)" }}>Methods</Link>
            <a href="https://github.com/Lenguist/ai-for-cad" style={NAV_STYLE}>GitHub →</a>
          </div>
        </div>
      </nav>

      <div style={{ maxWidth: 860, margin: "0 auto", padding: "56px 24px 80px" }}>

        {/* Header */}
        <h1 style={{ fontSize: 36, fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 12 }}>
          Methodology
        </h1>
        <p style={{ color: "var(--muted)", fontSize: 16, lineHeight: 1.7, marginBottom: 48 }}>
          How results are generated and scored — for both the static benchmark and the live dynamic evaluations.
        </p>

        {/* Static benchmark */}
        <section style={{ marginBottom: 56 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
            <h2 style={SECTION_HEAD}>Static Benchmark</h2>
            <span style={{ ...MONO, fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", padding: "3px 9px", borderRadius: 4, background: "rgba(255,255,255,0.1)", color: "rgba(255,255,255,0.6)" }}>
              FIXED · RUN ONCE
            </span>
          </div>
          <p style={{ color: "var(--muted)", fontSize: 15, lineHeight: 1.7, marginBottom: 24 }}>
            A curated set of 20 prompts run once against each model and reviewed manually.
            Results are a fixed snapshot dated <strong style={{ color: "var(--foreground)" }}>2026-03-08</strong>.
            See <Link href="/results" style={{ color: "var(--accent)", textDecoration: "none" }}>Results</Link> for the full grid.
          </p>

          {/* Prompt design */}
          <div style={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 10, padding: 28, marginBottom: 20 }}>
            <h3 style={{ fontWeight: 700, fontSize: 16, marginBottom: 12 }}>Prompt design</h3>
            <p style={{ color: "var(--muted)", fontSize: 14, lineHeight: 1.7, marginBottom: 16 }}>
              20 prompts spread across 4 tiers of increasing complexity. Prompts are written in plain English,
              describe a single mechanical part, and include explicit dimensions where applicable.
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12 }}>
              {[
                { tier: "T1", label: "Simple Primitives", n: 5, color: "#4ade80", desc: "Basic shapes with no features. Expected ~90%+ success." },
                { tier: "T2", label: "Single Part with Features", n: 5, color: "#60a5fa", desc: "One part with holes, fillets, or chamfers. Expected ~60–80%." },
                { tier: "T3", label: "Multi-Feature Parts", n: 5, color: "#fb923c", desc: "Multiple operations on one body. Expected ~30–50%." },
                { tier: "T4", label: "Complex Functional", n: 5, color: "#f87171", desc: "Gears, springs, assemblies. Expected ~5–20%." },
              ].map((t) => (
                <div key={t.tier} style={{ background: "var(--background)", border: "1px solid var(--border)", borderLeft: `3px solid ${t.color}`, borderRadius: 6, padding: "14px 16px" }}>
                  <div style={{ ...MONO, fontSize: 11, color: t.color, fontWeight: 700, letterSpacing: "0.08em", marginBottom: 4 }}>
                    {t.tier} · {t.label} ({t.n} prompts)
                  </div>
                  <div style={{ color: "var(--muted)", fontSize: 13, lineHeight: 1.5 }}>{t.desc}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Execution pipeline */}
          <div style={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 10, padding: 28, marginBottom: 20 }}>
            <h3 style={{ fontWeight: 700, fontSize: 16, marginBottom: 12 }}>Execution pipeline</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {[
                { step: "1", title: "Generation", desc: "Each prompt is sent to the model API (or self-hosted runner). No few-shot examples — all models are prompted zero-shot unless the model was fine-tuned." },
                { step: "2", title: "Execution", desc: "For CadQuery models: generated Python is run in a subprocess with a 30s timeout. The code is sandboxed — cq.exporters.export() is mocked to prevent file system side effects. A set of fallback variable names is tried if the primary export fails." },
                { step: "3", title: "STL export", desc: "A successful run exports the geometry to STL. For Zoo, the STL is returned directly by the API. For CadQuery models, CadQuery renders the geometry to STL." },
                { step: "4", title: "Scoring", desc: "A result is marked ✓ (success) if a valid, non-empty STL file was produced. No geometry quality metric is applied to the static benchmark — validity only." },
              ].map((s) => (
                <div key={s.step} style={{ display: "flex", gap: 16 }}>
                  <div style={{ ...MONO, fontSize: 12, color: "var(--accent)", fontWeight: 700, minWidth: 20, paddingTop: 2 }}>{s.step}</div>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 4 }}>{s.title}</div>
                    <div style={{ color: "var(--muted)", fontSize: 13, lineHeight: 1.6 }}>{s.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Scoring note */}
          <div style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 8, padding: "14px 18px", fontSize: 13, color: "var(--muted)", lineHeight: 1.6 }}>
            <strong style={{ color: "var(--foreground)" }}>Note on scoring:</strong>{" "}
            &ldquo;Success&rdquo; means the output produced a valid, executable 3D part — not that the part
            matches the prompt geometrically. A cube generated for a prompt asking for a cylinder
            would score ✓. Geometric accuracy metrics (Chamfer distance, VLM scoring) are planned
            but not yet computed.
          </div>
        </section>

        {/* Per-model details */}
        <section style={{ marginBottom: 56 }}>
          <h2 style={{ ...SECTION_HEAD, marginBottom: 16 }}>Per-model details</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {MODEL_DETAILS.map((m) => (
              <div key={m.name} style={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 10, padding: 24 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12, flexWrap: "wrap", gap: 8 }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 2 }}>{m.name}</div>
                    <div style={{ ...MONO, fontSize: 12, color: "var(--muted)" }}>{m.tag} · {m.api} · Output: {m.output}</div>
                  </div>
                  <div style={{ ...MONO, fontWeight: 800, fontSize: 16, color: "var(--foreground)" }}>{m.score}</div>
                </div>
                <ul style={{ margin: 0, paddingLeft: 18, display: "flex", flexDirection: "column", gap: 6 }}>
                  {m.notes.map((note, i) => (
                    <li key={i} style={{ color: "var(--muted)", fontSize: 13, lineHeight: 1.6 }}>{note}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* Dynamic */}
        <section style={{ marginBottom: 56 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
            <h2 style={SECTION_HEAD}>Dynamic Evaluation</h2>
            <span style={{ ...MONO, fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", padding: "3px 9px", borderRadius: 4, background: "rgba(96,165,250,0.15)", color: "#60a5fa" }}>
              COMING SOON
            </span>
          </div>
          <p style={{ color: "var(--muted)", fontSize: 15, lineHeight: 1.7, marginBottom: 20 }}>
            The <Link href="/try" style={{ color: "var(--accent)", textDecoration: "none" }}>Try</Link> page
            will let you submit any prompt and get results from all models in real time.
            The pipeline is identical to the static benchmark — same models, same execution engine, same scoring.
          </p>
          <div style={{ background: "var(--card)", border: "1px solid var(--border)", borderRadius: 10, padding: 24 }}>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {[
                { title: "Consent & storage", desc: "You will be asked whether your prompt and results can be saved to the public dataset. If yes, results appear in the Explore page for others to browse." },
                { title: "Rate limits", desc: "Anonymous users: 3 prompts/day. Free account (email sign-in): 20 prompts/day. No paid tier — this is a research tool." },
                { title: "Latency", desc: "Expect 5–20s depending on the model. Academic models (self-hosted) may take longer. Results stream per-model as they complete." },
              ].map((item) => (
                <div key={item.title} style={{ display: "flex", gap: 16 }}>
                  <div style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--accent)", marginTop: 7, flexShrink: 0 }} />
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 3 }}>{item.title}</div>
                    <div style={{ color: "var(--muted)", fontSize: 13, lineHeight: 1.6 }}>{item.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Contact */}
        <section>
          <p style={{ color: "var(--muted)", fontSize: 14, lineHeight: 1.7 }}>
            Questions about methodology or want to submit a model?{" "}
            <a href="mailto:contact@cadarena.dev" style={{ color: "var(--accent)", textDecoration: "none" }}>
              contact@cadarena.dev
            </a>
          </p>
        </section>

      </div>
    </div>
  );
}
