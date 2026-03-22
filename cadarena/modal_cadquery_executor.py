"""
Modal web endpoint: execute CadQuery code → return STL as base64.

Deploy:
    modal deploy cadarena/modal_cadquery_executor.py

Test:
    curl -X POST <endpoint_url> \
      -H "Content-Type: application/json" \
      -d '{"code": "import cadquery as cq\nresult = cq.Workplane(\"XY\").box(10, 10, 10)"}'

Returns:
    { stlBase64: string | null, error: string | null, syntaxValid: bool }
"""

import modal

app = modal.App("cad-arena-executor")

# CadQuery requires conda — it has complex OCC dependencies
image = (
    modal.Image.micromamba(python_version="3.11")
    .micromamba_install(
        "cadquery=2.4.0",
        channels=["cadquery", "conda-forge"],
    )
)


@app.function(image=image, timeout=60, memory=2048)
@modal.web_endpoint(method="POST")
def execute(item: dict) -> dict:
    import ast
    import base64
    import os
    import tempfile
    import traceback
    import types

    import cadquery as cq

    code = item.get("code", "").strip()
    if not code:
        return {"stlBase64": None, "error": "No code provided", "syntaxValid": False}

    # ── 1. Syntax check ────────────────────────────────────────────────────────
    try:
        ast.parse(code)
    except SyntaxError as e:
        return {"stlBase64": None, "error": f"SyntaxError: {e}", "syntaxValid": False}

    # ── 2. Execute ─────────────────────────────────────────────────────────────
    try:
        # Wrap exporters as no-op so models that embed hardcoded export()
        # calls (e.g. Text-to-CadQuery artifacts) don't crash execution.
        cq_safe = types.SimpleNamespace(
            **{k: getattr(cq, k) for k in dir(cq) if not k.startswith("__")}
        )
        cq_safe.exporters = types.SimpleNamespace(export=lambda *a, **kw: None)

        exec_globals = {"cq": cq_safe}
        exec(code, exec_globals)

        # Restore real cq for our own export below
        exec_globals["cq"] = cq

        # Find the result — try standard name first, then common fallbacks
        res = exec_globals.get("result")
        if res is None:
            for name in (
                "assembly", "part_1", "part_2", "model", "shape",
                "solid", "body", "plate", "bracket", "gear", "bolt", "spring",
            ):
                if name in exec_globals:
                    res = exec_globals[name]
                    break

        if res is None:
            return {
                "stlBase64": None,
                "error": "No result variable found after execution",
                "syntaxValid": True,
            }

        # ── 3. Export to STL ───────────────────────────────────────────────────
        with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as f:
            stl_path = f.name

        cq.exporters.export(res, stl_path)
        stl_bytes = open(stl_path, "rb").read()
        os.unlink(stl_path)

        if len(stl_bytes) < 100:
            return {
                "stlBase64": None,
                "error": "STL output too small — geometry may be empty",
                "syntaxValid": True,
            }

        return {
            "stlBase64": base64.b64encode(stl_bytes).decode(),
            "error": None,
            "syntaxValid": True,
        }

    except Exception as e:
        return {
            "stlBase64": None,
            "error": f"{e}\n{traceback.format_exc()}",
            "syntaxValid": True,
        }
