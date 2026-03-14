const INITIATIVES = [
  {
    name: "CAD Arena",
    url: "https://cadarena.dev",
    color: "#4a80b4",
    tagline: "AI-generated parametric CAD",
    desc: "The first open benchmark comparing text-to-CAD models. 13+ models, 4 difficulty tiers, arena-style voting.",
    status: "BETA",
    stats: [
      { value: "13+", label: "models" },
      { value: "20", label: "prompts run" },
      { value: "95%", label: "top score" },
    ],
  },
  {
    name: "Lego Engineering",
    url: "https://lego-engineering.dev",
    color: "#3d7a52",
    tagline: "AI-generated brick assemblies",
    desc: "Benchmark for AI on LEGO and brick assembly generation. Reproducing academic results, testing frontier models.",
    status: "IN PROGRESS",
    stats: [
      { value: "5+", label: "papers" },
      { value: "3+", label: "models" },
      { value: "Phase 1", label: "underway" },
    ],
  },
];

const DIGEST_PLACEHOLDER = {
  date: "2026-03-14",
  items: [
    {
      title: "BrickGPT reproduction underway",
      desc: "Phase 1 of Lego Engineering benchmark: reproducing BrickGPT (CVPR 2024) results on original dataset.",
      tag: "lego-engineering",
      tagColor: "#3d7a52",
    },
    {
      title: "CAD Arena preliminary results: Claude Opus & Zoo tied at 95%",
      desc: "Full run of 4 models × 20 prompts complete. CAD Arena leaderboard launching soon.",
      tag: "cadarena",
      tagColor: "#4a80b4",
    },
    {
      title: "Monorepo restructure complete",
      desc: "ai-for-cad repo reorganized into cadarena/, lego-engineering/, and ai-eng-hub/ sub-initiatives.",
      tag: "infrastructure",
      tagColor: "rgba(255,255,255,0.3)",
    },
  ],
};

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
          background: "rgba(70, 42, 120, 0.92)",
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
          <span
            style={{
              fontFamily: "var(--font-geist-mono), monospace",
              fontSize: 18,
              fontWeight: 700,
              color: "var(--accent)",
              letterSpacing: "-0.02em",
            }}
          >
            AI for Engineering
          </span>
          <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
            {["Digest", "Benchmarks", "About"].map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}
              >
                {item}
              </a>
            ))}
            <a
              href="https://github.com"
              style={{ color: "var(--muted)", textDecoration: "none", fontSize: 14, fontWeight: 500 }}
            >
              GitHub →
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
            <span style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--accent)", display: "inline-block" }} />
            OPEN RESEARCH HUB · 2026
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
            Tracking AI progress
            <br />
            <span style={{ color: "var(--accent)" }}>across engineering domains</span>
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
            Open benchmarks, weekly research digests, and deep analysis on AI for{" "}
            <strong style={{ color: "var(--foreground)" }}>CAD, LEGO, and beyond</strong>.
          </p>

          <div style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
            <a
              href="#benchmarks"
              style={{
                background: "rgba(255,255,255,0.9)",
                color: "#462a78",
                padding: "12px 28px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 700,
                fontSize: 15,
              }}
            >
              Browse Benchmarks →
            </a>
            <a
              href="#digest"
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
              Weekly Digest
            </a>
          </div>
        </div>
      </section>

      {/* Benchmarks */}
      <section id="benchmarks" style={{ padding: "80px 24px", borderTop: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" }}>
            Active benchmarks
          </h2>
          <p style={{ color: "var(--muted)", marginBottom: 48, fontSize: 16 }}>
            Each initiative is an independent research benchmark with its own website, leaderboard, and paper.
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(440px, 1fr))", gap: 24 }}>
            {INITIATIVES.map((init) => (
              <a
                key={init.name}
                href={init.url}
                style={{
                  background: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: 12,
                  padding: 32,
                  textDecoration: "none",
                  color: "inherit",
                  display: "block",
                  borderTop: `3px solid ${init.color}`,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
                  <div>
                    <div style={{ fontWeight: 800, fontSize: 20, marginBottom: 4, letterSpacing: "-0.02em" }}>
                      {init.name}
                    </div>
                    <div style={{ fontSize: 13, color: "var(--muted)", fontFamily: "var(--font-geist-mono), monospace" }}>
                      {init.tagline}
                    </div>
                  </div>
                  <span
                    style={{
                      fontSize: 10,
                      padding: "3px 8px",
                      borderRadius: 5,
                      background: `${init.color}33`,
                      color: init.color,
                      fontWeight: 700,
                      letterSpacing: "0.06em",
                      border: `1px solid ${init.color}55`,
                      whiteSpace: "nowrap",
                    }}
                  >
                    {init.status}
                  </span>
                </div>

                <p style={{ fontSize: 14, color: "var(--muted)", lineHeight: 1.7, marginBottom: 24 }}>
                  {init.desc}
                </p>

                <div style={{ display: "flex", gap: 24 }}>
                  {init.stats.map((s, i) => (
                    <div key={i}>
                      <div
                        style={{
                          fontFamily: "var(--font-geist-mono), monospace",
                          fontSize: 20,
                          fontWeight: 800,
                          color: init.color,
                          lineHeight: 1,
                          marginBottom: 4,
                        }}
                      >
                        {s.value}
                      </div>
                      <div style={{ fontSize: 11, color: "var(--muted)", fontWeight: 500 }}>{s.label}</div>
                    </div>
                  ))}
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Weekly Digest */}
      <section id="digest" style={{ padding: "80px 24px", borderTop: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: 48, flexWrap: "wrap", gap: 16 }}>
            <div>
              <h2 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8, letterSpacing: "-0.02em" }}>
                Weekly digest
              </h2>
              <p style={{ color: "var(--muted)", fontSize: 16, margin: 0 }}>
                AI for engineering news, research updates, and benchmark results.
              </p>
            </div>
            <span
              style={{
                fontFamily: "var(--font-geist-mono), monospace",
                fontSize: 12,
                color: "var(--muted)",
                padding: "4px 10px",
                border: "1px solid var(--border)",
                borderRadius: 6,
              }}
            >
              {DIGEST_PLACEHOLDER.date}
            </span>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {DIGEST_PLACEHOLDER.items.map((item, i) => (
              <div
                key={i}
                style={{
                  background: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: 10,
                  padding: 24,
                  display: "flex",
                  gap: 20,
                  alignItems: "flex-start",
                }}
              >
                <div
                  style={{
                    fontFamily: "var(--font-geist-mono), monospace",
                    fontSize: 20,
                    fontWeight: 800,
                    color: "rgba(255,255,255,0.15)",
                    lineHeight: 1,
                    minWidth: 32,
                    paddingTop: 2,
                  }}
                >
                  {String(i + 1).padStart(2, "0")}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                    <span style={{ fontWeight: 700, fontSize: 15 }}>{item.title}</span>
                    <span
                      style={{
                        fontSize: 10,
                        padding: "2px 7px",
                        borderRadius: 4,
                        background: `${item.tagColor}33`,
                        color: item.tagColor,
                        fontWeight: 600,
                        letterSpacing: "0.05em",
                        border: `1px solid ${item.tagColor}55`,
                        whiteSpace: "nowrap",
                      }}
                    >
                      {item.tag}
                    </span>
                  </div>
                  <p style={{ color: "var(--muted)", fontSize: 14, lineHeight: 1.6, margin: 0 }}>{item.desc}</p>
                </div>
              </div>
            ))}
          </div>

          <div
            style={{
              marginTop: 24,
              padding: 20,
              background: "rgba(255,255,255,0.07)",
              border: "1px solid rgba(255,255,255,0.2)",
              borderRadius: 10,
              fontSize: 14,
              color: "var(--muted)",
            }}
          >
            <strong style={{ color: "var(--foreground)" }}>Generated weekly with Claude + search.</strong>{" "}
            Covers AI for CAD, robotics, structural engineering, manufacturing, and more.
            Subscribe to get it in your inbox.{" "}
            <a href="mailto:digest@ai4eng.dev" style={{ color: "var(--accent)", textDecoration: "none" }}>
              digest@ai4eng.dev →
            </a>
          </div>
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
            AI for Engineering
          </span>
          <div style={{ display: "flex", gap: 24, fontSize: 13, color: "var(--muted)" }}>
            <span>Open research · 2026</span>
            <a href="https://cadarena.dev" style={{ color: "var(--muted)", textDecoration: "none" }}>CAD Arena</a>
            <a href="https://lego-engineering.dev" style={{ color: "var(--muted)", textDecoration: "none" }}>Lego Engineering</a>
            <a href="https://github.com" style={{ color: "var(--muted)", textDecoration: "none" }}>GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
