"""
modal_tools.py — Modal web endpoint for BrickGPT tool execution.

Replaces the local python3 subprocess with a stateless HTTP endpoint.
The Next.js route passes {fn, args, assembly} and gets back
{result, assembly, ldr_content, sim_result}.

Deploy:
    cd lego-engineering
    modal deploy agent/modal_tools.py

Then set MODAL_TOOL_URL=<deployed url> in Vercel env vars.
"""

import json
from pathlib import Path
import modal

app = modal.App("brickgpt-tools")

ROOT = Path(__file__).parent.parent  # lego-engineering/

# Mount compiler logic and parts DB into the container
compiler_mount = modal.Mount.from_local_dir(
    str(ROOT / "compiler"),
    remote_path="/app/compiler",
)
parts_mount = modal.Mount.from_local_dir(
    str(ROOT / "parts"),
    remote_path="/app/parts",
)


@app.function(mounts=[compiler_mount, parts_mount], keep_warm=1)
@modal.web_endpoint(method="POST")
def run_tool(request: dict) -> dict:
    """
    Stateless tool execution. Assembly state is passed in and returned out —
    no filesystem reads/writes. LDR content is returned as a string on save().
    """
    import sys
    sys.path.insert(0, "/app")
    from compiler.validator_semantic import validate as sem_validate
    from compiler.validator_physical import validate as phys_validate
    from compiler.compiler import compile_assembly

    fn = request.get("fn")
    args = request.get("args", {})
    assembly = request.get("assembly", {"bricks": []})

    result = None
    ldr_content = None
    sim_result = None

    try:
        if fn == "place":
            result, assembly = _place(args["spec"], assembly, sem_validate, phys_validate)

        elif fn == "remove":
            result, assembly = _remove(args["brick_id"], assembly)

        elif fn == "clear":
            n = len(assembly.get("bricks", []))
            assembly = {"bricks": []}
            result = {"ok": True, "cleared": n}

        elif fn == "inspect":
            result = _inspect(assembly, sem_validate, phys_validate)

        elif fn == "simulate":
            result = _simulate(args.get("level", 2), assembly, sem_validate, phys_validate)
            sim_result = result

        elif fn == "save":
            result, ldr_content, sim_result = _save(
                assembly, sem_validate, phys_validate, compile_assembly
            )

        elif fn == "search_parts":
            result = {"results": _search_parts(args["query"])}

        elif fn == "get_part":
            result = _get_part(args["part_id"])

        else:
            result = {"error": f"Unknown function: {fn}"}

    except Exception as e:
        import traceback
        result = {"error": str(e), "traceback": traceback.format_exc()}

    return {
        "result": result,
        "assembly": assembly,
        "ldr_content": ldr_content,
        "sim_result": sim_result,
    }


# ── Tool implementations (stateless) ──────────────────────────────────────────

def _load_parts() -> dict:
    with open("/app/parts/bricks.json") as f:
        return json.load(f)


def _place(spec, assembly, sem_validate, phys_validate):
    new_bricks = [spec] if isinstance(spec, dict) else list(spec)
    existing_ids = {b.get("id") for b in assembly["bricks"]}

    for brick in new_bricks:
        if brick.get("id") in existing_ids:
            return (
                {"ok": False, "errors": [{"brick_id": brick.get("id"), "field": "id",
                                          "message": f"Brick ID '{brick['id']}' already exists"}]},
                assembly,
            )

    test = {"bricks": assembly["bricks"] + new_bricks}
    l1 = sem_validate(test)
    if l1:
        return {"ok": False, "errors": l1}, assembly
    l2 = phys_validate(test)
    if l2:
        return {"ok": False, "errors": l2}, assembly

    return (
        {"ok": True, "placed": [b.get("id") for b in new_bricks]},
        {"bricks": assembly["bricks"] + new_bricks},
    )


def _remove(brick_id, assembly):
    before = len(assembly["bricks"])
    new_bricks = [b for b in assembly["bricks"] if b.get("id") != brick_id]
    if len(new_bricks) == before:
        return {"ok": False, "message": f"Brick '{brick_id}' not found"}, assembly
    return {"ok": True, "removed": brick_id}, {"bricks": new_bricks}


def _inspect(assembly, sem_validate, phys_validate):
    bricks = assembly.get("bricks", [])
    l1 = sem_validate(assembly) if bricks else []
    l2 = phys_validate(assembly) if bricks and not l1 else []
    return {
        "brick_count": len(bricks),
        "bricks": bricks,
        "errors": l1 + l2,
        "ldr_written": False,
    }


def _simulate(level, assembly, sem_validate, phys_validate):
    bricks = assembly.get("bricks", [])
    if not bricks:
        return {
            "level": level, "ok": False, "summary": "Assembly is empty",
            "l1_errors": [], "l2_errors": [], "brick_count": 0, "error_count": 0,
        }
    l1 = sem_validate(assembly)
    l2 = phys_validate(assembly) if level >= 2 and not l1 else []
    all_errors = l1 + l2
    ok = len(all_errors) == 0
    n = len(bricks)
    return {
        "level": level, "ok": ok,
        "l1_errors": l1, "l2_errors": l2,
        "brick_count": n, "error_count": len(all_errors),
        "summary": (
            f"Assembly valid — {n} bricks, no errors at L{level}"
            if ok else
            f"Assembly has {len(all_errors)} error(s) — {n} bricks"
        ),
    }


def _save(assembly, sem_validate, phys_validate, compile_assembly):
    bricks = assembly.get("bricks", [])
    if not bricks:
        return {"ok": False, "errors": [{"message": "Assembly is empty"}]}, None, None
    l1 = sem_validate(assembly)
    if l1:
        return {"ok": False, "errors": l1}, None, None
    l2 = phys_validate(assembly)
    if l2:
        return {"ok": False, "errors": l2}, None, None
    try:
        ldr = compile_assembly(assembly)
    except ValueError as e:
        return {"ok": False, "errors": [{"message": str(e)}]}, None, None
    n = len(bricks)
    sim = {
        "ok": True, "brick_count": n, "error_count": 0, "errors": [],
        "summary": f"Assembly valid — {n} bricks",
    }
    return {"ok": True, "brick_count": n}, ldr, sim


def _search_parts(query: str) -> list:
    parts_db = _load_parts()
    q = query.lower()
    return [
        {"id": pid, **pdef}
        for pid, pdef in parts_db.items()
        if q in pid.lower()
        or q in pdef.get("description", "").lower()
        or q in pdef.get("height_type", "").lower()
    ]


def _get_part(part_id: str) -> dict:
    parts_db = _load_parts()
    if part_id in parts_db:
        return {"id": part_id, **parts_db[part_id]}
    return {"error": f"Part '{part_id}' not found"}
