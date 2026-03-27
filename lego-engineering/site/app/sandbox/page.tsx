import Nav from "../components/Nav";

export default function SandboxPage() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh" }}>
      <Nav />
      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "64px 24px" }}>
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
            STEP 02
          </p>
          <h1 style={{ fontSize: 36, fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 12 }}>
            Assembly Sandbox
          </h1>
          <p style={{ color: "var(--muted-light)", fontSize: 16, maxWidth: 580, lineHeight: 1.7 }}>
            Write an assembly spec in JSON. The compiler checks connections, catches overlaps,
            and renders the result. Think of it as a LEGO IDE.
          </p>
        </div>

        {/* Mock split-pane */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 24 }}>
          {/* Editor */}
          <div
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 10,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                padding: "10px 16px",
                borderBottom: "1px solid var(--border)",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <span style={{ fontSize: 12, color: "var(--muted)", fontFamily: "var(--font-geist-mono), monospace" }}>
                assembly.json
              </span>
              <span
                style={{
                  fontSize: 11,
                  padding: "2px 10px",
                  borderRadius: 4,
                  background: "#1a1a1a",
                  border: "1px solid var(--border)",
                  color: "#555",
                  fontFamily: "var(--font-geist-mono), monospace",
                  cursor: "not-allowed",
                }}
              >
                Compile →
              </span>
            </div>
            <div
              style={{
                fontFamily: "var(--font-geist-mono), monospace",
                fontSize: 13,
                color: "#666",
                padding: 20,
                lineHeight: 2,
                minHeight: 320,
              }}
            >
              <span style={{ color: "#555" }}>{`{`}</span><br />
              &nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;parts&quot;</span>
              <span style={{ color: "#555" }}>: [</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#555" }}>{`{`}</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;id&quot;</span>
              <span style={{ color: "#555" }}>: </span>
              <span style={{ color: "#a8d8a8" }}>&quot;32523&quot;</span>
              <span style={{ color: "#555" }}>,</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;name&quot;</span>
              <span style={{ color: "#555" }}>: </span>
              <span style={{ color: "#a8d8a8" }}>&quot;Technic Axle 4&quot;</span>
              <span style={{ color: "#555" }}>,</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;pos&quot;</span>
              <span style={{ color: "#555" }}>: [</span>
              <span style={{ color: "var(--accent)" }}>0, 0, 0</span>
              <span style={{ color: "#555" }}>],</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;rot&quot;</span>
              <span style={{ color: "#555" }}>: [</span>
              <span style={{ color: "var(--accent)" }}>0, 0, 0</span>
              <span style={{ color: "#555" }}>]</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#555" }}>{`},`}</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#555" }}>{`{`}</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;id&quot;</span>
              <span style={{ color: "#555" }}>: </span>
              <span style={{ color: "#a8d8a8" }}>&quot;3648&quot;</span>
              <span style={{ color: "#555" }}>,</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;name&quot;</span>
              <span style={{ color: "#555" }}>: </span>
              <span style={{ color: "#a8d8a8" }}>&quot;Technic Gear 24 Tooth&quot;</span>
              <span style={{ color: "#555" }}>,</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;pos&quot;</span>
              <span style={{ color: "#555" }}>: [</span>
              <span style={{ color: "var(--accent)" }}>0, 0, 0</span>
              <span style={{ color: "#555" }}>],</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#4a9eff" }}>&quot;connect&quot;</span>
              <span style={{ color: "#555" }}>: </span>
              <span style={{ color: "#a8d8a8" }}>&quot;axle:0&quot;</span><br />
              &nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: "#555" }}>{`}`}</span><br />
              &nbsp;&nbsp;<span style={{ color: "#555" }}>]</span><br />
              <span style={{ color: "#555" }}>{`}`}</span>
            </div>
          </div>

          {/* Output */}
          <div
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 10,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                padding: "10px 16px",
                borderBottom: "1px solid var(--border)",
                fontSize: 12,
                color: "var(--muted)",
                fontFamily: "var(--font-geist-mono), monospace",
              }}
            >
              output
            </div>
            <div
              style={{
                minHeight: 320,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 8,
                padding: 20,
              }}
            >
              <div style={{ fontSize: 48, color: "#222" }}>◫</div>
              <p style={{ color: "#444", fontSize: 13, margin: 0, fontFamily: "var(--font-geist-mono), monospace", textAlign: "center" }}>
                compiled render or<br />error messages appear here
              </p>
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
            Unlocks after the renderer (Step 01) is complete. The compiler will validate connection points,
            check for interpenetration, and output LDraw format. Errors will appear inline in the editor.
          </p>
        </div>
      </div>
    </div>
  );
}
