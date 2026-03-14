#!/usr/bin/env python3
"""Generate outputs for scadlm on the CAD Arena static benchmark.

ScadLM uses an LLM to generate OpenSCAD code. No GPU required.
Requires ANTHROPIC_API_KEY or OPENAI_API_KEY (uses Claude Sonnet by default).
"""
import subprocess, sys
from pathlib import Path

if __name__ == "__main__":
    runner = Path(__file__).resolve().parents[2] / "run.py"
    method = Path(__file__).parent.name
    subprocess.run(
        [sys.executable, str(runner), "--method", method, *sys.argv[1:]],
        check=True,
    )
