import Link from "next/link";

const PRELIMINARY_RESULTS = [
  {
    rank: 1,
    model: "Claude Opus 4.6",
    type: "baseline" as const,
    stl_pct: 80,
    syntax_pct: 100,
    latency: "8.6s",
    prompts: "16 / 20",
    note: "Best syntax validity. Fastest LLM.",
  },
  {
    rank: 2,
    model: "Zoo ML-ephant",
    type: "commercial" as const,
    stl_pct: 80,
    syntax_pct: 80,
    latency: "64.8s",
    prompts: "16 / 20",
    note: "Matches Claude quality. Slow API.",
  },
  {
    rank: 3,
    model: "GPT-5",
    type: "baseline" as const,
    stl_pct: 70,
    syntax_pct: 70,
    latency: "23.3s",
    prompts: "14 / 20",
    note: "Drops on harder tiers.",
  },
  {
    rank: 4,
    model: "Gemini 2.5 Flash",
    type: "baseline" as const,
    stl_pct: 35,
    syntax_pct: 35,
    latency: "—",
    prompts: "7 / 20",
    note: "Rate-limited (free tier). Not model quality.",
  },
];

const MODELS = [
  // Academic
  {
    name: "Text2CAD",
    year: "2024",
    venue: "NeurIPS Spotlight",
    type: "academic" as const,
    input: "Text",
    output: "CAD sequences",
    note: "170K models, 4 abstraction levels",
  },
  {
    name: "FlexCAD",
    year: "2025",
    venue: "ICLR",
    type: "academic" as const,
    input: "Text / multi-cond",
    output: "CAD sequences",
    note: "Unified controllable generation",
  },
  {
    name: "CAD-Coder",
    year: "2025",
    venue: "arXiv",
    type: "academic" as const,
    input: "Text",
    output: "CAD code",
    note: "Chain-of-thought + geometric reward RL",
  },
  {
    name: "Text-to-CadQuery",
    year: "2025",
    venue: "arXiv",
    type: "academic" as const,
    input: "Text",
    output: "CadQuery Python",
    note: "Self-correction: 53% → 85% exec success",
  },
  {
    name: "CADFusion",
    year: "2025",
    venue: "arXiv",
    type: "academic" as const,
    input: "Text + visual feedback",
    output: "CadQuery",
    note: "Iterative visual refinement loop",
  },
  {
    name: "CAD-GPT",
    year: "2025",
    venue: "arXiv",
    type: "academic" as const,
    input: "Text + image",
    output: "CAD sequences",
    note: "Spatial reasoning multimodal LLM",
  },
  {
    name: "DeepCAD",
    year: "2021",
    venue: "ICCV",
    type: "academic" as const,
    input: "Unconditional",
    output: "CAD sequences",
    note: "Foundational baseline — 178K models",
  },
  // Commercial
  {
    name: "Zoo / ML-ephant",
    year: "2025",
    venue: "zoo.dev",
    type: "commercial" as const,
    input: "Text",
    output: "STEP / STL / OBJ",
    note: "$30M+ funded, public API",
  },
  {
    name: "AdamCAD",
    year: "2025",
    venue: "YC W25",
    type: "commercial" as const,
    input: "Text",
    output: "STEP",
    note: "$4.1M seed, mech. engineering focus",
  },
  {
    name: "CADGPT",
    year: "2025",
    venue: "cadgpt.ai",
    type: "commercial" as const,
    input: "Text",
    output: "STEP",
    note: "Commercial text-to-CAD API",
  },
  // LLM baselines
  {
    name: "GPT-4o (zero-shot)",
    year: "2024",
    venue: "OpenAI",
    type: "baseline" as const,
    input: "Text",
    output: "OpenSCAD / CadQuery",
    note: "93% invalid rate (Text2CAD eval)",
  },
  {
    name: "Claude Sonnet (zero-shot)",
    year: "2025",
    venue: "Anthropic",
    type: "baseline" as const,
    input: "Text",
    output: "CadQuery",
    note: "Strong code model — untested on CAD",
  },
  {
    name: "Gemini 2.0 (zero-shot)",
    year: "2025",
    venue: "Google",
    type: "baseline" as const,
    input: "Text",
    output: "CadQuery",
    note: "85% compile rate on CADPrompt",
  },
];

