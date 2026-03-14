"""
Execute CadQuery code in an isolated subprocess and validate the result.
Falls back to syntax-only check if cadquery is not installed.
"""

import ast
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Optional


# ── Subprocess runner script (written to a temp file and executed) ─────────

_RUNNER_SCRIPT = textwrap.dedent("""
import sys, json, traceback, os

code_file  = sys.argv[1]
output_json = sys.argv[2]
stl_out    = sys.argv[3]

with open(code_file) as f:
    code = f.read()

result_data = {}

# 1. Syntax check
try:
    import ast as _ast
    _ast.parse(code)
    result_data["syntax_valid"] = True
except SyntaxError as e:
    result_data["syntax_valid"] = False
    result_data["syntax_error"] = str(e)
    with open(output_json, "w") as f:
        json.dump(result_data, f, indent=2)
    sys.exit(0)

# 2. Execution check (requires cadquery)
try:
    import cadquery as cq
    import types
    # Wrap cq.exporters.export as a no-op so models that embed export calls
    # (e.g. Text-to-CadQuery training artifacts) don't crash the executor.
    cq_wrapped = types.SimpleNamespace(**{k: getattr(cq, k) for k in dir(cq) if not k.startswith('__')})
    cq_wrapped.exporters = types.SimpleNamespace(export=lambda *a, **kw: None)
    exec_globals = {"cq": cq_wrapped}
    exec(code, exec_globals)
    # Restore real cq for our own export below
    exec_globals["cq"] = cq
    # Check for 'result', then common fallback names used by Text-to-CadQuery
    res = exec_globals.get("result")
    if res is None:
        for fallback in ("assembly", "part_1", "part_2", "model", "shape", "solid", "body", "plate", "bracket", "gear", "bolt", "spring", "elbow", "shaft"):
            if fallback in exec_globals:
                res = exec_globals[fallback]
                break
    if res is None:
        result_data["exec_valid"] = False
        result_data["exec_error"] = "No variable named 'result' found after exec()"
    else:
        result_data["exec_valid"] = True
        # Bounding box
        try:
            bb = res.val().BoundingBox()
            result_data["bbox"] = {
                "x": round(bb.xmax - bb.xmin, 3),
                "y": round(bb.ymax - bb.ymin, 3),
                "z": round(bb.zmax - bb.zmin, 3),
            }
            vol_bb = (bb.xmax-bb.xmin)*(bb.ymax-bb.ymin)*(bb.zmax-bb.zmin)
            result_data["bbox_volume_mm3"] = round(vol_bb, 3)
        except Exception as e:
            result_data["bbox_error"] = str(e)
        # STL export
        try:
            import cadquery as cq
            cq.exporters.export(res, stl_out)
            result_data["stl_exported"] = True
            result_data["stl_size_bytes"] = os.path.getsize(stl_out)
        except Exception as e:
            result_data["stl_error"] = str(e)
            result_data["stl_exported"] = False
except ImportError:
    result_data["exec_valid"] = None   # unknown — cadquery not installed
    result_data["note"] = "cadquery_not_installed_syntax_only"
except Exception as e:
    result_data["exec_valid"] = False
    result_data["exec_error"] = str(e)
    result_data["traceback"] = traceback.format_exc()

with open(output_json, "w") as f:
    json.dump(result_data, f, indent=2)
""")


def validate_cadquery(
    code: str,
    run_dir: Path,
    filename_stem: str,
    timeout: int = 45,
) -> dict:
    """
    Execute CadQuery code in a subprocess.

    Returns a dict with keys:
        syntax_valid    bool
        exec_valid      bool | None  (None = cadquery not installed)
        stl_exported    bool
        stl_path        str | None
        bbox            dict | None
        error           str | None
    """
    run_dir.mkdir(parents=True, exist_ok=True)

    code_file   = run_dir / f"{filename_stem}.py"
    output_json = run_dir / f"{filename_stem}_exec.json"
    stl_out     = run_dir / f"{filename_stem}.stl"
    runner_file = run_dir / "_runner.py"

    code_file.write_text(code, encoding="utf-8")
    runner_file.write_text(_RUNNER_SCRIPT, encoding="utf-8")

    try:
        proc = subprocess.run(
            [sys.executable, str(runner_file),
             str(code_file), str(output_json), str(stl_out)],
            timeout=timeout,
            capture_output=True,
            text=True,
        )
        if output_json.exists():
            with open(output_json) as f:
                data = json.load(f)
        else:
            data = {
                "syntax_valid": False,
                "exec_valid": False,
                "exec_error": f"Runner produced no output.\nstdout: {proc.stdout}\nstderr: {proc.stderr}",
            }
    except subprocess.TimeoutExpired:
        data = {
            "syntax_valid": True,
            "exec_valid": False,
            "exec_error": f"Execution timed out after {timeout}s",
        }
    except Exception as e:
        data = {"syntax_valid": False, "exec_valid": False, "exec_error": str(e)}

    # Attach STL path if exported
    if data.get("stl_exported") and stl_out.exists():
        data["stl_path"] = str(stl_out)
    else:
        data["stl_path"] = None

    return data


def validate_zoo_stl(stl_b64: Optional[str], step_b64: Optional[str],
                     run_dir: Path, filename_stem: str) -> dict:
    """Save and validate Zoo-produced STL/STEP files (stored as base64 in metadata)."""
    if not stl_b64 and not step_b64:
        return {"exec_valid": False, "exec_error": "No STL/STEP data from Zoo API"}

    import base64
    run_dir.mkdir(parents=True, exist_ok=True)

    data: dict = {"syntax_valid": True, "exec_valid": True}

    if stl_b64:
        stl_out = run_dir / f"{filename_stem}.stl"
        stl_bytes = base64.b64decode(stl_b64)
        stl_out.write_bytes(stl_bytes)
        data["stl_exported"] = True
        data["stl_path"] = str(stl_out)
        data["stl_size_bytes"] = len(stl_bytes)

    if step_b64:
        step_out = run_dir / f"{filename_stem}.step"
        step_bytes = base64.b64decode(step_b64)
        step_out.write_bytes(step_bytes)
        data["step_exported"] = True
        data["step_path"] = str(step_out)
        data["step_size_bytes"] = len(step_bytes)

    data: dict = {
        "syntax_valid": True,   # N/A for Zoo — treat as valid
        "exec_valid": True,
        "stl_exported": True,
        "stl_path": str(stl_out),
        "stl_size_bytes": len(stl_bytes),
    }

    return data
