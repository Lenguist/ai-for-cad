import Link from "next/link";

const PRELIMINARY_RESULTS = [
  {
    rank: 1,
    model: "Claude Opus 4.6",
    type: "baseline" as const,
    stl_pct: 90,
    syntax_pct: 100,
    latency: "6.9s",
    prompts: "19 / 20",
    note: "Perfect T1–T3. Only tier 4 failures.",
  },
  {
    rank: 1,
    model: "Zoo ML-ephant",
    type: "commercial" as const,
    stl_pct: 95,
    syntax_pct: 95,
    latency: "11.1s",
    prompts: "19 / 20",
    note: "Tied with Claude. Returns native geometry.",
  },
  {
    rank: 3,
    model: "Gemini 2.5 Flash",
    type: "baseline" as const,
    stl_pct: 70,
    syntax_pct: 100,
    latency: "3.1s",
    prompts: "14 / 20",
    note: "Fastest. Hallucinates methods at T4.",
  },
  {
    rank: 4,
    model: "GPT-5",
    type: "baseline" as const,
    stl_pct: 60,
    syntax_pct: 60,
    latency: "16.1s",
    prompts: "12 / 20",
    note: "Token truncation kills all T4 prompts.",
  },
];


const PROMPT_TIERS = [
  {
    tier: "Tier 1",
    label: "Simple Primitives",
    color: "#4ade80",   // bright lime — pops on blue
    examples: [
      "A cube 20 × 20 × 20 mm",
      "A cylinder 10 mm diameter, 30 mm tall",
      "A hollow sphere, outer radius 20 mm, wall 2 mm",
    ],
  },
  {
    tier: "Tier 2",
    label: "Single Part with Features",
    color: "#facc15",   // yellow — high contrast on blue
    examples: [
      "A rectangular plate 50 × 30 × 5 mm with a centered hole 8 mm diameter",
      "An L-shaped bracket, 40 mm arms, 5 mm thick, 30 mm tall",
      "A hex bolt head 10 mm across flats, M6 thread, 20 mm shaft",
    ],
  },
  {
    tier: "Tier 3",
    label: "Multi-Feature Parts",
    color: "#fb923c",   // bright orange
    examples: [
      "A flanged shaft with 3 equally-spaced M4 bolt holes on the flange",
      "A box with a snap-fit lid, 50 × 40 × 30 mm",
      "A spur gear: 20 teeth, module 2, 10 mm thick, 8 mm center bore",
    ],
  },
  {
    tier: "Tier 4",
    label: "Complex Functional Parts",
    color: "#f87171",   // light red/coral
    examples: [
      "A parametric living hinge, 100 mm span, 0.3 mm flex zone",
      "An S-curve pipe fitting, 15 mm inner diameter, 45° bend",
      "A 3-part snap-fit assembly: housing, PCB carrier, and lid",
    ],
  },
];


