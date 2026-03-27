"use client";

import { useEffect, useState } from "react";
import Nav from "../components/Nav";

type Part = {
  id: string;
  name: string;
  category: string;
  length?: number | null;
  holes?: number[] | null;
  radius_studs?: number | null;
  teeth?: number | null;
  bl_id?: string;
  description?: string;
};

function specLine(p: Part): string {
  if (p.category === "gear") return `${p.teeth}T · r=${p.radius_studs} studs`;
  if (p.category === "axle" || p.category === "beam") return `length=${p.length} studs`;
  if (p.category === "rack") return `length=${p.length} studs`;
  if (p.category === "pin") return `length=${p.length}`;
  return "";
}

export default function PartsPage() {
  const [parts, setParts] = useState<Part[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [q, setQ] = useState("");
  const [cat, setCat] = useState("all");
  const [selected, setSelected] = useState<Part | null>(null);

  useEffect(() => {
    fetch(`/api/parts?q=${encodeURIComponent(q)}&category=${cat}`)
      .then((r) => r.json())
      .then((d) => {
        setParts(d.parts);
        if (d.categories.length) setCategories(["all", ...d.categories]);
      });
  }, [q, cat]);

  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>

        {/* Left: browser */}
        <div style={{ width: 320, background: "var(--panel)", borderRight: "1px solid var(--border)", display: "flex", flexDirection: "column" }}>
          <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>Parts</span>
            <span style={{ fontSize: 11, color: "var(--muted)", fontFamily: "monospace" }}>{parts.length}</span>
          </div>

          {/* Search */}
          <div style={{ padding: 10, borderBottom: "1px solid var(--border)" }}>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search..."
              style={{
                width: "100%", padding: "7px 10px", background: "var(--panel-dark)",
                border: "1px solid var(--border-light)", borderRadius: 4,
                color: "var(--fg)", fontSize: 13,
              }}
            />
          </div>

          {/* Category filters */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 4, padding: "8px 10px", borderBottom: "1px solid var(--border)" }}>
            {categories.map((c) => (
              <button
                key={c}
                onClick={() => setCat(c)}
                style={{
                  padding: "3px 8px", borderRadius: 3, fontSize: 11, cursor: "pointer",
                  border: "none", background: cat === c ? "var(--accent)" : "var(--border)",
                  color: cat === c ? "#fff" : "var(--muted-light)",
                  fontWeight: cat === c ? 600 : 400,
                }}
              >
                {c}
              </button>
            ))}
          </div>

          {/* Parts list */}
          <div style={{ flex: 1, overflowY: "auto" }}>
            {parts.map((p) => (
              <div
                key={p.id}
                onClick={() => setSelected(p)}
                style={{
                  padding: "9px 14px", cursor: "pointer",
                  borderBottom: "1px solid #0a2040",
                  background: selected?.id === p.id ? "var(--border-light)" : "transparent",
                }}
              >
                <div style={{ fontFamily: "monospace", fontSize: 13, color: "var(--blue)" }}>{p.id}</div>
                <div style={{ fontSize: 12, color: "var(--muted)", marginTop: 2 }}>{p.name}</div>
                {specLine(p) && (
                  <div style={{ fontSize: 11, color: "var(--accent)", marginTop: 1 }}>{specLine(p)}</div>
                )}
              </div>
            ))}
            {parts.length === 0 && (
              <div style={{ padding: 20, fontSize: 13, color: "var(--muted)", fontFamily: "monospace" }}>
                no results
              </div>
            )}
          </div>
        </div>

        {/* Right: detail */}
        <div style={{ flex: 1, padding: 32, overflowY: "auto" }}>
          {selected ? (
            <div>
              <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 24 }}>
                <span style={{ fontFamily: "monospace", fontSize: 22, fontWeight: 700, color: "var(--blue)" }}>{selected.id}</span>
                <span style={{ fontSize: 11, padding: "2px 7px", borderRadius: 3, background: "var(--border)", color: "var(--muted-light)", fontFamily: "monospace" }}>
                  {selected.category}
                </span>
              </div>

              <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 24, color: "var(--fg)" }}>{selected.name}</h2>

              <table style={{ borderCollapse: "collapse", width: "100%", maxWidth: 480 }}>
                <tbody>
                  {(
                    [
                      ["Description", selected.description],
                      ["Category", selected.category],
                      selected.length != null ? ["Length", `${selected.length} studs`] : null,
                      selected.teeth != null ? ["Teeth", String(selected.teeth)] : null,
                      selected.radius_studs != null ? ["Radius", `${selected.radius_studs} studs`] : null,
                      selected.holes?.length ? ["Holes at", selected.holes.join(", ")] : null,
                      selected.bl_id ? ["BrickLink ID", selected.bl_id] : null,
                    ] as ([string, string] | null)[]
                  )
                    .filter((x): x is [string, string] => x !== null)
                    .map(([k, v]) => (
                      <tr key={String(k)} style={{ borderBottom: "1px solid var(--border)" }}>
                        <td style={{ padding: "10px 16px 10px 0", fontSize: 12, color: "var(--muted)", width: 140, verticalAlign: "top" }}>{k}</td>
                        <td style={{ padding: "10px 0", fontSize: 13, color: "var(--fg)", fontFamily: ["Holes at", "BrickLink ID"].includes(String(k)) ? "monospace" : "inherit" }}>{String(v)}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%", flexDirection: "column", gap: 8 }}>
              <div style={{ fontSize: 36, color: "var(--border)" }}>←</div>
              <div style={{ fontSize: 13, color: "var(--muted)", fontFamily: "monospace" }}>select a part</div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
