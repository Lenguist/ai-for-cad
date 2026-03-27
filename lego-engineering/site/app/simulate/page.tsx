import Nav from "../components/Nav";

export default function SimulatePage() {
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
            STEP 04
          </p>
          <h1 style={{ fontSize: 36, fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 12 }}>
            Simulator
          </h1>
          <p style={{ color: "var(--muted-light)", fontSize: 16, maxWidth: 560, lineHeight: 1.7 }}>
            Apply a motor to an assembly and see what happens. Does the escalator escalate?
            Does the gear ratio check out? Physics tells you.
          </p>
        </div>

        {/* Mock UI */}
        <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", gap: 16, marginBottom: 24 }}>
          {/* Inputs */}
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
                marginBottom: 20,
              }}
            >
              SIMULATION INPUTS
            </p>

            {[
              { label: "Assembly", value: "gear_ratio_1_4.json", type: "file" },
              { label: "Motor axle", value: "axle:0", type: "select" },
              { label: "Input RPM", value: "100", type: "number" },
              { label: "Duration", value: "2s", type: "number" },
            ].map((field) => (
              <div key={field.label} style={{ marginBottom: 16 }}>
                <div style={{ fontSize: 11, color: "#555", fontFamily: "var(--font-geist-mono), monospace", marginBottom: 6 }}>
                  {field.label}
                </div>
                <div
                  style={{
                    height: 36,
                    background: "#0a0a0a",
                    border: "1px solid #222",
                    borderRadius: 6,
                    display: "flex",
                    alignItems: "center",
                    padding: "0 12px",
                    color: "#555",
                    fontSize: 13,
                    fontFamily: "var(--font-geist-mono), monospace",
                  }}
                >
                  {field.value}
                </div>
              </div>
            ))}

            <div
              style={{
                marginTop: 8,
                padding: "10px 16px",
                background: "#1a1a1a",
                border: "1px solid var(--border)",
                borderRadius: 6,
                fontSize: 13,
                fontWeight: 600,
                color: "#555",
                textAlign: "center",
                cursor: "not-allowed",
                fontFamily: "var(--font-geist-mono), monospace",
              }}
            >
              Run simulation →
            </div>
          </div>

          {/* Results */}
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
                marginBottom: 20,
              }}
            >
              RESULTS — example output (not live)
            </p>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 20 }}>
              {[
                { label: "Input RPM", value: "100", unit: "rpm" },
                { label: "Output RPM", value: "25", unit: "rpm" },
                { label: "Gear ratio", value: "1:4", unit: "" },
                { label: "Torque mult.", value: "4×", unit: "" },
                { label: "Status", value: "VALID", unit: "" },
                { label: "Stall?", value: "No", unit: "" },
              ].map((stat) => (
                <div
                  key={stat.label}
                  style={{
                    background: "#0a0a0a",
                    border: "1px solid #1a1a1a",
                    borderRadius: 6,
                    padding: "12px 14px",
                  }}
                >
                  <div style={{ fontSize: 11, color: "#555", fontFamily: "var(--font-geist-mono), monospace", marginBottom: 4 }}>
                    {stat.label}
                  </div>
                  <div style={{ fontSize: 20, fontWeight: 700, color: "#3a3a3a", fontFamily: "var(--font-geist-mono), monospace" }}>
                    {stat.value} <span style={{ fontSize: 12, fontWeight: 400 }}>{stat.unit}</span>
                  </div>
                </div>
              ))}
            </div>

            <div
              style={{
                height: 100,
                background: "#0a0a0a",
                border: "1px dashed #1a1a1a",
                borderRadius: 6,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#2a2a2a",
                fontSize: 13,
                fontFamily: "var(--font-geist-mono), monospace",
              }}
            >
              [motion animation / timeline]
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
          <p style={{ color: "var(--muted-light)", fontSize: 14, lineHeight: 1.7, margin: "0 0 12px" }}>
            The last layer. Starts simple: connected parts treated as rigid bodies, gear ratios computed
            from tooth counts, motor torque propagated through the assembly graph.
          </p>
          <p style={{ color: "var(--muted)", fontSize: 13, lineHeight: 1.7, margin: 0 }}>
            Eventually: contact forces, flex, collision detection. But first — does the gear ratio math out?
          </p>
        </div>
      </div>
    </div>
  );
}
