import Nav from "../components/Nav";

export default function ViewerPage() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh" }}>
      <Nav />
      <div style={{ maxWidth: 1000, margin: "0 auto", padding: "64px 24px" }}>
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
            STEP 01
          </p>
          <h1 style={{ fontSize: 36, fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 12 }}>
            Renderer
          </h1>
          <p style={{ color: "var(--muted-light)", fontSize: 16, maxWidth: 560, lineHeight: 1.7 }}>
            Give it a part ID or a simple assembly — get back a rendered image.
            The foundation for all visual feedback in Meche.
          </p>
        </div>

        {/* Mock UI */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          {/* Input */}
          <div
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 10,
              padding: 24,
            }}
          >
            <p
              style={{
                fontSize: 11,
                color: "var(--muted)",
                fontFamily: "var(--font-geist-mono), monospace",
                letterSpacing: "0.08em",
                marginBottom: 16,
              }}
            >
              INPUT
            </p>
            <div
              style={{
                fontFamily: "var(--font-geist-mono), monospace",
                fontSize: 13,
                color: "#555",
                background: "#0a0a0a",
                border: "1px solid var(--border)",
                borderRadius: 6,
                padding: 16,
                lineHeight: 1.8,
                minHeight: 160,
              }}
            >
              <span style={{ color: "#555" }}>{`// Part ID`}</span><br />
              <span style={{ color: "var(--accent)" }}>3001</span><br /><br />
              <span style={{ color: "#555" }}>{`// or assembly JSON`}</span><br />
              <span style={{ color: "#666" }}>{`{`}</span><br />
              <span style={{ color: "#666" }}>&nbsp;&nbsp;{`"parts": [`}</span><br />
              <span style={{ color: "#666" }}>&nbsp;&nbsp;&nbsp;&nbsp;{`{ "id": "3001", "pos": [0,0,0] }`}</span><br />
              <span style={{ color: "#666" }}>&nbsp;&nbsp;{`]`}</span><br />
              <span style={{ color: "#666" }}>{`}`}</span>
            </div>
            <div
              style={{
                marginTop: 16,
                padding: "10px 20px",
                background: "#1a1a1a",
                border: "1px solid var(--border)",
                borderRadius: 6,
                fontSize: 14,
                fontWeight: 600,
                color: "#555",
                textAlign: "center",
                cursor: "not-allowed",
              }}
            >
              Render →
            </div>
          </div>

          {/* Output */}
          <div
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 10,
              padding: 24,
              display: "flex",
              flexDirection: "column",
            }}
          >
            <p
              style={{
                fontSize: 11,
                color: "var(--muted)",
                fontFamily: "var(--font-geist-mono), monospace",
                letterSpacing: "0.08em",
                marginBottom: 16,
              }}
            >
              OUTPUT
            </p>
            <div
              style={{
                flex: 1,
                minHeight: 200,
                background: "#0a0a0a",
                border: "1px dashed #2a2a2a",
                borderRadius: 6,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 8,
              }}
            >
              <div style={{ fontSize: 32, color: "#2a2a2a" }}>□</div>
              <p style={{ color: "#444", fontSize: 13, margin: 0, fontFamily: "var(--font-geist-mono), monospace" }}>
                render will appear here
              </p>
            </div>
          </div>
        </div>

        {/* Status */}
        <div
          style={{
            marginTop: 24,
            background: "var(--card)",
            border: "1px solid rgba(249,115,22,0.2)",
            borderRadius: 10,
            padding: "24px 28px",
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              fontSize: 11,
              color: "var(--accent)",
              fontWeight: 700,
              letterSpacing: "0.1em",
              marginBottom: 12,
              fontFamily: "var(--font-geist-mono), monospace",
            }}
          >
            <span style={{ width: 7, height: 7, borderRadius: "50%", background: "var(--accent)", display: "inline-block" }} />
            BUILDING
          </div>
          <p style={{ color: "var(--muted-light)", fontSize: 14, lineHeight: 1.7, margin: 0 }}>
            Setting up the LDraw → PNG rendering pipeline.
            Evaluating: LDView (CLI), Blender + ImportLDraw addon, and a Python-native path via ldraw_py.
            Success = <code style={{ fontFamily: "var(--font-geist-mono), monospace", color: "var(--accent)" }}>render(&quot;3001&quot;)</code> returns
            a recognizable image of a 2x4 brick.
          </p>
        </div>
      </div>
    </div>
  );
}
