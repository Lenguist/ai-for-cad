import Link from "next/link";
import Nav from "./components/Nav";

const steps = [
  {
    num: "00",
    title: "Parts Library",
    href: "/parts",
    status: "BUILDING",
    statusColor: "#d4a843",
    statusBg: "#3a2a00",
    description: "Index LDraw parts with connection points, dimensions, categories. Search and filter.",
    userSees: "Search box + part grid with specs",
  },
  {
    num: "01",
    title: "Renderer",
    href: "/viewer",
    status: "BUILDING",
    statusColor: "#d4a843",
    statusBg: "#3a2a00",
    description: "Part ID or assembly JSON in → PNG render out. Programmatic pipeline.",
    userSees: "Input a part ID, get back an image of the brick",
  },
  {
    num: "02",
    title: "Assembly Sandbox",
    href: "/sandbox",
    status: "UPCOMING",
    statusColor: "#7eb8e8",
    statusBg: "#1a2a3a",
    description: "JSON assembly spec → compiler validates connections + overlaps → renders result.",
    userSees: "JSON editor left, render + errors right",
  },
  {
    num: "03",
    title: "Build",
    href: "/build",
    status: "UPCOMING",
    statusColor: "#7eb8e8",
    statusBg: "#1a2a3a",
    description: "Text prompt → agent searches parts, writes assembly, compiles, iterates on errors.",
    userSees: "Prompt input → streaming agent log → final render",
  },
  {
    num: "04",
    title: "Simulator",
    href: "/simulate",
    status: "UPCOMING",
    statusColor: "#7eb8e8",
    statusBg: "#1a2a3a",
    description: "Apply motor to assembly → rigid body sim → output RPM, torque, motion check.",
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
              Steps 00 + 01 in parallel: build the parts index and get a single brick rendering
              correctly. Everything else depends on these.
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
