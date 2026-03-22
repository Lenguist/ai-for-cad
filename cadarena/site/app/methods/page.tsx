import Link from "next/link";

const MONO = { fontFamily: "var(--font-geist-mono), monospace" as const };

const MODEL_DETAILS = [
  {
    name: "Claude Opus 4.6",
    tag: "LLM Baseline · Anthropic API",
    output: "CadQuery Python",
    score: "19/20",
    notes: [
      "Prompted zero-shot with a system message instructing CadQuery output.",
      "Code executed locally via Python subprocess with 30s timeout.",
      "1 failure: OpenCASCADE geometry crash on countersunk hole edge case.",
    ],
  },
  {
    name: "Zoo / ML-ephant",
    tag: "Commercial · KittyCAD API",
    output: "KCL (Zoo's geometry language)",
    score: "19/20",
    notes: [
      "Submitted prompt to the ML-ephant text-to-CAD endpoint.",
      "Validated by checking STL file existence in the job response.",
      "KCL source code captured from the `code` field in the job status response.",
      "1 failure: timeout on helical spring computation.",
    ],
  },
  {
    name: "Gemini 2.5 Flash",
    tag: "LLM Baseline · Google Generative AI API",
    output: "CadQuery Python",
    score: "14/20",
    notes: [
      "Prompted zero-shot, same system message as Claude.",
      "Free-tier API hit rate limits after ~7 prompts; exponential backoff applied.",
      "Failures include hallucinated CadQuery methods (.gear(), .cutExtrude()) and wrong variable names.",
      "Score likely reflects free-tier quality, not the model's ceiling.",
    ],
  },
  {
    name: "GPT-5",
    tag: "LLM Baseline · OpenAI API",
    output: "CadQuery Python",
    score: "12/20",
    notes: [
      "Prompted zero-shot, same system message as Claude.",
      "2048 token output limit causes silent truncation on Tier 3–4 prompts.",
      "All 5 Tier 4 failures are due to truncated code, not model reasoning.",
      "Increasing max_tokens would likely improve T3–T4 scores.",
    ],
  },
  {
    name: "Text-to-CadQuery (Qwen 3B)",
    tag: "Academic · Self-hosted on Modal GPU",
    output: "CadQuery Python",
    score: "14/20",
    notes: [
      "Fine-tuned Qwen 3B model from the Text-to-CadQuery paper (arXiv 2025).",
      "Run on Modal A10G GPU via a custom inference endpoint.",
      "Model was trained on normalized 0–1 unit coordinates, not millimeters.",
      "Geometry shapes are correct but all dimensions are scaled to 0–1 range.",
    ],
  },
];

const TIERS = [
  { tier: "T4", label: "Complex Functional", color: "#f87171", desc: "Gears, springs, snap-fit assemblies — hardest tier.", n: 5 },
  { tier: "T3", label: "Multi-Feature Parts", color: "#fb923c", desc: "Multiple boolean operations on a single body.", n: 5 },
  { tier: "T2", label: "Single Part with Features", color: "#facc15", desc: "One part with holes, fillets, or chamfers.", n: 5 },
  { tier: "T1", label: "Simple Primitives", color: "#4ade80", desc: "Basic shapes with no features — boxes, cylinders, spheres.", n: 5 },
];

const PIPELINE = [
  { step: "1", title: "Generation", desc: "Each prompt is sent to the model API (or self-hosted runner). No few-shot examples — all models are prompted zero-shot unless fine-tuned." },
  { step: "2", title: "Execution", desc: "For CadQuery models: generated Python is run in a subprocess with a 30s timeout. cq.exporters.export() is mocked; fallback variable names are tried if the primary export fails." },
  { step: "3", title: "STL export", desc: "A successful run exports the geometry to STL. For Zoo, the STL is returned directly by the API. For CadQuery models, CadQuery renders the geometry to STL." },
  { step: "4", title: "Scoring", desc: "A result is marked ✓ (success) if a valid, non-empty STL file was produced. Validity only — no geometry quality metric is applied." },
];

const NAV_STYLE = { color: "var(--muted)" as const, textDecoration: "none" as const, fontSize: 14, fontWeight: 500 };

