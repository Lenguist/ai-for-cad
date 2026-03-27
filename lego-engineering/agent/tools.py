"""
tools.py — Agent tool functions for MechE-Claude Phase 1

These are the Python functions Claude Code calls to build LEGO assemblies.
The assembly state lives in workspace/assembly.json.
The compiled LDraw output is written to workspace/assembly.ldr (website reads this).

Usage:
    from agent.tools import place, remove, inspect, save, simulate, feedback

All tools return structured dicts so Claude can reason about errors.
"""

import json
import os
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from compiler.validator_semantic import validate as semantic_validate
from compiler.validator_physical import validate as physical_validate
from compiler.compiler import compile_assembly

WORKSPACE = ROOT / "agent" / "workspace"
ASSEMBLY_JSON = WORKSPACE / "assembly.json"
ASSEMBLY_LDR = WORKSPACE / "assembly.ldr"
SIM_RESULT = WORKSPACE / "sim_result.json"
FEEDBACK_FILE = WORKSPACE / "feedback.txt"
PARTS_PATH = ROOT / "parts" / "bricks.json"

# Also write LDraw to site public dir so website can serve it directly
SITE_PUBLIC_LDR = ROOT / "site" / "public" / "workspace" / "assembly.ldr"
SITE_PUBLIC_SIM = ROOT / "site" / "public" / "workspace" / "sim_result.json"
# Written by save() AFTER the LDR — this is what the website polls to refresh
SITE_PUBLIC_READY = ROOT / "site" / "public" / "workspace" / "ready.json"


# ──────────────────────────────────────────────────────────────────────────────
# Internal state management
# ──────────────────────────────────────────────────────────────────────────────

def _load_assembly() -> dict:
    if ASSEMBLY_JSON.exists():
        with open(ASSEMBLY_JSON) as f:
            return json.load(f)
    return {"bricks": []}


def _save_assembly(spec: dict):
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    with open(ASSEMBLY_JSON, "w") as f:
        json.dump(spec, f, indent=2)


def _load_parts_db() -> dict:
    with open(PARTS_PATH) as f:
        return json.load(f)


# ──────────────────────────────────────────────────────────────────────────────
# Public tool functions
# ──────────────────────────────────────────────────────────────────────────────

def search_parts(query: str) -> list[dict]:
    """
    Search the parts database by name, type, or dimension.

    Args:
        query: fuzzy search string, e.g. "2x4 brick", "plate", "1x"

    Returns:
        List of matching parts with their specs.

    Example:
        search_parts("2x4")
        # → [{"id": "2x4", "description": "Brick 2x4", "width_studs": 2, ...}]
    """
    parts_db = _load_parts_db()
    q = query.lower()
    results = []
    for part_id, part_def in parts_db.items():
        if (q in part_id.lower() or
                q in part_def.get("description", "").lower() or
                q in part_def.get("height_type", "").lower()):
            results.append({"id": part_id, **part_def})
    return results


def get_part(part_id: str) -> dict | None:
    """
    Get full spec for a part by ID.

    Args:
        part_id: exact part ID, e.g. "2x4", "plate-1x2"

    Returns:
        Part spec dict, or None if not found.
    """
    parts_db = _load_parts_db()
    if part_id in parts_db:
        return {"id": part_id, **parts_db[part_id]}
    return None


