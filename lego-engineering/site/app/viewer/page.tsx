import Nav from "../components/Nav";

export default function ViewerPage() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div style={{ maxWidth: 1000, margin: "0 auto", padding: "32px 24px", width: "100%" }}>

        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 24 }}>
          <span style={{ fontFamily: "monospace", color: "var(--muted)", fontSize: 12 }}>01</span>
          <h1 style={{ fontSize: 20, fontWeight: 700, color: "var(--fg)" }}>Renderer</h1>
          <span style={{
            fontSize: 11, padding: "2px 7px", borderRadius: 3,
            background: "#3a2a00", color: "#d4a843", fontWeight: 700, letterSpacing: "0.05em", fontFamily: "monospace",
          }}>BUILDING</span>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "340px 1fr", gap: 12 }}>
          {/* Input panel */}
          <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 4 }}>
            <div style={{ padding: "8px 14px", borderBottom: "1px solid var(--border)", fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              input
            </div>
            <div style={{ padding: 14 }}>
              <div style={{ fontSize: 12, color: "var(--muted)", marginBottom: 6 }}>Part ID</div>
              <input
                disabled
                placeholder="e.g. 3001"
                style={{
                  width: "100%", padding: "7px 10px", background: "var(--panel-dark)",
                  border: "1px solid var(--border-light)", borderRadius: 4,
                  color: "var(--muted)", fontSize: 13, marginBottom: 16,
                }}
              />
              <div style={{ fontSize: 12, color: "var(--muted)", marginBottom: 6 }}>or Assembly JSON</div>
              <textarea
                disabled
                rows={8}
                placeholder={`{\n  "parts": [\n    { "id": "3001", "pos": [0,0,0] }\n  ]\n}`}
                style={{
                  width: "100%", padding: "7px 10px", background: "var(--panel-dark)",
                  border: "1px solid var(--border-light)", borderRadius: 4,
                  color: "var(--muted)", fontSize: 12, resize: "none",
                  fontFamily: "monospace", lineHeight: 1.6, marginBottom: 14,
                }}
              />
              <button disabled style={{
                width: "100%", padding: "8px", background: "var(--border)",
                border: "1px solid var(--border-light)", borderRadius: 4,
                color: "var(--muted)", fontSize: 13, fontWeight: 600, cursor: "not-allowed",
              }}>
                Render
              </button>
            </div>
          </div>

          {/* Output panel */}
          <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 4 }}>
            <div style={{ padding: "8px 14px", borderBottom: "1px solid var(--border)", fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              output
            </div>
            <div style={{
              display: "flex", alignItems: "center", justifyContent: "center",
              minHeight: 320, flexDirection: "column", gap: 8,
            }}>
              <div style={{ fontSize: 48, color: "var(--border-light)" }}>□</div>
              <div style={{ fontSize: 12, color: "var(--muted)", fontFamily: "monospace" }}>render appears here</div>
            </div>
          </div>
        </div>

        <div style={{
          marginTop: 16, background: "var(--panel)", border: "1px solid var(--border)",
          borderRadius: 4, padding: "14px 18px", fontSize: 13, color: "var(--muted-light)", lineHeight: 1.7,
        }}>
          <strong style={{ color: "var(--fg)" }}>Status:</strong> Evaluating LDraw → PNG pipeline options
          (LDView CLI, Blender + ImportLDraw, ldraw_py). Target: <code style={{ fontFamily: "monospace", color: "var(--blue)" }}>render("3001")</code> returns a recognizable 2x4 brick.
        </div>
      </div>
    </div>
  );
}
