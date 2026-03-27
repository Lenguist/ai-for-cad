"""
validator_physical.py — L2 Physical Validator (Static)

Checks after DSL parsing (before LDraw compilation):
1. Overlap: no two bricks occupy the same stud cells at the same layer
2. Support: every non-ground brick has at least one stud supported by a brick below

Works in stud grid space. Rotation is taken into account for footprint.

Footprint cell = (stud_x, stud_y, layer) integer tuple.
A brick occupies cells from its pos corner according to its width/depth after rotation.
"""

import json
from pathlib import Path

PARTS_PATH = Path(__file__).parent.parent / "parts" / "bricks.json"


def load_parts():
    with open(PARTS_PATH) as f:
        return json.load(f)


def get_footprint(part_def: dict, pos: list, rot: int) -> set[tuple]:
    """
    Return set of (stud_x, stud_y) occupied by this brick at its base layer.
    pos = [stud_x, stud_y, layer], rot = 0/90/180/270
    """
    w = part_def["width_studs"]
    d = part_def["depth_studs"]
    sx, sy = pos[0], pos[1]
    cells = set()

    # pos is always the min-stud corner regardless of rotation.
    # rot=0/180: w studs in X, d studs in Y
    # rot=90/270: d studs in X, w studs in Y (axes swap)
    if rot in (0, 180):
        for dx in range(w):
            for dy in range(d):
                cells.add((sx + dx, sy + dy))
    else:  # rot == 90 or rot == 270
        for dx in range(w):
            for dy in range(d):
                cells.add((sx + dy, sy + dx))

    return cells


def get_occupied_layers(part_def: dict, layer: int) -> list[int]:
    """
    Return list of layer indices this brick occupies (inclusive).
    Bricks = 3 plate-heights per brick (by LEGO convention: 1 brick = 3 plates).
    But in our layer system, each unit is one brick-height OR one plate-height,
    depending on the part type. For overlap purposes we track integer layer indices.
    Currently each brick occupies exactly 1 layer slot (its declared layer).
    """
    return [layer]


def validate(assembly_spec: dict) -> list[dict]:
    """
    Validate assembly physically.

    Returns list of error dicts:
      {"brick_id": str, "type": "overlap"|"unsupported", "message": str}
    """
    parts_db = load_parts()
    bricks = assembly_spec.get("bricks", [])
    errors = []

    # Build occupancy map: (stud_x, stud_y, layer) -> brick_id
    occupancy: dict[tuple, str] = {}

    brick_data = []
    for brick in bricks:
        brick_id = brick.get("id", "?")
        part_type = brick.get("type", "")
        pos = brick.get("pos", [0, 0, 0])
        rot = brick.get("rot", 0)

        if part_type not in parts_db:
            continue  # L1 already caught this
        part_def = parts_db[part_type]

        footprint = get_footprint(part_def, pos, rot)
        layer = pos[2]

        brick_data.append({
            "id": brick_id,
            "footprint": footprint,
            "layer": layer,
            "part_def": part_def,
        })

        # Check overlap
        for (fx, fy) in footprint:
            key = (fx, fy, layer)
            if key in occupancy:
                other_id = occupancy[key]
                errors.append({
                    "brick_id": brick_id,
                    "type": "overlap",
                    "message": f"Brick '{brick_id}' overlaps with '{other_id}' at stud ({fx}, {fy}) layer {layer}"
                })
            else:
                occupancy[key] = brick_id

    # Check support: every non-ground brick needs at least 1 stud covered by a brick at layer-1
    for bd in brick_data:
        if bd["layer"] == 0:
            continue  # ground level is always supported

        layer_below = bd["layer"] - 1
        has_support = False
        for (fx, fy) in bd["footprint"]:
            if (fx, fy, layer_below) in occupancy:
                has_support = True
                break

        if not has_support:
            errors.append({
                "brick_id": bd["id"],
                "type": "unsupported",
                "message": (
                    f"Brick '{bd['id']}' at layer {bd['layer']} has no support from below "
                    f"(footprint spans {sorted(bd['footprint'])}, nothing at layer {layer_below})"
                )
            })

    return errors


def validate_file(path: str) -> dict:
    with open(path) as f:
        spec = json.load(f)
    errors = validate(spec)
    return {"ok": len(errors) == 0, "errors": errors}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python validator_physical.py <assembly.json>")
        sys.exit(1)
    result = validate_file(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["ok"] else 1)
