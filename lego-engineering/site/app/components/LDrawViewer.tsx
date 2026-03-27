"use client";

import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { LDrawLoader } from "three/examples/jsm/loaders/LDrawLoader.js";
import { LDrawConditionalLineMaterial } from "three/examples/jsm/materials/LDrawConditionalLineMaterial.js";

// Map from our semantic part IDs to LDraw filenames
const LDRAW_MAP: Record<string, string> = {
  "beam-3": "32523.dat",
  "beam-5": "32316.dat",
  "beam-7": "32524.dat",
  "beam-9": "40490.dat",
  "beam-11": "32525.dat",
  "beam-15": "32278.dat",
  "gear-8t": "3647.dat",
  "gear-16t": "4019.dat",
  "gear-24t": "3648.dat",
  "gear-40t": "3649.dat",
  "gear-worm": "4716.dat",
  "rack-4": "3743.dat",
  "axle-3": "4519.dat",
  "axle-4": "3705.dat",
  "axle-5": "32073.dat",
  "axle-6": "3706.dat",
  "axle-8": "3707.dat",
  "axle-10": "3737.dat",
  "pin": "3673.dat",
  "pin-friction": "2780.dat",
  "pin-long": "6558.dat",
  "bush": "6590.dat",
  "connector-2x2": "6536.dat",
};

interface Props {
  partId: string;
}

export default function LDrawViewer({ partId }: Props) {
  const mountRef = useRef<HTMLDivElement>(null);
  const [status, setStatus] = useState<"loading" | "ok" | "error" | "unsupported">("loading");
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    const el = mountRef.current;
    if (!el) return;

    const ldrawFile = LDRAW_MAP[partId];
    if (!ldrawFile) {
      setStatus("unsupported");
      return;
    }

    setStatus("loading");

    // Scene
    const w = el.clientWidth;
    const h = el.clientHeight;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f1f3d);

    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 10000);
    camera.position.set(100, 100, 200);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.1;

    // Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const dir = new THREE.DirectionalLight(0xffffff, 1.2);
    dir.position.set(200, 300, 200);
    scene.add(dir);

    // Load LDraw part
    const loader = new LDrawLoader();
    loader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
    loader.setPath("/ldraw/");
    loader.setPartsLibraryPath("/ldraw/");
    loader.load(
      `parts/${ldrawFile}`,
      (group) => {
        // Center and scale
        const box = new THREE.Box3().setFromObject(group);
        const center = box.getCenter(new THREE.Vector3());
        group.position.sub(center);

        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const scale = 100 / maxDim;
        group.scale.setScalar(scale);

        // LDraw Y is flipped vs Three.js convention
        group.rotation.x = Math.PI;

        scene.add(group);

        // Fit camera
        camera.position.set(0, 60, 160);
        controls.target.set(0, 0, 0);
        controls.update();

        setStatus("ok");
      },
      undefined,
      (err) => {
        console.error("LDraw load error", err);
        setErrorMsg(String(err));
        setStatus("error");
      }
    );

    // Animate
    let raf: number;
    const animate = () => {
      raf = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // Resize
    const onResize = () => {
      const w2 = el.clientWidth;
      const h2 = el.clientHeight;
      camera.aspect = w2 / h2;
      camera.updateProjectionMatrix();
      renderer.setSize(w2, h2);
    };
    window.addEventListener("resize", onResize);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", onResize);
      renderer.dispose();
      el.removeChild(renderer.domElement);
    };
  }, [partId]);

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <div ref={mountRef} style={{ width: "100%", height: "100%" }} />
      {status === "loading" && (
        <div style={{
          position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center",
          flexDirection: "column", gap: 8, pointerEvents: "none",
        }}>
          <div style={{ fontSize: 12, color: "var(--muted)", fontFamily: "monospace" }}>loading...</div>
        </div>
      )}
      {status === "error" && (
        <div style={{
          position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center",
          flexDirection: "column", gap: 8, background: "var(--panel)",
        }}>
          <div style={{ fontSize: 12, color: "var(--accent)", fontFamily: "monospace" }}>render error</div>
          <div style={{ fontSize: 11, color: "var(--muted)", maxWidth: 240, textAlign: "center" }}>{errorMsg}</div>
        </div>
      )}
      {status === "unsupported" && (
        <div style={{
          position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center",
          background: "var(--panel)",
        }}>
          <div style={{ fontSize: 12, color: "var(--muted)", fontFamily: "monospace" }}>no LDraw file for this part</div>
        </div>
      )}
    </div>
  );
}