export default function Home() {
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
          background: "rgba(55, 105, 160, 0.92)",
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
                background: "rgba(255,255,255,0.12)",
                color: "var(--accent)",
                fontWeight: 600,
                letterSpacing: "0.05em",
              }}
            >
              BETA
            </span>
          </div>
          <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
            <Link href="/results" style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}>Results</Link>
            <Link href="/try" style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}>Try</Link>
            <Link href="/methods" style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}>Methods</Link>
            <a
              href="https://github.com/Lenguist/ai-for-cad"
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
              "radial-gradient(ellipse, rgba(255,255,255,0.08) 0%, transparent 70%)",
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
              border: "1px solid rgba(255,255,255,0.35)",
              borderRadius: 20,
              background: "rgba(255,255,255,0.1)",
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
            Compare outputs from{" "}
            <strong style={{ color: "var(--foreground)" }}>LLM baselines, academic, and commercial models</strong>{" "}
            — side by side — on a fixed set of 20 curated prompts across 4 difficulty tiers.
          </p>

          <div
            style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}
          >
            <a
              href="#models"
              style={{
                background: "rgba(255,255,255,0.9)",
                color: "#3568a0",
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
            { value: "5", label: "Models tested" },
            { value: "20", label: "Benchmark prompts" },
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
      <section className="blueprint-grid" style={{ padding: "80px 24px", borderTop: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" }}>
            How it works
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 40, fontSize: 16 }}>
            Inspired by{" "}
            <a href="https://chat.lmsys.org" style={{ color: "var(--accent)", textDecoration: "none" }}>Chatbot Arena</a>{" "}
            and{" "}
            <a href="https://huggingface.co/spaces/dylanebert/3d-arena" style={{ color: "var(--accent)", textDecoration: "none" }}>3D Arena</a>{" "}
            — but for engineering-grade parametric CAD.
          </p>

          <div style={{ border: "1px solid rgba(255,255,255,0.3)", display: "grid", gridTemplateColumns: "repeat(3, 1fr)" }}>
            {[
              { step: "01", title: "Enter a text prompt", desc: "Describe a mechanical part in plain English. From simple primitives to complex functional assemblies." },
              { step: "02", title: "Compare model outputs", desc: "See outputs from multiple models rendered side-by-side in 3D. Inspect geometry, view the generated code, see where each model fails." },
              { step: "03", title: "Browse the results", desc: "Explore the full benchmark grid — 20 prompts × 5 models. Click any cell to see the 3D output, source code, and failure analysis." },
            ].map((step, i) => (
              <div
                key={step.step}
                style={{
                  padding: "32px 28px",
                  borderRight: i < 2 ? "1px solid rgba(255,255,255,0.3)" : "none",
                }}
              >
                <div style={{
                  fontFamily: "var(--font-geist-mono), monospace",
                  fontSize: 11,
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  color: "rgba(255,255,255,0.4)",
                  marginBottom: 20,
                }}>
                  STEP {step.step}
                </div>
                <h3 style={{ fontSize: 17, fontWeight: 700, marginBottom: 12, lineHeight: 1.3 }}>
                  {step.title}
                </h3>
                <p style={{ color: "var(--muted)", fontSize: 14, lineHeight: 1.7, margin: 0 }}>
                  {step.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Models */}
      <section id="models" className="blueprint-grid" style={{ padding: "80px 24px", borderTop: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" }}>
            Models tested
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 40, fontSize: 16 }}>
            5 models evaluated on the full 20-prompt benchmark. More being added.
          </p>

          <div style={{ border: "1px solid rgba(255,255,255,0.3)" }}>
            {/* header row */}
            <div style={{
              display: "grid",
              gridTemplateColumns: "1fr 2fr 100px",
              borderBottom: "1px solid rgba(255,255,255,0.3)",
              background: "rgba(0,0,0,0.15)",
            }}>
              {["MODEL", "NOTES", "VALID STLs"].map((h, i) => (
                <div key={h} style={{
                  padding: "10px 20px",
                  fontFamily: "var(--font-geist-mono), monospace",
                  fontSize: 10,
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  color: "rgba(255,255,255,0.4)",
                  borderRight: i < 2 ? "1px solid rgba(255,255,255,0.15)" : "none",
                  textAlign: i === 2 ? "right" : "left",
                }}>{h}</div>
              ))}
            </div>
            {[
              { name: "Claude Opus 4.6", type: "LLM Baseline · Anthropic", valid: 19, note: "Best overall. Perfect on T1–T3." },
              { name: "Zoo / ML-ephant", type: "Commercial · zoo.dev", valid: 19, note: "Native geometry engine. Returns KCL." },
              { name: "Text-to-CadQuery", type: "Academic · arXiv 2025", valid: 14, note: "Qwen 3B fine-tuned. Unit normalization quirk." },
              { name: "Gemini 2.5 Flash", type: "LLM Baseline · Google", valid: 14, note: "Fastest. Hallucinates methods on T4." },
              { name: "GPT-5", type: "LLM Baseline · OpenAI", valid: 12, note: "Token limit cuts off complex prompts." },
            ].map((m, i, arr) => (
              <div
                key={m.name}
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 2fr 100px",
                  borderBottom: i < arr.length - 1 ? "1px solid rgba(255,255,255,0.12)" : "none",
                }}
              >
                <div style={{ padding: "18px 20px", borderRight: "1px solid rgba(255,255,255,0.15)" }}>
                  <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 3 }}>{m.name}</div>
                  <div style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)" }}>{m.type}</div>
                </div>
                <div style={{ padding: "18px 20px", fontSize: 13, color: "var(--muted)", lineHeight: 1.6, borderRight: "1px solid rgba(255,255,255,0.15)", display: "flex", alignItems: "center" }}>
                  {m.note}
                </div>
                <div style={{ padding: "18px 20px", textAlign: "right", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "flex-end" }}>
                  <div style={{ fontFamily: "var(--font-geist-mono), monospace", fontWeight: 800, fontSize: 22, lineHeight: 1 }}>{m.valid}</div>
                  <div style={{ fontSize: 10, color: "var(--muted)", marginTop: 3, letterSpacing: "0.05em" }}>of 20</div>
                </div>
              </div>
            ))}
          </div>

          <div style={{ marginTop: 16, fontSize: 13, color: "var(--muted)" }}>
            Have a model to add?{" "}
            <a href="mailto:contact@cadarena.dev" style={{ color: "var(--accent)", textDecoration: "none" }}>contact@cadarena.dev</a>
          </div>
        </div>
      </section>

      {/* Benchmark prompts */}
      <section id="benchmark" className="blueprint-grid" style={{ padding: "80px 24px", borderTop: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" }}>
            Benchmark prompts
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 40, fontSize: 16 }}>
            20 prompts across 4 difficulty tiers. A prompt scores ✓ if it produces a valid, executable 3D part.
          </p>

          {/* 2-column table: tier label | examples. T4 on top (hardest). */}
          <div style={{ border: "1px solid rgba(255,255,255,0.3)" }}>
            {[...PROMPT_TIERS].reverse().map((tier, i) => (
              <div
                key={tier.tier}
                style={{
                  display: "grid",
                  gridTemplateColumns: "200px 1fr",
                  borderBottom: i < 3 ? "1px solid rgba(255,255,255,0.2)" : "none",
                }}
              >
                {/* Left column: tier label */}
                <div style={{
                  padding: "24px 20px",
                  borderRight: "1px solid rgba(255,255,255,0.3)",
                  borderLeft: `4px solid ${tier.color}`,
                  background: "rgba(0,0,0,0.1)",
                  display: "flex",
                  flexDirection: "column",
                  gap: 4,
                }}>
                  <div style={{
                    fontFamily: "var(--font-geist-mono), monospace",
                    fontSize: 11,
                    fontWeight: 700,
                    letterSpacing: "0.1em",
                    color: tier.color,
                  }}>
                    {tier.tier.toUpperCase()}
                  </div>
                  <div style={{ fontWeight: 700, fontSize: 14, lineHeight: 1.3 }}>
                    {tier.label}
                  </div>
                  <div style={{ fontFamily: "var(--font-geist-mono), monospace", fontSize: 11, color: "var(--muted)", marginTop: 4 }}>
                    5 prompts
                  </div>
                </div>
                {/* Right column: example prompts */}
                <div style={{ padding: "20px 24px", display: "flex", flexDirection: "column", gap: 0 }}>
                  {tier.examples.map((ex, j) => (
                    <div
                      key={j}
                      style={{
                        fontFamily: "var(--font-geist-mono), monospace",
                        fontSize: 12,
                        color: "rgba(255,255,255,0.8)",
                        padding: "10px 0",
                        borderBottom: j < tier.examples.length - 1 ? "1px solid rgba(255,255,255,0.08)" : "none",
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
              background: "rgba(255,255,255,0.1)", color: "rgba(255,255,255,0.75)",
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
                  const barColor = row.stl_pct >= 75 ? "rgba(255,255,255,0.95)" : row.stl_pct >= 50 ? "rgba(255,255,255,0.65)" : "rgba(255,255,255,0.4)";
                  const typeLabel = row.type === "commercial" ? "Commercial" : "LLM Baseline";
                  return (
                    <tr key={row.model} style={{ borderBottom: "1px solid var(--border)" }}>
                      <td style={{ padding: "14px 14px", color: "var(--muted)", fontFamily: "var(--font-geist-mono), monospace" }}>
                        #{row.rank}
                      </td>
                      <td style={{ padding: "14px 14px", fontWeight: 700 }}>{row.model}</td>
                      <td style={{ padding: "14px 14px" }}>
                        <span style={{ fontSize: 11, padding: "3px 8px", borderRadius: 5, background: "rgba(255,255,255,0.12)", color: "rgba(255,255,255,0.9)", fontWeight: 600 }}>
                          {typeLabel}
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
            These are <strong style={{ color: "var(--foreground)" }}>API-only results</strong> on 20 hand-selected prompts, run and reviewed manually.
            More models and prompts being added. Gemini result reflects free-tier rate limiting, not model quality.
          </p>
        </div>
      </section>

      {/* Contact CTA */}
      <section
        style={{
          padding: "80px 24px",
          borderTop: "1px solid var(--border)",
          textAlign: "center",
        }}
      >
        <div style={{ maxWidth: 640, margin: "0 auto" }}>
          <h2
            style={{
              fontSize: 32,
              fontWeight: 700,
              marginBottom: 16,
              letterSpacing: "-0.02em",
            }}
          >
            Get involved
          </h2>
          <p
            style={{
              color: "var(--muted)",
              marginBottom: 40,
              fontSize: 16,
              lineHeight: 1.7,
            }}
          >
            Working on a text-to-CAD model and want it on the leaderboard?
            Have feedback on the benchmark design?
          </p>
          <a
            href="mailto:contact@cadarena.dev"
            style={{
              display: "inline-block",
              background: "rgba(255,255,255,0.9)",
              color: "#3568a0",
              padding: "12px 32px",
              borderRadius: 8,
              textDecoration: "none",
              fontWeight: 700,
              fontSize: 15,
            }}
          >
            contact@cadarena.dev →
          </a>
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
              href="mailto:contact@cadarena.dev"
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
