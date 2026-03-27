import Nav from "../components/Nav";

export default function PartsPage() {
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
            STEP 00
          </p>
          <h1 style={{ fontSize: 36, fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 12 }}>
            Parts Library
          </h1>
          <p style={{ color: "var(--muted-light)", fontSize: 16, maxWidth: 560, lineHeight: 1.7 }}>
            17k+ LEGO parts indexed with connection points, dimensions, and semantic labels.
            Search by name, category, or connection type.
          </p>
        </div>

        {/* Search bar placeholder */}
        <div
          style={{
            display: "flex",
            gap: 12,
            marginBottom: 40,
          }}
        >
          <div
            style={{
              flex: 1,
              height: 44,
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              padding: "0 16px",
              color: "#444",
              fontSize: 14,
              fontFamily: "var(--font-geist-mono), monospace",
            }}
          >
            Search parts... (e.g. "axle 4", "gear 40 tooth", "technic brick")
          </div>
          <div
            style={{
              height: 44,
              padding: "0 20px",
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              color: "#444",
              fontSize: 13,
              gap: 8,
            }}
          >
            Filter: All
          </div>
        </div>

        {/* Status */}
        <div
          style={{
            background: "var(--card)",
            border: "1px solid rgba(249,115,22,0.2)",
            borderRadius: 10,
            padding: "32px 36px",
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
              marginBottom: 16,
              fontFamily: "var(--font-geist-mono), monospace",
            }}
          >
            <span
              style={{
                width: 7,
                height: 7,
                borderRadius: "50%",
                background: "var(--accent)",
                display: "inline-block",
                animation: "pulse 2s infinite",
              }}
            />
            BUILDING
          </div>
          <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 10 }}>
            Parts indexer in progress
          </h3>
          <p style={{ color: "var(--muted-light)", fontSize: 14, lineHeight: 1.7, margin: "0 0 20px" }}>
            We&apos;re parsing the LDraw parts library (~17k .dat files) and extracting connection points,
            bounding boxes, and semantic categories for each part. Once done, this page will let you
            search and filter the full catalog.
          </p>
          <div style={{ display: "flex", gap: 24, fontSize: 13, color: "var(--muted)" }}>
            <span style={{ fontFamily: "var(--font-geist-mono), monospace" }}>
              Source: LDraw official parts library
            </span>
            <span style={{ fontFamily: "var(--font-geist-mono), monospace" }}>
              ~17,000 parts
            </span>
            <span style={{ fontFamily: "var(--font-geist-mono), monospace" }}>
              Format: .dat → JSON
            </span>
          </div>
        </div>

        {/* What will be here */}
        <div style={{ marginTop: 40 }}>
          <p style={{ fontSize: 13, color: "#444", marginBottom: 16, fontFamily: "var(--font-geist-mono), monospace" }}>
            WHAT WILL BE HERE:
          </p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 12 }}>
            {[
              "Search by name",
              "Filter by connection type",
              "Filter by category (Technic, Basic, etc.)",
              "Part detail view",
              "Connection points diagram",
              "Part image thumbnail",
            ].map((item) => (
              <div
                key={item}
                style={{
                  background: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: 8,
                  padding: "14px 16px",
                  fontSize: 13,
                  color: "#555",
                }}
              >
                {item}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
