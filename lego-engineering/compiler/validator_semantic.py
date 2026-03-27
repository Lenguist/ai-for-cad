"""
validator_semantic.py — L1 Semantic Validator

Checks before compilation:
- Brick type exists in parts DB
- pos is a list of 3 integers
- rot is one of 0/90/180/270
- id is a string (if present)
- No duplicate IDs

Returns list of errors (empty = valid).
"""

import json
from pathlib import Path

PARTS_PATH = Path(__file__).parent.parent / "parts" / "bricks.json"
VALID_ROTS = {0, 90, 180, 270}


def load_parts():
    with open(PARTS_PATH) as f:
        return json.load(f)


def validate(assembly_spec: dict) -> list[dict]:
    """
    Validate assembly DSL spec semantically.

    Returns list of error dicts:
      {"brick_id": str, "field": str, "message": str}
    Empty list = valid.
    """
    parts_db = load_parts()
    bricks = assembly_spec.get("bricks", [])
    errors = []

    if not isinstance(bricks, list):
        return [{"brick_id": None, "field": "bricks", "message": "'bricks' must be a list"}]

    if len(bricks) == 0:
        return [{"brick_id": None, "field": "bricks", "message": "Assembly has no bricks"}]

    seen_ids = set()

    for i, brick in enumerate(bricks):
        brick_id = brick.get("id", f"[index {i}]")

        # Duplicate ID check
        if "id" in brick:
            if brick["id"] in seen_ids:
                errors.append({
                    "brick_id": brick_id,
                    "field": "id",
                    "message": f"Duplicate brick ID '{brick_id}'"
                })
            seen_ids.add(brick["id"])

        # Type check
        part_type = brick.get("type")
        if part_type is None:
            errors.append({"brick_id": brick_id, "field": "type", "message": "Missing 'type'"})
        elif part_type not in parts_db:
            known = ", ".join(sorted(parts_db.keys()))
            errors.append({
                "brick_id": brick_id,
                "field": "type",
                "message": f"Unknown brick type '{part_type}'. Known types: {known}"
            })

        # Pos check
        pos = brick.get("pos")
        if pos is None:
            errors.append({"brick_id": brick_id, "field": "pos", "message": "Missing 'pos'"})
        elif not isinstance(pos, list) or len(pos) != 3:
            errors.append({"brick_id": brick_id, "field": "pos", "message": "'pos' must be [stud_x, stud_y, layer] (list of 3)"})
        else:
            for j, v in enumerate(pos):
                if not isinstance(v, int):
                    errors.append({
                        "brick_id": brick_id,
                        "field": f"pos[{j}]",
                        "message": f"pos[{j}] must be an integer, got {type(v).__name__}"
                    })
            if isinstance(pos[2], int) and pos[2] < 0:
                errors.append({
                    "brick_id": brick_id,
                    "field": "pos[2]",
                    "message": f"layer (pos[2]) must be >= 0, got {pos[2]}"
                })

        # Rot check
        rot = brick.get("rot", 0)
        if rot not in VALID_ROTS:
            errors.append({
                "brick_id": brick_id,
                "field": "rot",
                "message": f"'rot' must be 0, 90, 180, or 270 — got {rot}"
            })

        # Color check (optional)
        color = brick.get("color")
        if color is not None and not isinstance(color, int):
            errors.append({
                "brick_id": brick_id,
                "field": "color",
                "message": f"'color' must be an integer (LDraw color code), got {type(color).__name__}"
            })

    return errors


def validate_file(path: str) -> dict:
    """Validate a JSON file. Returns {"ok": bool, "errors": list}"""
    with open(path) as f:
        spec = json.load(f)
    errors = validate(spec)
    return {"ok": len(errors) == 0, "errors": errors}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python validator_semantic.py <assembly.json>")
        sys.exit(1)
    result = validate_file(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["ok"] else 1)
