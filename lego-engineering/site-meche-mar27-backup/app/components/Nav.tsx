"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/parts", label: "Parts" },
  { href: "/viewer", label: "Viewer" },
  { href: "/sandbox", label: "Sandbox" },
  { href: "/build", label: "Build" },
  { href: "/simulate", label: "Simulate" },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <header style={{
      background: "var(--panel)",
      padding: "10px 20px",
      display: "flex",
      alignItems: "center",
      gap: 24,
      borderBottom: "1px solid var(--border)",
      flexShrink: 0,
    }}>
      <Link href="/" style={{ fontSize: 16, fontWeight: 700, color: "var(--accent)", textDecoration: "none", letterSpacing: "1px" }}>
        MECHE
      </Link>
      <span style={{ color: "var(--muted)", fontSize: 12 }}>AI LEGO assembly agent</span>
      <div style={{ marginLeft: "auto", display: "flex", gap: 4 }}>
        {links.map((l) => {
          const active = pathname === l.href;
          return (
            <Link
              key={l.href}
              href={l.href}
              style={{
                padding: "5px 12px",
                borderRadius: 4,
                fontSize: 13,
                fontWeight: active ? 600 : 400,
                color: active ? "#fff" : "var(--muted)",
                textDecoration: "none",
                background: active ? "var(--border-light)" : "transparent",
                transition: "color 0.15s",
              }}
            >
              {l.label}
            </Link>
          );
        })}
      </div>
    </header>
  );
}
