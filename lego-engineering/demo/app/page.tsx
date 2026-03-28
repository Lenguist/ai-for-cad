import Link from "next/link";
import Nav from "./components/Nav";

const steps = [
  {
    num: "00",
    title: "Parts Library",
    href: "/parts",
    status: "LIVE",
    statusColor: "#4caf50",
    statusBg: "#0a2a0a",
    description: "26 Technic parts + 20 standard bricks. Search, filter by category, view specs.",
    userSees: "Search box + part list with specs table",
  },
  {
    num: "01",
    title: "Renderer",
    href: "/viewer",
    status: "LIVE",
    statusColor: "#4caf50",
    statusBg: "#0a2a0a",
    description: "LDraw part ID → Three.js 3D render. Orbit controls, auto-rotation.",
    userSees: "Select part → interactive 3D view",
  },
  {
    num: "02",
    title: "Compiler + Validator",
    href: "/build",
    status: "LIVE",
    statusColor: "#4caf50",
    statusBg: "#0a2a0a",
    description: "DSL JSON → L1 semantic + L2 physical validation → LDraw file. Agent tools: place, remove, save.",
    userSees: "Live assembly viewer — auto-refreshes as agent builds",
  },
  {
    num: "03",
    title: "Agent Build Loop",
    href: "/build",
    status: "UPCOMING",
    statusColor: "#7eb8e8",
    statusBg: "#1a2a3a",
    description: "Text prompt → Claude Code agent searches parts, places bricks, iterates on errors.",
    userSees: "Prompt → streaming agent log → live 3D render",
  },
  {
    num: "04",
    title: "Kinematic Simulator",
    href: "/simulate",
    status: "UPCOMING",
    statusColor: "#7eb8e8",
    statusBg: "#1a2a3a",
    description: "Technic phase: motor → gear train → L3 kinematic sim → RPM, direction, stall detection.",
    userSees: "Motor inputs → results table (does the mechanism work?)",
  },
];

export default function Home() {
  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />

      <div style={{ maxWidth: 860, margin: "0 auto", padding: "40px 24px", width: "100%" }}>
        <div style={{ marginBottom: 32 }}>
          <p style={{ color: "var(--muted)", fontSize: 13, lineHeight: 1.7 }}>
            Five-layer stack for AI-driven LEGO Technic design. Describe a mechanism, get back a
            working assembly with verified physics.
          </p>
        </div>

        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid var(--border)" }}>
              {["Step", "Name", "Status", "What it does", "User sees"].map((h) => (
                <th
                  key={h}
                  style={{
                    padding: "8px 12px",
                    textAlign: "left",
                    fontSize: 11,
                    color: "var(--muted)",
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: "0.08em",
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {steps.map((step) => (
              <tr
                key={step.num}
                style={{ borderBottom: "1px solid var(--border)", cursor: "pointer" }}
              >
                <td style={{ padding: "14px 12px" }}>
                  <Link href={step.href} style={{ textDecoration: "none" }}>
                    <span style={{ fontFamily: "monospace", fontSize: 13, color: "var(--muted)" }}>
                      {step.num}
                    </span>
                  </Link>
                </td>
                <td style={{ padding: "14px 12px" }}>
                  <Link href={step.href} style={{ textDecoration: "none" }}>
                    <span style={{ fontWeight: 600, color: "var(--fg)", fontSize: 14 }}>{step.title}</span>
                  </Link>
                </td>
                <td style={{ padding: "14px 12px" }}>
                  <span style={{
                    fontSize: 11,
                    padding: "2px 7px",
                    borderRadius: 3,
                    background: step.statusBg,
                    color: step.statusColor,
                    fontWeight: 700,
                    letterSpacing: "0.05em",
                    fontFamily: "monospace",
                    whiteSpace: "nowrap",
                  }}>
                    {step.status}
                  </span>
                </td>
                <td style={{ padding: "14px 12px" }}>
                  <span style={{ fontSize: 13, color: "var(--muted-light)" }}>{step.description}</span>
                </td>
                <td style={{ padding: "14px 12px" }}>
                  <span style={{ fontSize: 12, color: "var(--muted)", fontStyle: "italic" }}>{step.userSees}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <div style={{ marginTop: 48, display: "flex", gap: 32 }}>
          <div style={{
            flex: 1,
            background: "var(--panel)",
            border: "1px solid var(--border)",
            borderRadius: 6,
            padding: "20px 24px",
          }}>
            <div style={{ fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12 }}>
              current focus
            </div>
            <p style={{ fontSize: 13, color: "var(--muted-light)", lineHeight: 1.7 }}>
              Phase 1 done: parts DB, compiler, L1+L2 validators, agent tools.
              Next: Phase 2 — Technic parts, gear kinematics, agent prompt loop.
            </p>
          </div>

          <div style={{
            flex: 1,
            background: "var(--panel)",
            border: "1px solid var(--border)",
            borderRadius: 6,
            padding: "20px 24px",
          }}>
            <div style={{ fontSize: 11, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12 }}>
              data source
            </div>
            <p style={{ fontSize: 13, color: "var(--muted-light)", lineHeight: 1.7 }}>
              LDraw parts library — ~17k .dat files, open format, covers all official LEGO Technic parts.
              Connection points extracted programmatically.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
