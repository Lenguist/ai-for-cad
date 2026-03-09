"use client";

import { useEffect, useRef } from "react";

interface STLViewerProps {
  url: string;
  width?: number;
  height?: number;
}

export default function STLViewer({ url, width = 400, height = 300 }: STLViewerProps) {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    let animFrameId: number;
    let renderer: import("three").WebGLRenderer;

    (async () => {
      const THREE = await import("three");
      const { STLLoader } = await import("three/examples/jsm/loaders/STLLoader.js");

      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x3a6a9a);

      // Camera
      const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 10000);

      // Renderer
      renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(width, height);
      renderer.setPixelRatio(window.devicePixelRatio);
      mountRef.current?.appendChild(renderer.domElement);

      // Lights
      const ambient = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambient);
      const dir1 = new THREE.DirectionalLight(0xffffff, 0.8);
      dir1.position.set(1, 2, 3);
      scene.add(dir1);
      const dir2 = new THREE.DirectionalLight(0xffffff, 0.4);
      dir2.position.set(-2, -1, -1);
      scene.add(dir2);

      // Load STL
      const loader = new STLLoader();
      loader.load(
        url,
        (geometry) => {
          geometry.computeBoundingBox();
          const box = geometry.boundingBox!;
          const center = new THREE.Vector3();
          box.getCenter(center);
          geometry.translate(-center.x, -center.y, -center.z);

          const size = new THREE.Vector3();
          box.getSize(size);
          const maxDim = Math.max(size.x, size.y, size.z);
          const dist = maxDim * 1.8;
          camera.position.set(dist * 0.7, dist * 0.5, dist * 0.7);
          camera.lookAt(0, 0, 0);

          const mat = new THREE.MeshPhongMaterial({
            color: 0xd0e4f7,
            specular: 0x888888,
            shininess: 60,
          });
          const mesh = new THREE.Mesh(geometry, mat);
          scene.add(mesh);

          // Grid helper
          const grid = new THREE.GridHelper(maxDim * 2, 10, 0xffffff, 0xffffff);
          const gridMat = grid.material as import("three").Material & { opacity: number; transparent: boolean };
          gridMat.opacity = 0.1;
          gridMat.transparent = true;
          grid.position.y = -size.z / 2;
          scene.add(grid);

          // Auto-rotate animation
          let angle = 0;
          const animate = () => {
            animFrameId = requestAnimationFrame(animate);
            angle += 0.008;
            camera.position.x = dist * 0.9 * Math.cos(angle);
            camera.position.z = dist * 0.9 * Math.sin(angle);
            camera.lookAt(0, 0, 0);
            renderer.render(scene, camera);
          };
          animate();
        },
        undefined,
        () => {
          // On error show placeholder
          renderer.render(scene, camera);
        }
      );
    })();

    return () => {
      cancelAnimationFrame(animFrameId);
      renderer?.dispose();
      if (mountRef.current && renderer?.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
    };
  }, [url, width, height]);

  return (
    <div
      ref={mountRef}
      style={{ width, height, overflow: "hidden", background: "#3a6a9a" }}
    />
  );
}