const PROMPT_TIERS = [
  {
    tier: "Tier 1",
    label: "Simple Primitives",
    expected: "~90%+ success",
    color: "#4ade80",
    examples: [
      "A cube 20 × 20 × 20 mm",
      "A cylinder 10 mm diameter, 30 mm tall",
      "A hollow sphere, outer radius 20 mm, wall 2 mm",
    ],
  },
  {
    tier: "Tier 2",
    label: "Single Part with Features",
    expected: "~60–80% success",
    color: "#60a5fa",
    examples: [
      "A rectangular plate 50 × 30 × 5 mm with a centered hole 8 mm diameter",
      "An L-shaped bracket, 40 mm arms, 5 mm thick, 30 mm tall",
      "A hex bolt head 10 mm across flats, M6 thread, 20 mm shaft",
    ],
  },
  {
    tier: "Tier 3",
    label: "Multi-Feature Parts",
    expected: "~30–50% success",
    color: "#fb923c",
    examples: [
      "A flanged shaft with 3 equally-spaced M4 bolt holes on the flange",
      "A box with a snap-fit lid, 50 × 40 × 30 mm",
      "A spur gear: 20 teeth, module 2, 10 mm thick, 8 mm center bore",
    ],
  },
  {
    tier: "Tier 4",
    label: "Complex Functional Parts",
    expected: "~5–20% success",
    color: "#f87171",
    examples: [
      "A parametric living hinge, 100 mm span, 0.3 mm flex zone",
      "An S-curve pipe fitting, 15 mm inner diameter, 45° bend",
      "A 3-part snap-fit assembly: housing, PCB carrier, and lid",
    ],
  },
];

const TYPE_STYLES = {
  academic: {
    bg: "var(--tag-academic)",
    color: "var(--tag-academic-text)",
    label: "Academic",
  },
  commercial: {
    bg: "var(--tag-commercial)",
    color: "var(--tag-commercial-text)",
    label: "Commercial",
  },
  baseline: {
    bg: "var(--tag-baseline)",
    color: "var(--tag-baseline-text)",
    label: "LLM Baseline",
  },
};

