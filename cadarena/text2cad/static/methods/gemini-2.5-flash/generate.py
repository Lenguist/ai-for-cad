#!/usr/bin/env python3
"""Generate outputs for gemini-2.5-flash on the CAD Arena static benchmark."""
import subprocess, sys
from pathlib import Path

if __name__ == "__main__":
    runner = Path(__file__).resolve().parents[2] / "run.py"
    method = Path(__file__).parent.name
    subprocess.run(
        [sys.executable, str(runner), "--method", method, *sys.argv[1:]],
        check=True,
    )
