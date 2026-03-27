import Nav from "../components/Nav";

const exampleLog = [
  { icon: "◎", text: "decomposing: '1:4 gear ratio drivetrain'", color: "#888" },
  { icon: "⌕", text: "search parts: 'technic axle'  →  32523 (Axle 4), 32062 (Axle 2)", color: "#888" },
  { icon: "⌕", text: "search parts: 'technic gear'  →  3648 (24T), 32270 (8T)", color: "#888" },
  { icon: "▸", text: "place 32523 at [0,0,0]", color: "#888" },
  { icon: "▸", text: "place 3648 on axle:0 at [0,0,0]", color: "#888" },
  { icon: "▸", text: "place 32062 at [40,0,0]", color: "#888" },
  { icon: "▸", text: "place 32270 on axle:0 at [40,0,0]", color: "#888" },
  { icon: "✓", text: "compile: OK — no overlaps, all connections valid", color: "#4caf50" },
  { icon: "◻", text: "rendering → assembly_v1.png", color: "#888" },
];

export default function BuildPage() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div style={{ maxWidth: 900, margin: "0 auto", padding: "32px 24px", width: "100%" }}>

        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 24 }}>
          <span style={{ fontFamily: "monospace", color: "var(--muted)", fontSize: 12 }}>03</span>
          <h1 style={{ fontSize: 20, fontWeight: 700, color: "var(--fg)" }}>Build</h1>
          <span style={{
            fontSize: 11, padding: "2px 7px", borderRadius: 3,
            background: "#1a2a3a", color: "#7eb8e8", fontWeight: 700, letterSpacing: "0.05em", fontFamily: "monospace",
          }}>UPCOMING</span>
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          <input
            disabled
            defaultValue="build a 1:4 gear ratio drivetrain"
            style={{
              flex: 1, padding: "8px 12px", background: "var(--panel)",
              border: "1px solid var(--border)", borderRadius: 4,
              color: "var(--muted)", fontSize: 14, opacity: 0.6,
            }}
          />
          <button disabled style={{
            padding: "8px 20px", background: "var(--border)", border: "1px solid var(--border-light)",
            borderRadius: 4, color: "var(--muted)", fontSize: 13, fontWeight: 600, cursor: "not-allowed",
          }}>
            Build →
          </button>
        </div>

        <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 4, marginBottom: 12, opacity: 0.6 }}>
          <div style={{ padding: "8px 14px", borderBottom: "1px solid var(--border)", fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
            agent log — example
          </div>
          <div style={{ padding: 16, display: "flex", flexDirection: "column", gap: 8 }}>
            {exampleLog.map((line, i) => (
              <div key={i} style={{ display: "flex", gap: 10, fontFamily: "monospace", fontSize: 12 }}>
                <span style={{ color: line.color, minWidth: 14 }}>{line.icon}</span>
                <span style={{ color: line.color }}>{line.text}</span>
              </div>
            ))}
            <div style={{
              marginTop: 8, height: 100, background: "var(--panel-dark)",
              border: "1px dashed var(--border)", borderRadius: 4,
              display: "flex", alignItems: "center", justifyContent: "center",
              color: "var(--border-light)", fontSize: 12, fontFamily: "monospace",
            }}>
              [rendered assembly]
            </div>
          </div>
        </div>

        <div style={{
          background: "var(--panel)", border: "1px solid var(--border)",
          borderRadius: 4, padding: "14px 18px", fontSize: 13, color: "var(--muted-light)", lineHeight: 1.7,
        }}>
          <strong style={{ color: "var(--fg)" }}>Unlocks after:</strong> Assembly sandbox (step 02).
          Agent uses part search, compile, and render as tool calls — iterates on errors like a coding agent.
        </div>
      </div>
    </div>
  );
}
