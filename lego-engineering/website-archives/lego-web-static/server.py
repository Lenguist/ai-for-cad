#!/usr/bin/env python3
"""
server.py — Local dev server for lego-web-static.
Serves index.html and exposes /physics API using physics.py.

Usage:
    python server.py
Then open http://localhost:8765
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from pathlib import Path

# Add mar11-demo-attempt to path for physics + validator imports
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "mar11-demo-attempt"))

from physics import compile_and_simulate
from validator import validate_assembly

PARTS_FILE = ROOT / "mar11-demo-attempt" / "parts_library.json"
with open(PARTS_FILE) as f:
    PARTS_LIBRARY = json.load(f)

STATIC_DIR = Path(__file__).parent


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"  {self.command} {self.path} → {args[1] if len(args) > 1 else ''}")

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html") or path.startswith("/library") or path.startswith("/studio"):
            self._serve_file(STATIC_DIR / "index.html", "text/html")
        elif path == "/ldraw-bundle":
            # One-shot bundle: all primitives + sub-parts as JSON for cache preloading
            bundle = {}
            ldraw = STATIC_DIR / "ldraw"
            for f in (ldraw / "p").iterdir():
                if f.is_file():
                    bundle[f.name.lower()] = f.read_text(errors="ignore")
            p48 = ldraw / "p" / "48"
            if p48.exists():
                for f in p48.iterdir():
                    if f.is_file():
                        bundle["48/" + f.name.lower()] = f.read_text(errors="ignore")
            parts_s = ldraw / "parts" / "s"
            if parts_s.exists():
                for f in parts_s.iterdir():
                    if f.is_file():
                        bundle["s/" + f.name.lower()] = f.read_text(errors="ignore")
            self._json(bundle)
        elif path.startswith("/ldraw/"):
            # Serve LDraw part files
            rel = path[len("/ldraw/"):]
            local = STATIC_DIR / "ldraw" / rel
            if local.exists():
                self._serve_file(local, "text/plain")
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/physics":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                assembly = json.loads(body)
                errors, warnings = validate_assembly(assembly, PARTS_LIBRARY)
                kinematics = compile_and_simulate(assembly, PARTS_LIBRARY)
                response = {
                    "ok": True,
                    "validation_errors": errors,
                    "validation_warnings": warnings,
                    "kinematics": kinematics,
                }
            except Exception as e:
                response = {"ok": False, "error": str(e)}
            self._json(response)
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def _serve_file(self, path, content_type):
        try:
            data = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(data))
            self._cors_headers()
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def _raw(self, code, content_type, data):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(data))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(data)

    def _json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(data))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(data)

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle each request in a new thread."""

if __name__ == "__main__":
    port = 8765
    print(f"Serving at http://localhost:{port}")
    print(f"  Static: {STATIC_DIR}/index.html")
    print(f"  Physics API: POST http://localhost:{port}/physics")
    ThreadedHTTPServer(("localhost", port), Handler).serve_forever()
