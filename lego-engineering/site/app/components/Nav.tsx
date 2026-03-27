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
    <nav
      style={{
        borderBottom: "1px solid var(--border)",
        position: "sticky",
        top: 0,
        zIndex: 50,
        background: "rgba(13,13,13,0.92)",
        backdropFilter: "blur(12px)",
      }}
    >
      <div
        style={{
          maxWidth: 1100,
          margin: "0 auto",
          padding: "0 24px",
          height: 54,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Link
          href="/"
          style={{
            fontFamily: "var(--font-geist-mono), monospace",
            fontSize: 17,
            fontWeight: 700,
            color: "var(--accent)",
            textDecoration: "none",
            letterSpacing: "-0.02em",
          }}
        >
          meche
        </Link>

        <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
          {links.map((l) => {
            const active = pathname === l.href;
            return (
              <Link
                key={l.href}
                href={l.href}
                style={{
                  padding: "5px 12px",
                  borderRadius: 6,
                  fontSize: 14,
                  fontWeight: active ? 600 : 400,
                  color: active ? "var(--fg)" : "var(--muted)",
                  textDecoration: "none",
                  background: active ? "var(--card)" : "transparent",
                  border: active ? "1px solid var(--border)" : "1px solid transparent",
                  transition: "color 0.15s",
                }}
              >
                {l.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
