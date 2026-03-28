import Nav from "../components/Nav";

export default function SimulatePage() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div style={{ maxWidth: 900, margin: "0 auto", padding: "32px 24px", width: "100%" }}>

        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 24 }}>
          <span style={{ fontFamily: "monospace", color: "var(--muted)", fontSize: 12 }}>04</span>
          <h1 style={{ fontSize: 20, fontWeight: 700, color: "var(--fg)" }}>Simulator</h1>
          <span style={{
            fontSize: 11, padding: "2px 7px", borderRadius: 3,
            background: "#1a2a3a", color: "#7eb8e8", fontWeight: 700, letterSpacing: "0.05em", fontFamily: "monospace",
          }}>UPCOMING</span>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", gap: 12, marginBottom: 12, opacity: 0.6 }}>
          {/* Inputs */}
          <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 4 }}>
            <div style={{ padding: "8px 14px", borderBottom: "1px solid var(--border)", fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              inputs
            </div>
            <div style={{ padding: 14, display: "flex", flexDirection: "column", gap: 12 }}>
              {[
                { label: "Assembly", value: "gear_ratio_1_4.json" },
                { label: "Motor axle", value: "axle:0" },
                { label: "Input RPM", value: "100" },
                { label: "Duration", value: "2s" },
              ].map((f) => (
                <div key={f.label}>
                  <div style={{ fontSize: 11, color: "var(--muted)", marginBottom: 4 }}>{f.label}</div>
                  <input disabled defaultValue={f.value} style={{
                    width: "100%", padding: "6px 10px", background: "var(--panel-dark)",
                    border: "1px solid var(--border)", borderRadius: 3,
                    color: "#666", fontSize: 12, fontFamily: "monospace",
                  }} />
                </div>
              ))}
              <button disabled style={{
                marginTop: 4, padding: "8px", background: "var(--border)", border: "1px solid var(--border-light)",
                borderRadius: 3, color: "var(--muted)", fontSize: 12, cursor: "not-allowed",
              }}>
                Run simulation →
              </button>
            </div>
          </div>

          {/* Results */}
          <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 4 }}>
            <div style={{ padding: "8px 14px", borderBottom: "1px solid var(--border)", fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              results — example
            </div>
            <div style={{ padding: 16 }}>
              <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: 16 }}>
                <tbody>
                  {[
                    ["Input RPM", "100"],
                    ["Output RPM", "25"],
                    ["Gear ratio", "1:4"],
                    ["Torque mult.", "4×"],
                    ["Valid assembly", "yes"],
                    ["Stall?", "no"],
                  ].map(([k, v]) => (
                    <tr key={k} style={{ borderBottom: "1px solid var(--border)" }}>
                      <td style={{ padding: "8px 12px", fontSize: 12, color: "var(--muted)" }}>{k}</td>
                      <td style={{ padding: "8px 12px", fontSize: 13, color: "#555", fontFamily: "monospace", fontWeight: 600 }}>{v}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div style={{
                height: 80, background: "var(--panel-dark)", border: "1px dashed var(--border)",
                borderRadius: 3, display: "flex", alignItems: "center", justifyContent: "center",
                color: "var(--border-light)", fontSize: 12, fontFamily: "monospace",
              }}>
                [motion timeline]
              </div>
            </div>
          </div>
        </div>

        <div style={{
          background: "var(--panel)", border: "1px solid var(--border)",
          borderRadius: 4, padding: "14px 18px", fontSize: 13, color: "var(--muted-light)", lineHeight: 1.7,
        }}>
          <strong style={{ color: "var(--fg)" }}>Unlocks after:</strong> Build agent (step 03).
          Rigid body first: connected parts = one body, gear ratios from tooth counts, torque propagated through assembly graph.
        </div>
      </div>
    </div>
  );
}