def place(spec: dict | list[dict]) -> dict:
    """
    Add one or more bricks to the current assembly.

    Args:
        spec: single brick dict or list of brick dicts.
              Each brick: {"id": str, "type": str, "pos": [x, y, layer], "rot": 0, "color": 4}
              - id: unique brick identifier (required)
              - type: brick type from parts DB (e.g. "2x4", "plate-1x2")
              - pos: [stud_x, stud_y, layer] — integer stud grid position
              - rot: rotation in degrees — 0, 90, 180, or 270 (default 0)
              - color: LDraw color code (default 4 = red; 1=blue, 2=green, 14=yellow, 15=white, 0=black)

    Returns:
        {"ok": True, "placed": [id, ...]} on success
        {"ok": False, "errors": [...]} on validation failure

    Example:
        place({"id": "b1", "type": "2x4", "pos": [0, 0, 0], "rot": 0, "color": 4})
        place([
            {"id": "b1", "type": "2x4", "pos": [0, 0, 0]},
            {"id": "b2", "type": "2x4", "pos": [0, 0, 1]},
        ])
    """
    if isinstance(spec, dict):
        new_bricks = [spec]
    else:
        new_bricks = list(spec)

    assembly = _load_assembly()
    existing_ids = {b.get("id") for b in assembly["bricks"]}

    # Check for duplicate IDs with existing assembly
    for brick in new_bricks:
        if brick.get("id") in existing_ids:
            return {
                "ok": False,
                "errors": [{"brick_id": brick.get("id"), "field": "id",
                             "message": f"Brick ID '{brick['id']}' already exists in assembly"}]
            }

    # Run L1 + L2 on the combined assembly
    test_assembly = {"bricks": assembly["bricks"] + new_bricks}

    l1_errors = semantic_validate(test_assembly)
    if l1_errors:
        return {"ok": False, "errors": l1_errors}

    l2_errors = physical_validate(test_assembly)
    if l2_errors:
        return {"ok": False, "errors": l2_errors}

    # Commit
    assembly["bricks"].extend(new_bricks)
    _save_assembly(assembly)

    return {"ok": True, "placed": [b.get("id") for b in new_bricks]}


def remove(brick_id: str) -> dict:
    """
    Remove a brick from the assembly by ID.

    Args:
        brick_id: the 'id' field of the brick to remove

    Returns:
        {"ok": True} or {"ok": False, "message": str}

    Example:
        remove("b3")
    """
    assembly = _load_assembly()
    before = len(assembly["bricks"])
    assembly["bricks"] = [b for b in assembly["bricks"] if b.get("id") != brick_id]

    if len(assembly["bricks"]) == before:
        return {"ok": False, "message": f"Brick '{brick_id}' not found in assembly"}

    _save_assembly(assembly)
    return {"ok": True, "removed": brick_id}


def clear() -> dict:
    """
    Clear the entire assembly (start fresh).

    Returns:
        {"ok": True, "cleared": N} where N is number of bricks removed.
    """
    assembly = _load_assembly()
    n = len(assembly["bricks"])
    _save_assembly({"bricks": []})
    if ASSEMBLY_LDR.exists():
        ASSEMBLY_LDR.unlink()
    return {"ok": True, "cleared": n}


def inspect() -> dict:
    """
    Return the current assembly state.

    Returns:
        {
          "brick_count": int,
          "bricks": [...],        # full spec of each brick
          "errors": [...],        # current L1 + L2 errors
          "ldr_written": bool,    # whether assembly.ldr exists
        }

    Example:
        state = inspect()
        print(state["brick_count"])
    """
    assembly = _load_assembly()
    bricks = assembly.get("bricks", [])

    l1_errors = semantic_validate(assembly) if bricks else []
    l2_errors = physical_validate(assembly) if bricks and not l1_errors else []
    all_errors = l1_errors + l2_errors

    return {
        "brick_count": len(bricks),
        "bricks": bricks,
        "errors": all_errors,
        "ldr_written": ASSEMBLY_LDR.exists(),
    }


def save(filename: str = "assembly.ldr") -> dict:
    """
    Compile current assembly to LDraw and write to workspace.
    The website watches this file and auto-refreshes.

    Args:
        filename: output filename (default "assembly.ldr")

    Returns:
        {"ok": True, "path": str, "brick_count": int} on success
        {"ok": False, "errors": [...]} on failure

    Example:
        save()   # writes workspace/assembly.ldr
    """
    assembly = _load_assembly()

    if not assembly.get("bricks"):
        return {"ok": False, "errors": [{"message": "Assembly is empty — nothing to save"}]}

    # Validate first
    l1_errors = semantic_validate(assembly)
    if l1_errors:
        return {"ok": False, "errors": l1_errors}

    l2_errors = physical_validate(assembly)
    if l2_errors:
        return {"ok": False, "errors": l2_errors}

    try:
        ldr_content = compile_assembly(assembly)
    except ValueError as e:
        return {"ok": False, "errors": [{"message": str(e)}]}

    out_path = WORKSPACE / filename
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        f.write(ldr_content)

    # Mirror to site public dir so website auto-refreshes
    SITE_PUBLIC_LDR.parent.mkdir(parents=True, exist_ok=True)
    SITE_PUBLIC_LDR.write_text(ldr_content)

    # Write ready.json AFTER the LDR — this is what the website polls
    import time as _time
    ready = {
        "ts": int(_time.time() * 1000),
        "brick_count": len(assembly["bricks"]),
    }
    SITE_PUBLIC_READY.write_text(json.dumps(ready))

    return {
        "ok": True,
        "path": str(out_path),
        "brick_count": len(assembly["bricks"]),
    }


