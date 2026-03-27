import Link from "next/link";
import Nav from "./components/Nav";

const steps = [
  {
    num: "00",
    title: "Parts Library",
    href: "/parts",
    status: "BUILDING",
    statusColor: "#f97316",
    description: "17k+ LEGO parts indexed with connection points, dimensions, and semantic labels. Search by name, category, or connection type.",
    userExperience: "Browse and search the full LEGO parts catalog. Click any part to see its specs and connection points.",
  },
  {
    num: "01",
    title: "Renderer",
    href: "/viewer",
    status: "BUILDING",
    statusColor: "#f97316",
    description: "Programmatic rendering pipeline. Give it a part ID or assembly spec — get back a PNG.",
    userExperience: "Type a part ID, hit Render, see the brick. Works for single parts and multi-part assemblies.",
  },
  {
    num: "02",
    title: "Assembly Sandbox",
    href: "/sandbox",
    status: "COMING SOON",
    statusColor: "#444",
    description: "JSON-based assembly DSL with a real-time compiler. Validates connections, catches overlaps, outputs LDraw.",
    userExperience: "Write an assembly spec on the left, see the compiled render on the right. Error messages inline.",
  },
  {
    num: "03",
    title: "Build",
    href: "/build",
    status: "COMING SOON",
    statusColor: "#444",
    description: "Meche-Claude agent: takes a text prompt, searches parts, writes assembly code, compiles + renders, iterates on errors.",
    userExperience: "Type 'build a 1:4 gear ratio drivetrain'. Watch the agent search parts, place them, fix errors, and show you the result.",
  },
  {
    num: "04",
    title: "Simulator",
    href: "/simulate",
    status: "COMING SOON",
    statusColor: "#444",
    description: "Physics-based simulation. Rigid body first: connected parts move as one. Then gear ratios, motor torques, contact forces.",
    userExperience: "Set motor RPM on input axle. Simulator tells you output shaft speed, whether the mechanism moves, what breaks.",
  },
];

export default function Home() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh" }}>
      <Nav />

      {/* Hero */}
      <section
        className="grid-bg"
        style={{ padding: "96px 24px 80px", textAlign: "center", position: "relative" }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "radial-gradient(ellipse 60% 50% at 50% 40%, rgba(249,115,22,0.07) 0%, transparent 70%)",
            pointerEvents: "none",
          }}
        />
        <div style={{ maxWidth: 720, margin: "0 auto", position: "relative" }}>
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              fontSize: 12,
              color: "var(--accent)",
              fontWeight: 600,
              letterSpacing: "0.1em",
              marginBottom: 32,
              padding: "5px 14px",
              border: "1px solid rgba(249,115,22,0.3)",
              borderRadius: 20,
              background: "rgba(249,115,22,0.08)",
              fontFamily: "var(--font-geist-mono), monospace",
            }}
          >
            <span style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--accent)", display: "inline-block" }} />
            EARLY RESEARCH · 2026
          </div>

          <h1
            style={{
              fontSize: "clamp(38px, 6vw, 68px)",
              fontWeight: 800,
              lineHeight: 1.08,
              marginBottom: 24,
              letterSpacing: "-0.035em",
              color: "var(--fg)",
            }}
          >
            Describe it.
            <br />
            <span style={{ color: "var(--accent)" }}>Build it.</span>
            <br />
            Simulate it.
          </h1>

          <p
            style={{
              fontSize: 18,
              color: "var(--muted-light)",
              maxWidth: 520,
              margin: "0 auto 44px",
              lineHeight: 1.7,
            }}
          >
            An AI agent that designs working LEGO Technic mechanisms from plain english —
            finding parts, placing them, and verifying the physics.
          </p>

          <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
            <Link
              href="/build"
              style={{
                background: "var(--accent)",
                color: "#fff",
                padding: "11px 28px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 700,
                fontSize: 15,
              }}
            >
              Try it →
            </Link>
            <Link
              href="/parts"
              style={{
                border: "1px solid var(--border)",
                color: "var(--muted-light)",
                padding: "11px 28px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 500,
                fontSize: 15,
                background: "var(--card)",
              }}
            >
              Browse parts
            </Link>
          </div>
        </div>
      </section>

      {/* Pipeline */}
      <section style={{ padding: "80px 24px", borderTop: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <div style={{ marginBottom: 56 }}>
            <p
              style={{
                fontFamily: "var(--font-geist-mono), monospace",
                fontSize: 11,
                color: "var(--accent)",
                letterSpacing: "0.12em",
                fontWeight: 600,
                marginBottom: 10,
              }}
            >
              THE STACK
            </p>
            <h2 style={{ fontSize: 28, fontWeight: 700, letterSpacing: "-0.02em", margin: 0 }}>
              Five layers, built in order
            </h2>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
            {steps.map((step, i) => (
              <Link
                key={step.num}
                href={step.href}
                style={{ textDecoration: "none" }}
              >
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "56px 1fr auto",
                    alignItems: "center",
                    gap: 24,
                    padding: "24px 28px",
                    background: "var(--card)",
                    border: "1px solid var(--border)",
                    borderRadius: 10,
                    cursor: "pointer",
                    transition: "border-color 0.15s",
                  }}
                >
                  <div
                    style={{
                      fontFamily: "var(--font-geist-mono), monospace",
                      fontSize: 22,
                      fontWeight: 700,
                      color: step.status === "BUILDING" ? "var(--accent)" : "#333",
                      lineHeight: 1,
                    }}
                  >
                    {step.num}
                  </div>

                  <div>
                    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                      <span style={{ fontSize: 16, fontWeight: 700, color: "var(--fg)" }}>{step.title}</span>
                      <span
                        style={{
                          fontSize: 10,
                          padding: "2px 8px",
                          borderRadius: 4,
                          background: `${step.statusColor}18`,
                          color: step.statusColor,
                          fontWeight: 700,
                          letterSpacing: "0.06em",
                          border: `1px solid ${step.statusColor}33`,
                          fontFamily: "var(--font-geist-mono), monospace",
                        }}
                      >
                        {step.status}
                      </span>
                    </div>
                    <p style={{ fontSize: 13, color: "var(--muted)", margin: "0 0 6px", lineHeight: 1.6 }}>
                      {step.description}
                    </p>
                    <p style={{ fontSize: 12, color: "#555", margin: 0, fontStyle: "italic" }}>
                      User sees: {step.userExperience}
                    </p>
                  </div>

                  <div style={{ color: "#333", fontSize: 18 }}>→</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: "1px solid var(--border)", padding: "28px 24px" }}>
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
            meche
          </span>
          <div style={{ display: "flex", gap: 24, fontSize: 13, color: "var(--muted)" }}>
            <span>open research · 2026</span>
            <a href="https://cadarena.dev" style={{ color: "var(--muted)", textDecoration: "none" }}>CAD Arena</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
