"use client";

import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { LDrawLoader } from "three/examples/jsm/loaders/LDrawLoader.js";
import { LDrawConditionalLineMaterial } from "three/examples/jsm/materials/LDrawConditionalLineMaterial.js";

interface Props {
  ldrUrl: string;
  version?: number;
}

export default function AssemblyViewer({ ldrUrl, version = 0 }: Props) {
  const mountRef = useRef<HTMLDivElement>(null);
  const [status, setStatus] = useState<"loading" | "ok" | "error" | "empty">("loading");
  const [errorMsg, setErrorMsg] = useState("");

  // Auto-rotate toggle
  const [autoRotate, setAutoRotate] = useState(true);

  // Step replay state
  const [stepMode, setStepMode] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [totalSteps, setTotalSteps] = useState(0);
  const [playing, setPlaying] = useState(false);

  // Three.js objects that persist for the lifetime of this component.
  const threeRef = useRef<{
    renderer: THREE.WebGLRenderer;
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera;
    controls: OrbitControls;
    currentGroup: THREE.Group | null;
    raf: number;
    stopped: boolean;
  } | null>(null);

  // ── Effect 1: initialize Three.js once ──────────────────────────────────
  useEffect(() => {
    const el = mountRef.current;
    if (!el || threeRef.current) return;

    const w = el.clientWidth || 600;
    const h = el.clientHeight || 400;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a1628);

    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 10000);
    camera.position.set(150, 150, 350);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.1;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 1.5;

    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const dir = new THREE.DirectionalLight(0xffffff, 1.2);
    dir.position.set(200, 400, 200);
    scene.add(dir);

    // Ground grid
    const grid = new THREE.GridHelper(400, 20, 0x1a3a5a, 0x1a3a5a);
    grid.position.y = 0;
    scene.add(grid);

    const obj = { renderer, scene, camera, controls, currentGroup: null, raf: 0, stopped: false };
    threeRef.current = obj;

    const animate = () => {
      if (obj.stopped) return;
      obj.raf = requestAnimationFrame(animate);
      controls.update();
      // Filter out any null children LDrawLoader may have transiently introduced
      scene.children = scene.children.filter(Boolean);
      try {
        renderer.render(scene, camera);
      } catch {
        // Renderer disposed or scene not yet ready — stop loop
        obj.stopped = true;
      }
    };
    animate();

    const onResize = () => {
      const w2 = el.clientWidth;
      const h2 = el.clientHeight;
      if (!w2 || !h2) return;
      camera.aspect = w2 / h2;
      camera.updateProjectionMatrix();
      renderer.setSize(w2, h2);
    };
    const ro = new ResizeObserver(onResize);
    ro.observe(el);
    window.addEventListener("resize", onResize);

    return () => {
      obj.stopped = true;
      cancelAnimationFrame(obj.raf);
      ro.disconnect();
      window.removeEventListener("resize", onResize);
      renderer.dispose();
      if (el.contains(renderer.domElement)) el.removeChild(renderer.domElement);
      threeRef.current = null;
    };
  }, []); // only run once

  // ── Effect 2: reload LDraw content when ldrUrl or version changes ────────
  useEffect(() => {
    const three = threeRef.current;
    if (!three) return;

    setStatus("loading");
    setErrorMsg("");
    setStepMode(false);
    setPlaying(false);
    setCurrentStep(0);
    setTotalSteps(0);

    // Remove previous model
    if (three.currentGroup) {
      three.scene.remove(three.currentGroup);
      three.currentGroup = null;
    }

    let cancelled = false;

    const loader = new LDrawLoader();
    loader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
    loader.setPartsLibraryPath("/ldraw/");

    const url = `${ldrUrl}?v=${version}`;

    // Load color definitions first, then load the assembly
    (loader as any).preloadMaterials("/ldraw/LDConfig.ldr").then(() => {
      if (cancelled) return;

      loader.load(
        url,
        (group) => {
          if (cancelled) return;

          const box = new THREE.Box3().setFromObject(group);
          if (box.isEmpty()) {
            setStatus("empty");
            return;
          }

          const center = box.getCenter(new THREE.Vector3());
          group.position.sub(center);

          const size = box.getSize(new THREE.Vector3());
          const maxDim = Math.max(size.x, size.y, size.z);
          group.scale.setScalar(120 / maxDim);
          group.rotation.x = Math.PI;

          three.scene.add(group);
          three.currentGroup = group;

          three.camera.position.set(150, 150, 350);
          three.controls.target.set(0, 0, 0);
          three.controls.update();

          // Each top-level child of the group = one brick (one `1 ... file.dat` line)
          const n = group.children.length;
          setTotalSteps(n);
          setCurrentStep(n); // default: show all

          setStatus("ok");
        },
        undefined,
        (err) => {
          if (cancelled) return;
          console.error("AssemblyViewer load error", err);
          setErrorMsg(String(err));
          setStatus("error");
        }
      );
    });

    return () => {
      cancelled = true;
    };
  }, [ldrUrl, version]);

  // ── Effect 3: sync autoRotate with controls ──────────────────────────────
  useEffect(() => {
    const three = threeRef.current;
    if (!three) return;
    three.controls.autoRotate = autoRotate;
  }, [autoRotate]);

  // ── Effect 4: toggle brick visibility based on step ──────────────────────
  useEffect(() => {
    const group = threeRef.current?.currentGroup;
    if (!group) return;
    group.children.forEach((child, i) => {
      child.visible = !stepMode || i < currentStep;
    });
  }, [stepMode, currentStep]);

  // ── Effect 5: auto-play ───────────────────────────────────────────────────
  useEffect(() => {
    if (!playing) return;
    if (currentStep >= totalSteps) {
      setPlaying(false);
      return;
    }
    const timer = setTimeout(() => setCurrentStep((s) => s + 1), 700);
    return () => clearTimeout(timer);
  }, [playing, currentStep, totalSteps]);

  const btnStyle: React.CSSProperties = {
    background: "rgba(255,255,255,0.08)",
    border: "1px solid rgba(255,255,255,0.15)",
    color: "#ccc",
    borderRadius: 4,
    padding: "2px 8px",
    fontSize: 11,
    cursor: "pointer",
    fontFamily: "monospace",
  };

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <div ref={mountRef} style={{ width: "100%", height: "100%" }} />

      {status === "loading" && (
        <div style={{
          position: "absolute", inset: 0, display: "flex", alignItems: "center",
          justifyContent: "center", pointerEvents: "none",
        }}>
          <span style={{ fontFamily: "monospace", fontSize: 12, color: "var(--muted)" }}>
            loading assembly...
          </span>
        </div>
      )}
      {status === "error" && (
        <div style={{
          position: "absolute", inset: 0, display: "flex", flexDirection: "column",
          alignItems: "center", justifyContent: "center", background: "var(--panel)", gap: 8,
        }}>
          <span style={{ fontFamily: "monospace", fontSize: 12, color: "var(--accent)" }}>render error</span>
          <span style={{ fontSize: 11, color: "var(--muted)", maxWidth: 300, textAlign: "center" }}>{errorMsg}</span>
        </div>
      )}
      {status === "empty" && (
        <div style={{
          position: "absolute", inset: 0, display: "flex", alignItems: "center",
          justifyContent: "center", background: "var(--panel)",
        }}>
          <span style={{ fontFamily: "monospace", fontSize: 12, color: "var(--muted)" }}>empty assembly</span>
        </div>
      )}

      {/* Step replay controls */}
      {status === "ok" && totalSteps > 0 && (
        <div style={{
          position: "absolute", bottom: 8, left: 8, right: 8,
          display: "flex", alignItems: "center", gap: 6,
          background: "rgba(10,22,40,0.85)", borderRadius: 6, padding: "6px 8px",
        }}>
          <button style={{ ...btnStyle, color: autoRotate ? "#4a80b4" : "#666" }}
            onClick={() => setAutoRotate((r) => !r)}
            title="Toggle auto-rotate">
            ↻
          </button>

          <button style={btnStyle} onClick={() => {
            const next = !stepMode;
            setStepMode(next);
            setPlaying(false);
            if (next) setCurrentStep(0);
            else setCurrentStep(totalSteps);
          }}>
            {stepMode ? "final" : "replay"}
          </button>

          {stepMode && (
            <>
              <button style={btnStyle} onClick={() => { setPlaying(false); setCurrentStep(0); }}>⏮</button>
              <button style={btnStyle} onClick={() => setCurrentStep((s) => Math.max(0, s - 1))}>◀</button>
              <button style={{ ...btnStyle, color: playing ? "#4caf50" : "#ccc" }}
                onClick={() => {
                  if (playing) { setPlaying(false); }
                  else { if (currentStep >= totalSteps) setCurrentStep(0); setPlaying(true); }
                }}>
                {playing ? "⏸" : "▶"}
              </button>
              <button style={btnStyle} onClick={() => setCurrentStep((s) => Math.min(totalSteps, s + 1))}>▶</button>
              <button style={btnStyle} onClick={() => { setPlaying(false); setCurrentStep(totalSteps); }}>⏭</button>
              <span style={{ fontFamily: "monospace", fontSize: 11, color: "var(--muted)", marginLeft: 4 }}>
                {currentStep} / {totalSteps}
              </span>
              <input
                type="range" min={0} max={totalSteps} value={currentStep}
                onChange={(e) => { setPlaying(false); setCurrentStep(Number(e.target.value)); }}
                style={{ flex: 1, accentColor: "#4a80b4" }}
              />
            </>
          )}
        </div>
      )}
    </div>
  );
}
