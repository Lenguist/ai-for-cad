"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { LDrawLoader } from "three/examples/jsm/loaders/LDrawLoader.js";
import { LDrawConditionalLineMaterial } from "three/examples/jsm/materials/LDrawConditionalLineMaterial.js";

interface Props {
  /** URL to the .ldr file to render. Re-renders on change. */
  ldrUrl: string;
  /** Cache-bust key — increment to force reload even if url is same */
  version?: number;
}

export default function AssemblyViewer({ ldrUrl, version = 0 }: Props) {
  const mountRef = useRef<HTMLDivElement>(null);
  const [status, setStatus] = useState<"loading" | "ok" | "error" | "empty">("loading");
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    const el = mountRef.current;
    if (!el) return;

    setStatus("loading");
    setErrorMsg("");

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

    const loader = new LDrawLoader();
    loader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
    loader.setPath("/ldraw/");
    loader.setPartsLibraryPath("/ldraw/");

    // Append cache-buster to URL
    const url = `${ldrUrl}?v=${version}`;

    loader.load(
      url,
      (group) => {
        const box = new THREE.Box3().setFromObject(group);
        if (box.isEmpty()) {
          setStatus("empty");
          return;
        }

        const center = box.getCenter(new THREE.Vector3());
        group.position.sub(center);

        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const scale = 120 / maxDim;
        group.scale.setScalar(scale);

        // LDraw Y is flipped
        group.rotation.x = Math.PI;

        scene.add(group);
        camera.position.set(150, 150, 350);
        controls.target.set(0, 0, 0);
        controls.update();
        setStatus("ok");
      },
      undefined,
      (err) => {
        console.error("AssemblyViewer load error", err);
        setErrorMsg(String(err));
        setStatus("error");
      }
    );

    let raf: number;
    const animate = () => {
      raf = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

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
      if (el.contains(renderer.domElement)) {
        el.removeChild(renderer.domElement);
      }
    };
  }, [ldrUrl, version]);

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
    </div>
  );
}
