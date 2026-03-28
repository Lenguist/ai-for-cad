"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import Nav from "../components/Nav";

const LDrawViewer = dynamic(() => import("../components/LDrawViewer"), { ssr: false });

const PART_IDS = [
  "beam-3", "beam-5", "beam-7", "beam-9", "beam-11", "beam-15",
  "gear-8t", "gear-16t", "gear-24t", "gear-40t", "gear-worm",
  "rack-4",
  "axle-3", "axle-4", "axle-5", "axle-6", "axle-8", "axle-10",
  "pin", "pin-friction", "pin-long",
  "bush", "connector-2x2",
];

export default function ViewerPage() {
  const [partId, setPartId] = useState("gear-8t");
  const [inputVal, setInputVal] = useState("gear-8t");

  return (
    <div style={{ background: "var(--bg)", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Nav />
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>

        {/* Left controls */}
        <div style={{ width: 240, background: "var(--panel)", borderRight: "1px solid var(--border)", display: "flex", flexDirection: "column" }}>
          <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontFamily: "monospace", color: "var(--muted)", fontSize: 11 }}>01</span>
            <span style={{ fontSize: 13, fontWeight: 700, color: "var(--fg)" }}>Renderer</span>
            <span style={{ fontSize: 10, padding: "1px 6px", borderRadius: 3, background: "#3a2a00", color: "#d4a843", fontWeight: 700, fontFamily: "monospace" }}>LIVE</span>
          </div>

          <div style={{ padding: 12, borderBottom: "1px solid var(--border)" }}>
            <div style={{ fontSize: 11, color: "var(--muted)", marginBottom: 6 }}>part id</div>
            <div style={{ display: "flex", gap: 6 }}>
              <input
                value={inputVal}
                onChange={(e) => setInputVal(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && setPartId(inputVal.trim())}
                style={{
                  flex: 1, padding: "6px 8px", background: "var(--panel-dark)",
                  border: "1px solid var(--border-light)", borderRadius: 3,
                  color: "var(--fg)", fontSize: 12, fontFamily: "monospace",
                }}
              />
              <button
                onClick={() => setPartId(inputVal.trim())}
                style={{
                  padding: "6px 10px", background: "var(--accent)", border: "none",
                  borderRadius: 3, color: "#fff", fontSize: 12, cursor: "pointer", fontWeight: 600,
                }}
              >
                →
              </button>
            </div>
          </div>

          <div style={{ padding: "8px 12px", borderBottom: "1px solid var(--border)", fontSize: 11, color: "var(--muted)" }}>
            quick select
          </div>
          <div style={{ flex: 1, overflowY: "auto" }}>
            {PART_IDS.map((id) => (
              <div
                key={id}
                onClick={() => { setPartId(id); setInputVal(id); }}
                style={{
                  padding: "7px 14px", cursor: "pointer", borderBottom: "1px solid #0a2040",
                  background: partId === id ? "var(--border-light)" : "transparent",
                  fontFamily: "monospace", fontSize: 12,
                  color: partId === id ? "var(--fg)" : "var(--muted)",
                }}
              >
                {id}
              </div>
            ))}
          </div>
        </div>

        {/* 3D viewport */}
        <div style={{ flex: 1, position: "relative" }}>
          <LDrawViewer key={partId} partId={partId} />
          <div style={{
            position: "absolute", bottom: 12, left: 14,
            fontSize: 11, color: "rgba(255,255,255,0.3)", fontFamily: "monospace",
          }}>
            drag to orbit · scroll to zoom
          </div>
          <div style={{
            position: "absolute", top: 12, left: 14,
            fontFamily: "monospace", fontSize: 13, color: "var(--blue)", fontWeight: 700,
          }}>
            {partId}
          </div>
        </div>

      </div>
    </div>
  );
}
