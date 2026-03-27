import Nav from "../components/Nav";

export default function PartsPage() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div style={{ maxWidth: 1000, margin: "0 auto", padding: "32px 24px", width: "100%" }}>

        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 24 }}>
          <span style={{ fontFamily: "monospace", color: "var(--muted)", fontSize: 12 }}>00</span>
          <h1 style={{ fontSize: 20, fontWeight: 700, color: "var(--fg)" }}>Parts Library</h1>
          <span style={{
            fontSize: 11, padding: "2px 7px", borderRadius: 3,
            background: "#3a2a00", color: "#d4a843", fontWeight: 700, letterSpacing: "0.05em", fontFamily: "monospace",
          }}>BUILDING</span>
        </div>

        {/* Search */}
        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          <input
            disabled
            placeholder="Search parts... (e.g. axle 4, gear 40 tooth, technic brick)"
            style={{
              flex: 1, padding: "8px 12px", background: "var(--panel-dark)",
              border: "1px solid var(--border-light)", borderRadius: 4,
              color: "var(--muted)", fontSize: 13,
            }}
          />
          <select disabled style={{
            padding: "8px 12px", background: "var(--panel-dark)",
            border: "1px solid var(--border-light)", borderRadius: 4,
            color: "var(--muted)", fontSize: 13,
          }}>
            <option>All categories</option>
          </select>
        </div>

        {/* Placeholder grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 8, marginBottom: 32 }}>
          {Array.from({ length: 12 }).map((_, i) => (
            <div key={i} style={{
              background: "var(--panel)",
              border: "1px solid var(--border)",
              borderRadius: 4,
              padding: "12px 14px",
              opacity: 0.35,
            }}>
              <div style={{ fontFamily: "monospace", fontSize: 13, color: "var(--blue)", marginBottom: 4 }}>
                {String(3001 + i * 7)}
              </div>
              <div style={{ fontSize: 12, color: "var(--muted)" }}>—</div>
            </div>
          ))}
        </div>

        <div style={{
          background: "var(--panel)",
          border: "1px solid var(--border)",
          borderRadius: 4,
          padding: "16px 20px",
          fontSize: 13,
          color: "var(--muted-light)",
          lineHeight: 1.7,
        }}>
          <strong style={{ color: "var(--fg)" }}>Status:</strong> Parsing LDraw .dat files (~17k parts) to extract
          connection points, bounding boxes, and categories. Grid above will populate once the index is built.
        </div>
      </div>
    </div>
  );
}