export default function Home() {
  const academicCount = MODELS.filter((m) => m.type === "academic").length;
  const commercialCount = MODELS.filter((m) => m.type === "commercial").length;
  const baselineCount = MODELS.filter((m) => m.type === "baseline").length;

  return (
    <div style={{ background: "var(--background)", minHeight: "100vh" }}>
      {/* Nav */}
      <nav
        style={{
          borderBottom: "1px solid var(--border)",
          position: "sticky",
          top: 0,
          zIndex: 50,
          backdropFilter: "blur(12px)",
          background: "rgba(8, 12, 20, 0.85)",
        }}
      >
        <div
          style={{
            maxWidth: 1200,
            margin: "0 auto",
            padding: "0 24px",
            height: 56,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span
              style={{
                fontFamily: "var(--font-geist-mono), monospace",
                fontSize: 18,
                fontWeight: 700,
                color: "var(--accent)",
                letterSpacing: "-0.02em",
              }}
            >
              CAD Arena
            </span>
            <span
              style={{
                fontSize: 11,
                padding: "2px 8px",
                borderRadius: 4,
                background: "rgba(59, 130, 246, 0.15)",
                color: "var(--accent)",
                fontWeight: 600,
                letterSpacing: "0.05em",
              }}
            >
              BETA
            </span>
          </div>
          <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
            {["Models", "Benchmark", "Paper"].map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                style={{
                  color: "var(--muted)",
                  textDecoration: "none",
                  fontSize: 14,
                  fontWeight: 500,
                }}
              >
                {item}
              </a>
            ))}
            <a
              href="https://github.com"
              style={{
                color: "var(--muted)",
                textDecoration: "none",
                fontSize: 14,
                fontWeight: 500,
              }}
            >
              GitHub →
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section
        className="blueprint-bg"
        style={{
          padding: "100px 24px 80px",
          textAlign: "center",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Glow */}
        <div
          style={{
            position: "absolute",
            top: "40%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 600,
            height: 400,
            background:
              "radial-gradient(ellipse, rgba(59, 130, 246, 0.08) 0%, transparent 70%)",
            pointerEvents: "none",
          }}
        />

        <div style={{ maxWidth: 800, margin: "0 auto", position: "relative" }}>
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              fontSize: 13,
              color: "var(--accent)",
              fontWeight: 600,
              letterSpacing: "0.08em",
              marginBottom: 28,
              padding: "6px 14px",
              border: "1px solid rgba(59, 130, 246, 0.3)",
              borderRadius: 20,
              background: "rgba(59, 130, 246, 0.07)",
            }}
          >
            <span
              style={{
                width: 6,
                height: 6,
                borderRadius: "50%",
                background: "var(--accent)",
                display: "inline-block",
              }}
            />
            OPEN RESEARCH · LAUNCHING 2026
          </div>

          <h1
            style={{
              fontSize: "clamp(36px, 6vw, 64px)",
              fontWeight: 800,
              lineHeight: 1.1,
              marginBottom: 24,
              letterSpacing: "-0.03em",
              color: "var(--foreground)",
            }}
          >
            The first open benchmark
            <br />
            <span style={{ color: "var(--accent)" }}>
              for AI-generated parametric CAD
            </span>
          </h1>

          <p
            style={{
              fontSize: 19,
              color: "var(--muted)",
              maxWidth: 600,
              margin: "0 auto 40px",
              lineHeight: 1.7,
            }}
          >
            Enter a text prompt. Compare outputs from{" "}
            <strong style={{ color: "var(--foreground)" }}>13+ models</strong>{" "}
            — academic and commercial — side by side. Vote for the best result.
            Watch the leaderboard evolve.
          </p>

          <div
            style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}
          >
            <a
              href="#models"
              style={{
                background: "var(--accent)",
                color: "#fff",
                padding: "12px 28px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 700,
                fontSize: 15,
              }}
            >
              Browse Models →
            </a>
            <a
              href="#benchmark"
              style={{
                border: "1px solid var(--border)",
                color: "var(--foreground)",
                padding: "12px 28px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 600,
                fontSize: 15,
                background: "var(--card)",
              }}
            >
              See the Benchmark
            </a>
          </div>
        </div>
      </section>

      {/* Stats bar */}
      <div
        style={{
          borderTop: "1px solid var(--border)",
          borderBottom: "1px solid var(--border)",
          background: "var(--card)",
        }}
      >
        <div
          style={{
            maxWidth: 1000,
            margin: "0 auto",
            padding: "0 24px",
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            textAlign: "center",
          }}
        >
          {[
            { value: "173", label: "Papers analyzed" },
            { value: "13+", label: "Models compared" },
            { value: "~200", label: "Benchmark prompts" },
            { value: "4", label: "Difficulty tiers" },
          ].map((stat, i) => (
            <div
              key={i}
              style={{
                padding: "28px 16px",
                borderRight:
                  i < 3 ? "1px solid var(--border)" : "none",
              }}
            >
              <div
                style={{
                  fontSize: 32,
                  fontWeight: 800,
                  color: "var(--accent)",
                  fontFamily: "var(--font-geist-mono), monospace",
                  lineHeight: 1,
                  marginBottom: 6,
                }}
              >
                {stat.value}
              </div>
              <div style={{ fontSize: 13, color: "var(--muted)", fontWeight: 500 }}>
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* How it works */}
      <section style={{ padding: "80px 24px" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: 32,
              fontWeight: 700,
              marginBottom: 8,
              letterSpacing: "-0.02em",
            }}
          >
            How it works
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 48, fontSize: 16 }}>
            Inspired by{" "}
            <a
              href="https://chat.lmsys.org"
              style={{ color: "var(--accent)", textDecoration: "none" }}
            >
              Chatbot Arena
            </a>{" "}
            and{" "}
            <a
              href="https://huggingface.co/spaces/dylanebert/3d-arena"
              style={{ color: "var(--accent)", textDecoration: "none" }}
            >
              3D Arena
            </a>{" "}
            — but for engineering-grade parametric CAD.
          </p>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(3, 1fr)",
              gap: 24,
            }}
          >
            {[
              {
                step: "01",
                title: "Enter a text prompt",
                desc: "Describe a mechanical part in plain English. From simple primitives to complex functional assemblies.",
                icon: "✏️",
              },
              {
                step: "02",
                title: "Compare model outputs",
                desc: "See outputs from 13+ models rendered side-by-side in 3D. Inspect geometry, download STEP files, view the generated code.",
                icon: "⚙️",
              },
              {
                step: "03",
                title: "Vote + see metrics",
                desc: "Cast a pairwise vote. Results feed into Elo-based rankings. Automated metrics (validity, Chamfer distance, VLM score) run in parallel.",
                icon: "📊",
              },
            ].map((step) => (
              <div
                key={step.step}
                style={{
                  background: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: 12,
                  padding: 32,
                }}
              >
                <div
                  style={{
                    fontFamily: "var(--font-geist-mono), monospace",
                    fontSize: 12,
                    color: "var(--accent)",
                    fontWeight: 700,
                    letterSpacing: "0.1em",
                    marginBottom: 16,
                  }}
                >
                  STEP {step.step}
                </div>
                <div style={{ fontSize: 28, marginBottom: 14 }}>{step.icon}</div>
                <h3
                  style={{
                    fontSize: 18,
                    fontWeight: 700,
                    marginBottom: 10,
                    letterSpacing: "-0.01em",
                  }}
                >
                  {step.title}
                </h3>
                <p style={{ color: "var(--muted)", fontSize: 14, lineHeight: 1.7 }}>
                  {step.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Models */}
      <section
        id="models"
        style={{
          padding: "80px 24px",
          borderTop: "1px solid var(--border)",
        }}
      >
        <div style={{ maxWidth: 1200, margin: "0 auto" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-end",
              marginBottom: 48,
              flexWrap: "wrap",
              gap: 16,
            }}
          >
            <div>
              <h2
                style={{
                  fontSize: 32,
                  fontWeight: 700,
                  marginBottom: 8,
                  letterSpacing: "-0.02em",
                }}
              >
                Models included
              </h2>
              <p style={{ color: "var(--muted)", fontSize: 16 }}>
                {academicCount} academic &nbsp;·&nbsp; {commercialCount}{" "}
                commercial &nbsp;·&nbsp; {baselineCount} LLM baselines
              </p>
            </div>
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
              {(["academic", "commercial", "baseline"] as const).map((type) => {
                const s = TYPE_STYLES[type];
                return (
                  <span
                    key={type}
                    style={{
                      fontSize: 12,
                      padding: "4px 10px",
                      borderRadius: 6,
                      background: s.bg,
                      color: s.color,
                      fontWeight: 600,
                    }}
                  >
                    {s.label}
                  </span>
                );
              })}
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
              gap: 16,
            }}
          >
            {MODELS.map((model) => {
              const s = TYPE_STYLES[model.type];
              return (
                <div
                  key={model.name}
                  style={{
                    background: "var(--card)",
                    border: "1px solid var(--border)",
                    borderRadius: 10,
                    padding: 22,
                    transition: "border-color 0.2s",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      marginBottom: 12,
                    }}
                  >
                    <div>
                      <div
                        style={{
                          fontWeight: 700,
                          fontSize: 15,
                          marginBottom: 2,
                          letterSpacing: "-0.01em",
                        }}
                      >
                        {model.name}
                      </div>
                      <div
                        style={{
                          fontSize: 12,
                          color: "var(--muted)",
                          fontFamily: "var(--font-geist-mono), monospace",
                        }}
                      >
                        {model.venue} · {model.year}
                      </div>
                    </div>
                    <span
                      style={{
                        fontSize: 11,
                        padding: "3px 8px",
                        borderRadius: 5,
                        background: s.bg,
                        color: s.color,
                        fontWeight: 600,
                        whiteSpace: "nowrap",
                        letterSpacing: "0.03em",
                      }}
                    >
                      {s.label}
                    </span>
                  </div>

                  <div
                    style={{
                      display: "flex",
                      gap: 8,
                      marginBottom: 12,
                      flexWrap: "wrap",
                    }}
                  >
                    <span
                      style={{
                        fontSize: 11,
                        padding: "2px 8px",
                        borderRadius: 4,
                        background: "var(--card-hover)",
                        color: "var(--muted)",
                        border: "1px solid var(--border)",
                      }}
                    >
                      IN: {model.input}
                    </span>
                    <span
                      style={{
                        fontSize: 11,
                        padding: "2px 8px",
                        borderRadius: 4,
                        background: "var(--card-hover)",
                        color: "var(--muted)",
                        border: "1px solid var(--border)",
                      }}
                    >
                      OUT: {model.output}
                    </span>
                  </div>

                  <p
                    style={{
                      fontSize: 12,
                      color: "var(--muted)",
                      lineHeight: 1.6,
                      margin: 0,
                    }}
                  >
                    {model.note}
                  </p>
                </div>
              );
            })}
          </div>

          <div
            style={{
              marginTop: 32,
              padding: 20,
              background: "rgba(59, 130, 246, 0.06)",
              border: "1px solid rgba(59, 130, 246, 0.2)",
              borderRadius: 10,
              fontSize: 14,
              color: "var(--muted)",
            }}
          >
            <strong style={{ color: "var(--foreground)" }}>Open submissions.</strong>{" "}
            Once launched, any model can be submitted for evaluation. If you
            have a text-to-CAD model and want it on the leaderboard,{" "}
            <a
              href="mailto:contact@cadarena.ai"
              style={{ color: "var(--accent)", textDecoration: "none" }}
            >
              get in touch
            </a>
            .
          </div>
        </div>
      </section>

      {/* Benchmark prompts */}
      <section
        id="benchmark"
        style={{
          padding: "80px 24px",
          borderTop: "1px solid var(--border)",
        }}
      >
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: 32,
              fontWeight: 700,
              marginBottom: 8,
              letterSpacing: "-0.02em",
            }}
          >
            Benchmark prompts
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 48, fontSize: 16 }}>
            ~200 prompts across 4 difficulty tiers. Fixed set for reproducible
            evaluation. Models are scored on validity rate, Chamfer distance,
            and VLM-judged prompt adherence.
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 20 }}>
            {PROMPT_TIERS.map((tier) => (
              <div
                key={tier.tier}
                style={{
                  background: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: 12,
                  padding: 28,
                  borderLeft: `3px solid ${tier.color}`,
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    marginBottom: 16,
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontFamily: "var(--font-geist-mono), monospace",
                        fontSize: 12,
                        color: tier.color,
                        fontWeight: 700,
                        letterSpacing: "0.08em",
                        marginBottom: 4,
                      }}
                    >
                      {tier.tier}
                    </div>
                    <div style={{ fontWeight: 700, fontSize: 16 }}>
                      {tier.label}
                    </div>
                  </div>
                  <span
                    style={{
                      fontSize: 11,
                      padding: "3px 8px",
                      borderRadius: 5,
                      background: `${tier.color}18`,
                      color: tier.color,
                      fontWeight: 600,
                      whiteSpace: "nowrap",
                    }}
                  >
                    {tier.expected}
                  </span>
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {tier.examples.map((ex, i) => (
                    <div
                      key={i}
                      style={{
                        background: "var(--background)",
                        border: "1px solid var(--border)",
                        borderRadius: 6,
                        padding: "8px 12px",
                        fontFamily: "var(--font-geist-mono), monospace",
                        fontSize: 12,
                        color: "var(--muted)",
                        lineHeight: 1.5,
                      }}
                    >
                      &ldquo;{ex}&rdquo;
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Preliminary Results */}
      <section
        style={{
          padding: "80px 24px",
          borderTop: "1px solid var(--border)",
        }}
      >
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: 8, flexWrap: "wrap", gap: 12 }}>
            <h2 style={{ fontSize: 32, fontWeight: 700, letterSpacing: "-0.02em", margin: 0 }}>
              Preliminary results
            </h2>
            <span style={{
              fontSize: 11, padding: "4px 10px", borderRadius: 5,
              background: "rgba(251, 191, 36, 0.12)", color: "#fbbf24",
              fontWeight: 700, letterSpacing: "0.06em",
            }}>
              EARLY DATA · 2026-03-03
            </span>
          </div>
          <p style={{ color: "var(--muted)", marginBottom: 40, fontSize: 16 }}>
            20 prompts across 4 difficulty tiers. Metric: % of prompts that produced
            a valid, executable 3D part. Full leaderboard launching soon.
          </p>

          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
              <thead>
                <tr style={{ borderBottom: "1px solid var(--border)" }}>
                  {["Rank", "Model", "Type", "Valid STL", "Syntax OK", "Avg Latency", "Prompts passed", "Notes"].map((h) => (
                    <th key={h} style={{
                      textAlign: "left", padding: "10px 14px",
                      color: "var(--muted)", fontWeight: 600,
                      fontFamily: "var(--font-geist-mono), monospace", fontSize: 11,
                      letterSpacing: "0.06em", whiteSpace: "nowrap",
                    }}>{h.toUpperCase()}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {PRELIMINARY_RESULTS.map((row) => {
                  const s = TYPE_STYLES[row.type];
                  const barColor = row.stl_pct >= 75 ? "#4ade80" : row.stl_pct >= 50 ? "#fbbf24" : "#f87171";
                  return (
                    <tr key={row.model} style={{ borderBottom: "1px solid var(--border)" }}>
                      <td style={{ padding: "14px 14px", color: "var(--muted)", fontFamily: "var(--font-geist-mono), monospace" }}>
                        #{row.rank}
                      </td>
                      <td style={{ padding: "14px 14px", fontWeight: 700 }}>{row.model}</td>
                      <td style={{ padding: "14px 14px" }}>
                        <span style={{ fontSize: 11, padding: "3px 8px", borderRadius: 5, background: s.bg, color: s.color, fontWeight: 600 }}>
                          {s.label}
                        </span>
                      </td>
                      <td style={{ padding: "14px 14px" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                          <div style={{ width: 60, height: 6, background: "var(--border)", borderRadius: 3, overflow: "hidden" }}>
                            <div style={{ width: `${row.stl_pct}%`, height: "100%", background: barColor, borderRadius: 3 }} />
                          </div>
                          <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 13, color: barColor, fontWeight: 700 }}>
                            {row.stl_pct}%
                          </span>
                        </div>
                      </td>
                      <td style={{ padding: "14px 14px", fontFamily: "var(--font-geist-mono), monospace", color: "var(--muted)" }}>
                        {row.syntax_pct}%
                      </td>
                      <td style={{ padding: "14px 14px", fontFamily: "var(--font-geist-mono), monospace", color: "var(--muted)" }}>
                        {row.latency}
                      </td>
                      <td style={{ padding: "14px 14px", fontFamily: "var(--font-geist-mono), monospace", color: "var(--muted)" }}>
                        {row.prompts}
                      </td>
                      <td style={{ padding: "14px 14px", color: "var(--muted)", fontSize: 13 }}>{row.note}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <p style={{ marginTop: 20, fontSize: 13, color: "var(--muted)" }}>
            These are <strong style={{ color: "var(--foreground)" }}>API-only baseline results</strong> on 20 prompts.
            Full benchmark (200 prompts, 13+ models including academic open-source models)
            is in progress. Gemini result reflects free-tier rate limiting, not model quality.
          </p>
        </div>
      </section>

      {/* Why it matters */}
      <section
        style={{
          padding: "80px 24px",
          borderTop: "1px solid var(--border)",
          background: "var(--card)",
        }}
      >
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: 32,
              fontWeight: 700,
              marginBottom: 8,
              letterSpacing: "-0.02em",
            }}
          >
            Why this doesn&apos;t exist yet
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 48, fontSize: 16 }}>
            The 2025 survey{" "}
            <em>Large Language Models for Computer-Aided Design</em> explicitly
            identifies this as the field&apos;s most critical gap.
          </p>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(2, 1fr)",
              gap: 20,
            }}
          >
            {[
              {
                title: "No cross-model comparison",
                desc: "Sequence-based (Text2CAD), code-based (CAD-Coder), and B-rep direct (BrepGen) models are evaluated on different benchmarks with different metrics. You can't compare results across papers.",
              },
              {
                title: "Academic ≠ commercial",
                desc: "Commercial tools like Zoo and AdamCAD are never included in academic benchmark tables. Academic models are never in commercial tool comparisons. Nobody has done both.",
              },
              {
                title: "No living leaderboard",
                desc: "Every benchmark is a static snapshot tied to a paper. There's no place where new models submit and get ranked continuously — no SWE-bench equivalent for CAD.",
              },
              {
                title: "No agreed-upon metrics",
                desc: "Unlike image generation (FID, CLIP score) or code (pass@k), CAD has no community-consensus quality metric. Papers pick different metrics, making progress hard to track.",
              },
            ].map((item) => (
              <div
                key={item.title}
                style={{
                  background: "var(--background)",
                  border: "1px solid var(--border)",
                  borderRadius: 10,
                  padding: 28,
                }}
              >
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: "var(--accent)",
                    marginBottom: 16,
                  }}
                />
                <h3 style={{ fontWeight: 700, fontSize: 16, marginBottom: 10 }}>
                  {item.title}
                </h3>
                <p style={{ color: "var(--muted)", fontSize: 14, lineHeight: 1.7, margin: 0 }}>
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Paper / CTA */}
      <section
        id="paper"
        style={{
          padding: "80px 24px",
          borderTop: "1px solid var(--border)",
          textAlign: "center",
        }}
      >
        <div style={{ maxWidth: 640, margin: "0 auto" }}>
          <div
            style={{
              fontFamily: "var(--font-geist-mono), monospace",
              fontSize: 12,
              color: "var(--accent)",
              fontWeight: 700,
              letterSpacing: "0.1em",
              marginBottom: 16,
            }}
          >
            PAPER IN PREPARATION
          </div>
          <h2
            style={{
              fontSize: 32,
              fontWeight: 700,
              marginBottom: 16,
              letterSpacing: "-0.02em",
            }}
          >
            Accompanying publication
          </h2>
          <p
            style={{
              color: "var(--muted)",
              marginBottom: 40,
              fontSize: 16,
              lineHeight: 1.7,
            }}
          >
            We are preparing a benchmark paper targeting{" "}
            <strong style={{ color: "var(--foreground)" }}>
              NeurIPS 2026 Datasets &amp; Benchmarks
            </strong>
            . The paper will evaluate all listed models on the fixed benchmark,
            propose standardized metrics, and describe the arena platform.
          </p>

          <div
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 12,
              padding: 32,
              marginBottom: 32,
            }}
          >
            <p
              style={{
                fontSize: 14,
                color: "var(--muted)",
                marginBottom: 20,
              }}
            >
              Get notified when the leaderboard launches and the preprint drops.
            </p>
            <a
              href="mailto:contact@cadarena.ai"
              style={{
                display: "inline-block",
                background: "var(--accent)",
                color: "#fff",
                padding: "12px 32px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 700,
                fontSize: 15,
              }}
            >
              contact@cadarena.ai →
            </a>
          </div>

          <p style={{ fontSize: 13, color: "var(--muted)" }}>
            Are you working on a text-to-CAD model and want it on the
            leaderboard? We want to hear from you.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer
        style={{
          borderTop: "1px solid var(--border)",
          padding: "32px 24px",
        }}
      >
        <div
          style={{
            maxWidth: 1000,
            margin: "0 auto",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: 12,
          }}
        >
          <span
            style={{
              fontFamily: "var(--font-geist-mono), monospace",
              fontWeight: 700,
              color: "var(--accent)",
              fontSize: 14,
            }}
          >
            CAD Arena
          </span>
          <div style={{ display: "flex", gap: 24, fontSize: 13, color: "var(--muted)" }}>
            <span>Open research · 2026</span>
            <a
              href="https://github.com"
              style={{ color: "var(--muted)", textDecoration: "none" }}
            >
              GitHub
            </a>
            <a
              href="mailto:contact@cadarena.ai"
              style={{ color: "var(--muted)", textDecoration: "none" }}
            >
              Contact
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
