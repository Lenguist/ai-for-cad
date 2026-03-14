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
          background: "rgba(45, 100, 65, 0.92)",
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
              Lego Engineering
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
            {["Papers", "Leaderboard", "About"].map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}
              >
                {item}
              </a>
            ))}
            <a
              href="https://ai4eng.dev"
              style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}
            >
              AI4Eng Hub →
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section
        className="blueprint-bg"
        style={{ padding: "100px 24px 80px", textAlign: "center", position: "relative", overflow: "hidden" }}
      >
        <div
          style={{
            position: "absolute",
            top: "40%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 600,
            height: 400,
            background: "radial-gradient(ellipse, rgba(255,255,255,0.08) 0%, transparent 70%)",
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
            <span style={{ color: "var(--accent)" }}>for AI-generated brick assemblies</span>
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
            Reproduce academic results. Test frontier models. Compare{" "}
            <strong style={{ color: "var(--foreground)" }}>BrickGPT, GPT-4, Claude</strong>{" "}
            and more on LEGO and brick assembly generation tasks.
          </p>

          <div style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
            <a
              href="#leaderboard"
              style={{
                background: "rgba(255,255,255,0.9)",
                color: "#2d6441",
                padding: "12px 28px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 700,
                fontSize: 15,
              }}
            >
              View Leaderboard →
            </a>
            <a
              href="#papers"
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
              Browse Papers
            </a>
          </div>
        </div>
      </section>

      {/* Stats bar */}
      <div style={{ borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)", background: "var(--card)" }}>
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
            { value: "5+", label: "Papers reproduced" },
            { value: "3+", label: "Models compared" },
            { value: "100+", label: "Benchmark prompts" },
            { value: "2", label: "Datasets" },
          ].map((stat, i) => (
            <div key={i} style={{ padding: "28px 16px", borderRight: i < 3 ? "1px solid var(--border)" : "none" }}>
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
              <div style={{ fontSize: 13, color: "var(--muted)", fontWeight: 500 }}>{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Research phases */}
      <section style={{ padding: "80px 24px" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" }}>
            Research approach
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 48, fontSize: 16 }}>
            Three phases: reproduce, retest with frontier models, then cross-benchmark.
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 24 }}>
            {[
              {
                step: "01",
                title: "Reproduce papers",
                desc: "Run each paper on its own benchmark. Verify claimed results using the original code and datasets. Starting with BrickGPT.",
                status: "IN PROGRESS",
                statusColor: "#4ade80",
              },
              {
                step: "02",
                title: "Retest with frontier models",
                desc: "Apply the same benchmark tasks to latest Claude, GPT, and Gemini. How do general LLMs compare to specialized models?",
                status: "UPCOMING",
                statusColor: "rgba(255,255,255,0.4)",
              },
              {
                step: "03",
                title: "Cross-benchmark",
                desc: "Evaluate all models across all paper benchmarks. Build a unified leaderboard with reproducible metrics.",
                status: "UPCOMING",
                statusColor: "rgba(255,255,255,0.4)",
              },
            ].map((phase) => (
              <div
                key={phase.step}
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
                    marginBottom: 12,
                  }}
                >
                  PHASE {phase.step}
                </div>
                <div
                  style={{
                    display: "inline-block",
                    fontSize: 10,
                    padding: "2px 8px",
                    borderRadius: 4,
                    background: `${phase.statusColor}22`,
                    color: phase.statusColor,
                    fontWeight: 700,
                    letterSpacing: "0.06em",
                    marginBottom: 16,
                    border: `1px solid ${phase.statusColor}44`,
                  }}
                >
                  {phase.status}
                </div>
                <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 10, letterSpacing: "-0.01em" }}>
                  {phase.title}
                </h3>
                <p style={{ color: "var(--muted)", fontSize: 14, lineHeight: 1.7, margin: 0 }}>{phase.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Papers */}
      <section id="papers" style={{ padding: "80px 24px", borderTop: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" }}>
            Papers in scope
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 48, fontSize: 16 }}>
            Academic work on AI-driven brick and LEGO assembly generation.
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
            {[
              {
                name: "BrickGPT",
                venue: "CVPR 2024",
                desc: "LLM-based LEGO brick assembly generation. Autoregressive model conditioned on 3D structure.",
                status: "Reproducing",
                statusColor: "#4ade80",
              },
              {
                name: "More papers coming",
                venue: "—",
                desc: "Additional papers on procedural assembly generation, brick-level 3D reconstruction, and instruction following.",
                status: "Planned",
                statusColor: "rgba(255,255,255,0.4)",
              },
            ].map((paper) => (
              <div
                key={paper.name}
                style={{
                  background: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: 10,
                  padding: 22,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 2 }}>{paper.name}</div>
                    <div style={{ fontSize: 12, color: "var(--muted)", fontFamily: "var(--font-geist-mono), monospace" }}>
                      {paper.venue}
                    </div>
                  </div>
                  <span
                    style={{
                      fontSize: 10,
                      padding: "3px 8px",
                      borderRadius: 5,
                      background: `${paper.statusColor}22`,
                      color: paper.statusColor,
                      fontWeight: 600,
                      border: `1px solid ${paper.statusColor}44`,
                      whiteSpace: "nowrap",
                    }}
                  >
                    {paper.status}
                  </span>
                </div>
                <p style={{ fontSize: 12, color: "var(--muted)", lineHeight: 1.6, margin: 0 }}>{paper.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Leaderboard placeholder */}
      <section id="leaderboard" style={{ padding: "80px 24px", borderTop: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" }}>
            Leaderboard
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 48, fontSize: 16 }}>
            Results will appear here as benchmarks are completed.
          </p>
          <div
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 12,
              padding: 48,
              textAlign: "center",
            }}
          >
            <div
              style={{
                fontFamily: "var(--font-geist-mono), monospace",
                fontSize: 12,
                color: "var(--muted)",
                letterSpacing: "0.1em",
                marginBottom: 16,
              }}
            >
              PHASE 1 IN PROGRESS
            </div>
            <p style={{ color: "var(--muted)", fontSize: 15, margin: 0 }}>
              Reproducing BrickGPT results. Leaderboard launches after Phase 1 is complete.
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section style={{ padding: "80px 24px", borderTop: "1px solid var(--border)", textAlign: "center" }}>
        <div style={{ maxWidth: 640, margin: "0 auto" }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 16, letterSpacing: "-0.02em" }}>
            Get involved
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 40, fontSize: 16, lineHeight: 1.7 }}>
            Working on brick assembly AI? Have a model you&apos;d like benchmarked? Get in touch.
          </p>
          <a
            href="mailto:contact@lego-engineering.dev"
            style={{
              display: "inline-block",
              background: "rgba(255,255,255,0.9)",
              color: "#2d6441",
              padding: "12px 32px",
              borderRadius: 8,
              textDecoration: "none",
              fontWeight: 700,
              fontSize: 15,
            }}
          >
            contact@lego-engineering.dev →
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: "1px solid var(--border)", padding: "32px 24px" }}>
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
          <span style={{ fontFamily: "var(--font-geist-mono), monospace", fontWeight: 700, color: "var(--accent)", fontSize: 14 }}>
            Lego Engineering
          </span>
          <div style={{ display: "flex", gap: 24, fontSize: 13, color: "var(--muted)" }}>
            <span>Open research · 2026</span>
            <a href="https://ai4eng.dev" style={{ color: "var(--muted)", textDecoration: "none" }}>AI4Eng Hub</a>
            <a href="https://cadarena.dev" style={{ color: "var(--muted)", textDecoration: "none" }}>CAD Arena</a>
            <a href="https://github.com" style={{ color: "var(--muted)", textDecoration: "none" }}>GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