def simulate(level: int = 2) -> dict:
    """
    Run validation/simulation at the requested level.

    Level 1: L1 semantic only
    Level 2: L1 + L2 physical static (default)
    Level 3: not yet implemented (kinematic — Phase 2)

    Returns:
        {
          "level": int,
          "ok": bool,
          "l1_errors": [...],
          "l2_errors": [...],   # only if level >= 2
          "summary": str,
        }

    Example:
        result = simulate(2)
        if result["ok"]:
            print("Assembly is valid!")
    """
    assembly = _load_assembly()

    if not assembly.get("bricks"):
        return {"level": level, "ok": False, "summary": "Assembly is empty",
                "l1_errors": [], "l2_errors": []}

    l1_errors = semantic_validate(assembly)

    result = {
        "level": level,
        "l1_errors": l1_errors,
        "l2_errors": [],
    }

    if level >= 2 and not l1_errors:
        result["l2_errors"] = physical_validate(assembly)

    if level >= 3:
        result["l3_note"] = "Kinematic simulation not yet implemented (Phase 2)"

    all_errors = result["l1_errors"] + result["l2_errors"]
    result["ok"] = len(all_errors) == 0

    brick_count = len(assembly.get("bricks", []))
    if result["ok"]:
        result["summary"] = f"Assembly valid — {brick_count} bricks, no errors at L{level}"
    else:
        result["summary"] = f"Assembly has {len(all_errors)} error(s) — {brick_count} bricks"

    # Write sim result to file for website
    sim_out = {
        "ok": result["ok"],
        "level": level,
        "brick_count": brick_count,
        "error_count": len(all_errors),
        "errors": all_errors,
        "summary": result["summary"],
    }
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    with open(SIM_RESULT, "w") as f:
        json.dump(sim_out, f, indent=2)
    SITE_PUBLIC_SIM.parent.mkdir(parents=True, exist_ok=True)
    SITE_PUBLIC_SIM.write_text(json.dumps(sim_out, indent=2))

    return result


def feedback() -> str | None:
    """
    Check if a human has left feedback in workspace/feedback.txt.

    Returns the feedback string, or None if no feedback waiting.

    Example:
        msg = feedback()
        if msg:
            print(f"Human says: {msg}")
            # act on feedback, then clear it
    """
    if not FEEDBACK_FILE.exists():
        return None
    content = FEEDBACK_FILE.read_text().strip()
    if not content:
        return None
    # Clear after reading so agent doesn't re-read same feedback
    FEEDBACK_FILE.write_text("")
    return content


# ──────────────────────────────────────────────────────────────────────────────
# Quick test / demo
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== MechE-Claude agent tools test ===\n")

    # Clear
    print("clear():", clear())

    # Search
    print("\nsearch_parts('2x4'):", search_parts("2x4"))
    print("search_parts('plate'):", [p["id"] for p in search_parts("plate")])

    # Place some bricks
    print("\n--- Building a simple 2-layer staircase ---")

    result = place([
        {"id": "base1", "type": "2x4", "pos": [0, 0, 0], "color": 4},
        {"id": "base2", "type": "2x4", "pos": [2, 0, 0], "color": 4},
        {"id": "step1", "type": "2x2", "pos": [0, 0, 1], "color": 1},
    ])
    print("place staircase:", result)

    # Inspect
    state = inspect()
    print(f"\ninspect(): {state['brick_count']} bricks, {len(state['errors'])} errors")

    # Simulate
    sim = simulate(2)
    print(f"\nsimulate(2): {sim['summary']}")

    # Save
    saved = save()
    print(f"\nsave(): {saved}")

    if saved["ok"]:
        print(f"\nLDraw file written to: {saved['path']}")
        ldr = Path(saved["path"]).read_text()
        print("\n--- LDraw content ---")
        print(ldr)
