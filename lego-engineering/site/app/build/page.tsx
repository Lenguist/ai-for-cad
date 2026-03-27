"use client";

import { useEffect, useState, useRef } from "react";
import dynamic from "next/dynamic";
import Nav from "../components/Nav";

const AssemblyViewer = dynamic(() => import("../components/AssemblyViewer"), { ssr: false });

type SimResult = {
  ok: boolean;
  level: number;
  brick_count: number;
  error_count: number;
  errors: { brick_id?: string; type?: string; message: string }[];
  summary: string;
};

type AssemblyBrick = {
  id: string;
  type: string;
  pos: [number, number, number];
  rot: number;
  color?: number;
};

type AssemblyState = {
  bricks: AssemblyBrick[];
};

const POLL_INTERVAL = 2000; // ms

export default function BuildPage() {
  const [version, setVersion] = useState(0);
  const [sim, setSim] = useState<SimResult | null>(null);
  const [assembly, setAssembly] = useState<AssemblyState | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [ldrExists, setLdrExists] = useState(false);
  const prevSimJson = useRef<string>("");

  // Poll for sim_result.json to detect updates
  useEffect(() => {
    let active = true;

    const poll = async () => {
      if (!active) return;

      try {
        // Check sim result
        const simRes = await fetch(`/workspace/sim_result.json?t=${Date.now()}`);
        if (simRes.ok) {
          const simData: SimResult = await simRes.json();
          const simJson = JSON.stringify(simData);
          if (simJson !== prevSimJson.current) {
            prevSimJson.current = simJson;
            setSim(simData);
            setVersion((v) => v + 1); // bump to reload ldr
            setLastUpdated(new Date().toLocaleTimeString());
            setLdrExists(true);
          }
        }
      } catch {
        // no sim result yet
      }
    };

    poll();
    const id = setInterval(poll, POLL_INTERVAL);
    return () => {
      active = false;
      clearInterval(id);
    };
  }, []);

  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>

        {/* Left: info + sim result */}
        <div style={{
          width: 280, background: "var(--panel)", borderRight: "1px solid var(--border)",
          display: "flex", flexDirection: "column", flexShrink: 0,
        }}>
          <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontFamily: "monospace", color: "var(--muted)", fontSize: 11 }}>03</span>
            <span style={{ fontSize: 13, fontWeight: 700, color: "var(--fg)" }}>Build</span>
            <span style={{
              fontSize: 10, padding: "1px 6px", borderRadius: 3,
              background: "#3a2a00", color: "#d4a843", fontWeight: 700, fontFamily: "monospace",
            }}>LIVE</span>
          </div>

          {/* Status */}
          <div style={{ padding: "12px 14px", borderBottom: "1px solid var(--border)" }}>
            <div style={{ fontSize: 11, color: "var(--muted)", marginBottom: 8 }}>assembly status</div>

            {sim ? (
              <>
                <div style={{
                  display: "flex", alignItems: "center", gap: 8, marginBottom: 8,
                }}>
                  <span style={{
                    width: 8, height: 8, borderRadius: "50%",
                    background: sim.ok ? "#4caf50" : "#e94560",
                    display: "inline-block", flexShrink: 0,
                  }} />
                  <span style={{ fontFamily: "monospace", fontSize: 12, color: sim.ok ? "#4caf50" : "#e94560" }}>
                    {sim.ok ? "valid" : `${sim.error_count} error${sim.error_count !== 1 ? "s" : ""}`}
                  </span>
                </div>

                <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                  <Row label="bricks" value={String(sim.brick_count)} />
                  <Row label="level" value={`L${sim.level}`} />
                  {lastUpdated && <Row label="updated" value={lastUpdated} />}
                </div>

                {sim.errors.length > 0 && (
                  <div style={{ marginTop: 12 }}>
                    <div style={{ fontSize: 11, color: "var(--muted)", marginBottom: 6 }}>errors</div>
                    <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                      {sim.errors.map((e, i) => (
                        <div key={i} style={{
                          background: "#2a0a0a", border: "1px solid #5a1a1a",
                          borderRadius: 3, padding: "6px 8px",
                          fontSize: 11, color: "#ff6b6b", fontFamily: "monospace",
                        }}>
                          {e.brick_id && <span style={{ color: "#e94560" }}>[{e.brick_id}] </span>}
                          {e.message}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div style={{ fontSize: 12, color: "var(--muted)", fontFamily: "monospace" }}>
                waiting for agent...
                <div style={{ marginTop: 8, fontSize: 11, lineHeight: 1.6 }}>
                  Run <code style={{ color: "var(--blue)" }}>python agent/tools.py</code> to generate an assembly.
                </div>
              </div>
            )}
          </div>

          {/* How to use */}
          <div style={{ padding: "12px 14px", flex: 1 }}>
            <div style={{ fontSize: 11, color: "var(--muted)", marginBottom: 8 }}>how to use</div>
            <div style={{ fontSize: 11, color: "var(--muted)", lineHeight: 1.7 }}>
              From <code style={{ color: "var(--blue)" }}>lego-engineering/</code>:
              <br /><br />
              <code style={{ color: "#7eb8e8" }}>python agent/tools.py</code>
              <br /><br />
              Or in Claude Code:
              <br />
              <code style={{ color: "#7eb8e8", fontSize: 10 }}>from agent.tools import place, save</code>
              <br /><br />
              After <code style={{ color: "var(--blue)" }}>save()</code>, this viewer auto-updates every 2s.
            </div>
          </div>
        </div>

        {/* Right: 3D viewer */}
        <div style={{ flex: 1, position: "relative" }}>
          {ldrExists ? (
            <AssemblyViewer
              ldrUrl="/workspace/assembly.ldr"
              version={version}
            />
          ) : (
            <div style={{
              width: "100%", height: "100%", display: "flex", flexDirection: "column",
              alignItems: "center", justifyContent: "center", gap: 12,
            }}>
              <div style={{ fontSize: 13, color: "var(--muted)", fontFamily: "monospace" }}>
                no assembly yet
              </div>
              <div style={{ fontSize: 12, color: "var(--muted)", opacity: 0.6 }}>
                run <code style={{ color: "var(--blue)" }}>python agent/tools.py</code> to generate one
              </div>
            </div>
          )}

          <div style={{
            position: "absolute", bottom: 12, left: 14,
            fontSize: 11, color: "rgba(255,255,255,0.3)", fontFamily: "monospace",
          }}>
            drag to orbit · scroll to zoom · auto-refreshes every 2s
          </div>
        </div>

      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11 }}>
      <span style={{ color: "var(--muted)" }}>{label}</span>
      <span style={{ fontFamily: "monospace", color: "var(--fg)" }}>{value}</span>
    </div>
  );
}
