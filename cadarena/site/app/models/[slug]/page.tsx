import { notFound } from "next/navigation";
import Link from "next/link";
import { MODELS, TYPE_STYLES } from "../../data/models";

export function generateStaticParams() {
  return MODELS.map((m) => ({ slug: m.slug }));
}

export default async function ModelPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const model = MODELS.find((m) => m.slug === slug);
  if (!model) notFound();

  const s = TYPE_STYLES[model.type];

  return (
    <div style={{ background: "var(--background)", minHeight: "100vh" }}>
      {/* Nav */}
      <nav
        style={{
          borderBottom: "1px solid var(--border)",
          position: "sticky",
          top: 0,
          zIndex: 50,
          backdropFilter: "blur(12px)",
          background: "rgba(55, 105, 160, 0.92)",
        }}
      >
        <div
          style={{
            maxWidth: 1200,
            margin: "0 auto",
            padding: "0 24px",
            height: 56,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <Link
            href="/"
            style={{
              fontFamily: "var(--font-geist-mono), monospace",
              fontSize: 18,
              fontWeight: 700,
              color: "var(--accent)",
              textDecoration: "none",
              letterSpacing: "-0.02em",
            }}
          >
            CAD Arena
          </Link>
          <Link
            href="/#models"
            style={{
              color: "var(--muted)",
              textDecoration: "none",
              fontSize: 14,
              fontWeight: 500,
            }}
          >
            ← All models
          </Link>
        </div>
      </nav>

      <div
        style={{
          maxWidth: 860,
          margin: "0 auto",
          padding: "56px 40px",
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px)",
          backgroundSize: "40px 40px",
          minHeight: "calc(100vh - 56px)",
        }}
      >
        {/* Header */}
        <div style={{ marginBottom: 48 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
            <span
              style={{
                fontSize: 11,
                padding: "3px 10px",
                background: s.bg,
                color: s.color,
                fontWeight: 700,
                letterSpacing: "0.1em",
                border: "1px solid rgba(255,255,255,0.2)",
                fontFamily: "var(--font-geist-mono), monospace",
              }}
            >
              {s.label.toUpperCase()}
            </span>
            <span
              style={{
                fontFamily: "var(--font-geist-mono), monospace",
                fontSize: 12,
                color: "var(--muted)",
              }}
            >
              {model.venue} · {model.year}
            </span>
          </div>

          <h1
            style={{
              fontSize: "clamp(28px, 4vw, 42px)",
              fontWeight: 800,
              color: "var(--foreground)",
              marginBottom: 16,
              letterSpacing: "-0.02em",
              lineHeight: 1.1,
            }}
          >
            {model.name}
          </h1>

          {model.description && (
            <p
              style={{
                fontSize: 16,
                color: "rgba(255,255,255,0.8)",
                lineHeight: 1.75,
                maxWidth: 680,
              }}
            >
              {model.description}
            </p>
          )}
        </div>

        {/* Meta grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: 1,
            marginBottom: 48,
            border: "1px solid var(--border)",
            background: "var(--border)",
          }}
        >
          {[
            { label: "Input", value: model.input },
            { label: "Output", value: model.output },
            { label: "Venue", value: model.venue },
            { label: "Year", value: model.year },
          ].map(({ label, value }) => (
            <div
              key={label}
              style={{
                background: "rgba(0,0,0,0.1)",
                padding: "18px 20px",
              }}
            >
              <div
                style={{
                  fontFamily: "var(--font-geist-mono), monospace",
                  fontSize: 10,
                  color: "var(--muted)",
                  letterSpacing: "0.1em",
                  marginBottom: 6,
                  textTransform: "uppercase",
                }}
              >
                {label}
              </div>
              <div style={{ fontSize: 14, fontWeight: 600, color: "var(--foreground)" }}>
                {value}
              </div>
            </div>
          ))}
        </div>

        {/* Links */}
        {model.links && Object.keys(model.links).length > 0 && (
          <div style={{ marginBottom: 48 }}>
            <div
              style={{
                fontFamily: "var(--font-geist-mono), monospace",
                fontSize: 11,
                color: "var(--muted)",
                letterSpacing: "0.1em",
                marginBottom: 14,
                textTransform: "uppercase",
              }}
            >
              Links
            </div>
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
              {model.links.paper && (
                <a
                  href={model.links.paper}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={linkStyle}
                >
                  Paper →
                </a>
              )}
              {model.links.github && (
                <a
                  href={model.links.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={linkStyle}
                >
                  GitHub →
                </a>
              )}
              {model.links.project && (
                <a
                  href={model.links.project}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={linkStyle}
                >
                  Project page →
                </a>
              )}
              {model.links.website && (
                <a
                  href={model.links.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={linkStyle}
                >
                  Website →
                </a>
              )}
            </div>
          </div>
        )}

        {/* Arena status */}
        <div
          style={{
            background: "rgba(0,0,0,0.1)",
            border: "1px solid var(--border)",
            borderLeft: "3px solid rgba(255,255,255,0.4)",
            padding: "20px 24px",
          }}
        >
          <div
            style={{
              fontFamily: "var(--font-geist-mono), monospace",
              fontSize: 10,
              color: "var(--muted)",
              letterSpacing: "0.1em",
              marginBottom: 8,
              textTransform: "uppercase",
            }}
          >
            CAD Arena Status
          </div>
          <div style={{ fontSize: 14, color: "rgba(255,255,255,0.7)" }}>
            Scheduled for evaluation on the full 200-prompt benchmark. Results will appear on the leaderboard at launch.
          </div>
        </div>
      </div>
    </div>
  );
}

const linkStyle: React.CSSProperties = {
  display: "inline-block",
  padding: "8px 16px",
  border: "1px solid rgba(255,255,255,0.25)",
  color: "var(--foreground)",
  textDecoration: "none",
  fontSize: 13,
  fontFamily: "var(--font-geist-mono), monospace",
  background: "rgba(255,255,255,0.07)",
  fontWeight: 500,
};