export default function MethodsPage() {
  return (
    <div style={{ background: "var(--background)", minHeight: "100vh" }}>
      {/* Nav */}
      <nav style={{ borderBottom: "1px solid rgba(255,255,255,0.25)", position: "sticky", top: 0, zIndex: 50, backdropFilter: "blur(12px)", background: "rgba(55,105,160,0.92)" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <Link href="/" style={{ ...MONO, fontSize: 18, fontWeight: 700, color: "white", textDecoration: "none", letterSpacing: "-0.02em" }}>
            CAD Arena
          </Link>
          <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
            <Link href="/results" style={NAV_STYLE}>Results</Link>
            <Link href="/try" style={NAV_STYLE}>Try</Link>
            <Link href="/methods" style={{ ...NAV_STYLE, color: "white" }}>Methods</Link>
            <a href="https://github.com/Lenguist/ai-for-cad" style={NAV_STYLE}>GitHub →</a>
          </div>
        </div>
      </nav>

      <div style={{ maxWidth: 860, margin: "0 auto", padding: "56px 24px 80px" }}>

        {/* Header */}
        <h1 style={{ fontSize: 36, fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 12 }}>
          Methodology
        </h1>
        <p style={{ color: "var(--muted)", fontSize: 16, lineHeight: 1.7, marginBottom: 56 }}>
          How results are generated and scored — for both the static benchmark and the live dynamic evaluations.
        </p>

        {/* ── Static Benchmark ── */}
        <section style={{ marginBottom: 64 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 24 }}>
            <h2 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: "-0.02em" }}>Static Benchmark</h2>
            <span style={{ ...MONO, fontSize: 10, fontWeight: 700, letterSpacing: "0.1em", padding: "3px 9px", border: "1px solid rgba(255,255,255,0.3)", color: "rgba(255,255,255,0.6)" }}>
              FIXED · RUN ONCE
            </span>
          </div>
          <p style={{ color: "var(--muted)", fontSize: 15, lineHeight: 1.7, marginBottom: 32 }}>
            A curated set of 20 prompts run once against each model and reviewed manually.
            Results are a fixed snapshot dated <strong style={{ color: "white" }}>2026-03-08</strong>.
            See <Link href="/results" style={{ color: "#facc15", textDecoration: "none" }}>Results</Link> for the full grid.
          </p>

          {/* Prompt design — ruled table */}
          <h3 style={{ fontSize: 11, fontWeight: 700, marginBottom: 12, color: "rgba(255,255,255,0.6)", ...MONO, letterSpacing: "0.06em", textTransform: "uppercase" as const }}>
            Prompt tiers
          </h3>
          <div style={{ border: "1px solid rgba(255,255,255,0.3)", marginBottom: 32 }}>
            {TIERS.map((t, i) => (
              <div key={t.tier} style={{ display: "grid", gridTemplateColumns: "140px 1fr", borderBottom: i < 3 ? "1px solid rgba(255,255,255,0.15)" : "none" }}>
                <div style={{ padding: "14px 16px", borderRight: "1px solid rgba(255,255,255,0.3)", borderLeft: `3px solid ${t.color}`, background: "rgba(0,0,0,0.1)" }}>
                  <div style={{ ...MONO, fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", color: t.color, marginBottom: 2 }}>{t.tier}</div>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>{t.label}</div>
                  <div style={{ ...MONO, fontSize: 10, color: "rgba(255,255,255,0.4)", marginTop: 4 }}>{t.n} prompts</div>
                </div>
                <div style={{ padding: "14px 18px", fontSize: 13, color: "rgba(255,255,255,0.75)", lineHeight: 1.6, display: "flex", alignItems: "center" }}>
                  {t.desc}
                </div>
              </div>
            ))}
          </div>

          {/* Execution pipeline — ruled numbered list */}
          <h3 style={{ ...MONO, fontSize: 11, fontWeight: 700, letterSpacing: "0.06em", textTransform: "uppercase" as const, color: "rgba(255,255,255,0.6)", marginBottom: 12 }}>
            Execution pipeline
          </h3>
          <div style={{ border: "1px solid rgba(255,255,255,0.3)", marginBottom: 24 }}>
            {PIPELINE.map((s, i) => (
              <div key={s.step} style={{ display: "grid", gridTemplateColumns: "48px 1fr", borderBottom: i < 3 ? "1px solid rgba(255,255,255,0.15)" : "none" }}>
                <div style={{ padding: "16px", borderRight: "1px solid rgba(255,255,255,0.3)", background: "rgba(0,0,0,0.1)", display: "flex", alignItems: "flex-start", justifyContent: "center", paddingTop: 18 }}>
                  <span style={{ ...MONO, fontSize: 13, fontWeight: 800, color: "#facc15" }}>{s.step}</span>
                </div>
                <div style={{ padding: "16px 20px" }}>
                  <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 4 }}>{s.title}</div>
                  <div style={{ color: "rgba(255,255,255,0.65)", fontSize: 13, lineHeight: 1.6 }}>{s.desc}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Scoring note */}
          <div style={{ borderLeft: "3px solid rgba(255,255,255,0.3)", paddingLeft: 16, fontSize: 13, color: "rgba(255,255,255,0.6)", lineHeight: 1.7 }}>
            <strong style={{ color: "white" }}>Note on scoring:</strong>{" "}
            &ldquo;Success&rdquo; means the output produced a valid, executable 3D part — not that the part
            matches the prompt geometrically. A cube generated for a prompt asking for a cylinder
            would score ✓. Geometric accuracy metrics are planned but not yet computed.
          </div>
        </section>

        {/* ── Per-model details ── */}
        <section style={{ marginBottom: 64 }}>
          <h2 style={{ fontSize: 22, fontWeight: 700, marginBottom: 24, letterSpacing: "-0.02em" }}>Per-model details</h2>
          <div style={{ border: "1px solid rgba(255,255,255,0.3)" }}>
            {MODEL_DETAILS.map((m, i) => (
              <div key={m.name} style={{ borderBottom: i < MODEL_DETAILS.length - 1 ? "1px solid rgba(255,255,255,0.15)" : "none" }}>
                <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: 16, padding: "16px 20px", borderBottom: "1px solid rgba(255,255,255,0.08)", background: "rgba(0,0,0,0.1)" }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 15 }}>{m.name}</div>
                    <div style={{ ...MONO, fontSize: 11, color: "rgba(255,255,255,0.5)", marginTop: 2 }}>{m.tag} · {m.output}</div>
                  </div>
                  <div style={{ ...MONO, fontWeight: 800, fontSize: 16, color: "#4ade80", alignSelf: "center" }}>{m.score}</div>
                </div>
                <ul style={{ margin: 0, padding: "14px 20px 14px 32px", display: "flex", flexDirection: "column", gap: 6 }}>
                  {m.notes.map((note, j) => (
                    <li key={j} style={{ color: "rgba(255,255,255,0.65)", fontSize: 13, lineHeight: 1.6 }}>{note}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* ── Dynamic Evaluation ── */}
        <section style={{ marginBottom: 56 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
            <h2 style={{ fontSize: 22, fontWeight: 700, margin: 0, letterSpacing: "-0.02em" }}>Dynamic Evaluation</h2>
            <span style={{ ...MONO, fontSize: 10, fontWeight: 700, letterSpacing: "0.1em", padding: "3px 9px", border: "1px solid #facc15", color: "#facc15" }}>
              COMING SOON
            </span>
          </div>
          <p style={{ color: "rgba(255,255,255,0.65)", fontSize: 15, lineHeight: 1.7, marginBottom: 20 }}>
            The <Link href="/try" style={{ color: "#facc15", textDecoration: "none" }}>Try</Link> page
            will let you submit any prompt and get results from all models in real time.
            The pipeline is identical to the static benchmark — same models, same execution engine, same scoring.
          </p>
          <div style={{ border: "1px solid rgba(255,255,255,0.3)" }}>
            {[
              { title: "Consent & storage", desc: "You will be asked whether your prompt and results can be saved to the public dataset. If yes, results appear in the Explore page for others to browse." },
              { title: "Rate limits", desc: "Anonymous users: 3 prompts/day. Free account (email sign-in): 20 prompts/day. No paid tier — this is a research tool." },
              { title: "Latency", desc: "Expect 5–20s depending on the model. Academic models (self-hosted) may take longer. Results stream per-model as they complete." },
            ].map((item, i) => (
              <div key={item.title} style={{ display: "grid", gridTemplateColumns: "160px 1fr", borderBottom: i < 2 ? "1px solid rgba(255,255,255,0.15)" : "none" }}>
                <div style={{ padding: "16px 18px", borderRight: "1px solid rgba(255,255,255,0.3)", background: "rgba(0,0,0,0.1)", fontWeight: 600, fontSize: 13, display: "flex", alignItems: "center" }}>
                  {item.title}
                </div>
                <div style={{ padding: "16px 20px", fontSize: 13, color: "rgba(255,255,255,0.65)", lineHeight: 1.6 }}>
                  {item.desc}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Contact */}
        <p style={{ color: "rgba(255,255,255,0.5)", fontSize: 13, lineHeight: 1.7, borderTop: "1px solid rgba(255,255,255,0.15)", paddingTop: 24 }}>
          Questions about methodology or want to submit a model?{" "}
          <a href="mailto:contact@cadarena.dev" style={{ color: "#facc15", textDecoration: "none" }}>
            contact@cadarena.dev
          </a>
        </p>

      </div>
    </div>
  );
}
