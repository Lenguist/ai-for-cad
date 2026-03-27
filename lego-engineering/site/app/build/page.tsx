import Nav from "../components/Nav";

const exampleSteps = [
  { icon: "◎", text: "Decomposing task: '1:4 gear ratio drivetrain'", color: "var(--muted)" },
  { icon: "⌕", text: "Searching parts: 'technic axle'  →  32523 (Axle 4), 32062 (Axle 2)", color: "var(--muted)" },
  { icon: "⌕", text: "Searching parts: 'technic gear'  →  3648 (24T), 32270 (8T)", color: "var(--muted)" },
  { icon: "◈", text: "Placing: axle 32523 at [0,0,0]", color: "var(--muted)" },
  { icon: "◈", text: "Placing: gear 3648 (24T) on axle at [0,0,0], connect: axle:0", color: "var(--muted)" },
  { icon: "◈", text: "Placing: axle 32062 at [40,0,0]", color: "var(--muted)" },
  { icon: "◈", text: "Placing: gear 32270 (8T) on axle at [40,0,0], connect: axle:0", color: "var(--muted)" },
  { icon: "✓", text: "Compile: OK — no overlaps, all connections valid", color: "#4ade80" },
  { icon: "◻", text: "Rendering... → assembly_v1.png", color: "var(--muted)" },
];

export default function BuildPage() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh" }}>
      <Nav />
      <div style={{ maxWidth: 900, margin: "0 auto", padding: "64px 24px" }}>
        <div style={{ marginBottom: 48 }}>
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
            STEP 03
          </p>
          <h1 style={{ fontSize: 36, fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 12 }}>
            Build
          </h1>
          <p style={{ color: "var(--muted-light)", fontSize: 16, maxWidth: 560, lineHeight: 1.7 }}>
            Describe a LEGO mechanism in plain english. The agent searches parts,
            writes assembly code, compiles it, and iterates until it works.
          </p>
        </div>

        {/* Prompt input */}
        <div
          style={{
            display: "flex",
            gap: 12,
            marginBottom: 32,
          }}
        >
          <div
            style={{
              flex: 1,
              height: 50,
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              padding: "0 18px",
              color: "#444",
              fontSize: 15,
            }}
          >
            build a 1:4 gear ratio drivetrain
          </div>
          <div
            style={{
              height: 50,
              padding: "0 24px",
              background: "#1a1a1a",
              border: "1px solid var(--border)",
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              color: "#555",
              fontSize: 14,
              fontWeight: 600,
              cursor: "not-allowed",
            }}
          >
            Build →
          </div>
        </div>

        {/* Agent steps preview */}
        <div
          style={{
            background: "var(--card)",
            border: "1px solid var(--border)",
            borderRadius: 10,
            overflow: "hidden",
            marginBottom: 16,
          }}
        >
          <div
            style={{
              padding: "10px 20px",
              borderBottom: "1px solid var(--border)",
              fontSize: 11,
              color: "var(--muted)",
              fontFamily: "var(--font-geist-mono), monospace",
              letterSpacing: "0.08em",
            }}
          >
            AGENT LOG — example output (not live)
          </div>
          <div style={{ padding: "16px 20px", display: "flex", flexDirection: "column", gap: 10 }}>
            {exampleSteps.map((step, i) => (
              <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
                <span
                  style={{
                    fontFamily: "var(--font-geist-mono), monospace",
                    fontSize: 14,
                    color: step.color,
                    lineHeight: 1.5,
                    minWidth: 16,
                  }}
                >
                  {step.icon}
                </span>
                <span
                  style={{
                    fontFamily: "var(--font-geist-mono), monospace",
                    fontSize: 13,
                    color: step.color,
                    lineHeight: 1.5,
                  }}
                >
                  {step.text}
                </span>
              </div>
            ))}
            <div
              style={{
                marginTop: 8,
                height: 120,
                background: "#0a0a0a",
                border: "1px dashed #2a2a2a",
                borderRadius: 6,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#333",
                fontSize: 13,
                fontFamily: "var(--font-geist-mono), monospace",
              }}
            >
              [rendered assembly image]
            </div>
          </div>
        </div>

        {/* Coming soon */}
        <div
          style={{
            background: "var(--card)",
            border: "1px solid var(--border)",
            borderRadius: 10,
            padding: "24px 28px",
          }}
        >
          <span
            style={{
              fontSize: 10,
              padding: "2px 8px",
              borderRadius: 4,
              background: "#1a1a1a",
              color: "#444",
              fontWeight: 700,
              letterSpacing: "0.06em",
              fontFamily: "var(--font-geist-mono), monospace",
              border: "1px solid #2a2a2a",
              display: "inline-block",
              marginBottom: 12,
            }}
          >
            COMING SOON
          </span>
          <p style={{ color: "var(--muted-light)", fontSize: 14, lineHeight: 1.7, margin: 0 }}>
            Unlocks after the assembly sandbox (Step 02) is complete. Meche-Claude will have access to
            part search, assembly compilation, and rendering as tool calls — iterating on errors
            exactly like a coding agent.
          </p>
        </div>
      </div>
    </div>
  );
}
