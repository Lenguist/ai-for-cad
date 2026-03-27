import Nav from "../components/Nav";

export default function SandboxPage() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "32px 24px", width: "100%" }}>

        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 24 }}>
          <span style={{ fontFamily: "monospace", color: "var(--muted)", fontSize: 12 }}>02</span>
          <h1 style={{ fontSize: 20, fontWeight: 700, color: "var(--fg)" }}>Assembly Sandbox</h1>
          <span style={{
            fontSize: 11, padding: "2px 7px", borderRadius: 3,
            background: "#1a2a3a", color: "#7eb8e8", fontWeight: 700, letterSpacing: "0.05em", fontFamily: "monospace",
          }}>UPCOMING</span>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 16 }}>
          {/* Editor */}
          <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 4, opacity: 0.6 }}>
            <div style={{ padding: "8px 14px", borderBottom: "1px solid var(--border)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>assembly.json</span>
              <button disabled style={{
                padding: "3px 10px", background: "var(--border)", border: "1px solid var(--border-light)",
                borderRadius: 3, color: "var(--muted)", fontSize: 12, cursor: "not-allowed",
              }}>Compile</button>
            </div>
            <pre style={{
              padding: 16, fontFamily: "monospace", fontSize: 12, color: "#666",
              lineHeight: 1.8, minHeight: 280,
            }}>{`{
  "parts": [
    {
      "id": "32523",
      "name": "Technic Axle 4",
      "pos": [0, 0, 0],
      "rot": [0, 0, 0]
    },
    {
      "id": "3648",
      "name": "Technic Gear 24 Tooth",
      "pos": [0, 0, 0],
      "connect": "axle:0"
    }
  ]
}`}</pre>
          </div>

          {/* Output */}
          <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 4, opacity: 0.6 }}>
            <div style={{ padding: "8px 14px", borderBottom: "1px solid var(--border)", fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              output
            </div>
            <div style={{ minHeight: 280, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", gap: 8 }}>
              <div style={{ fontSize: 36, color: "var(--border-light)" }}>◫</div>
              <div style={{ fontSize: 12, color: "var(--muted)", fontFamily: "monospace" }}>render or error list</div>
            </div>
          </div>
        </div>

        <div style={{
          background: "var(--panel)", border: "1px solid var(--border)",
          borderRadius: 4, padding: "14px 18px", fontSize: 13, color: "var(--muted-light)", lineHeight: 1.7,
        }}>
          <strong style={{ color: "var(--fg)" }}>Unlocks after:</strong> Renderer (step 01). Compiler will validate
          connection points and check for part interpenetration, then output LDraw.
        </div>
      </div>
    </div>
  );
}
