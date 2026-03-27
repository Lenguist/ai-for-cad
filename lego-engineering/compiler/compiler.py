"""
compiler.py — Phase 1 DSL → LDraw compiler

DSL format:
{
  "bricks": [
    {"id": "b1", "type": "2x4", "pos": [stud_x, stud_y, layer], "rot": 0, "color": 4}
  ]
}

Coordinate system:
  pos[0] = stud_x  (increases right)
  pos[1] = stud_y  (increases forward/depth)
  pos[2] = layer   (0 = ground, increases up)
  rot = 0/90/180/270 degrees (rotation around vertical axis)

LDraw units:
  1 stud = 20 LDraw units (horizontal)
  1 brick height = 24 LDraw units
  1 plate height = 8 LDraw units
  LDraw Y is vertical, negative = up (we negate before writing)
"""

import json
import math
import os
from pathlib import Path

PARTS_PATH = Path(__file__).parent.parent / "parts" / "bricks.json"

# LDraw unit constants
STUD = 20       # horizontal: 1 stud = 20 LDraw units
BRICK_H = 24    # 1 brick height in LDraw units
PLATE_H = 8     # 1 plate height in LDraw units

# LDraw rotation matrices for 0/90/180/270 around Y axis
# Row format: [a, b, c, d, e, f, g, h, i] = 3x3 matrix row-major
ROTATION_MATRICES = {
    0:   "1 0 0 0 1 0 0 0 1",
    90:  "0 0 1 0 1 0 -1 0 0",
    180: "-1 0 0 0 1 0 0 0 -1",
    270: "0 0 -1 0 1 0 1 0 0",
}

def load_parts():
    with open(PARTS_PATH) as f:
        return json.load(f)

def get_height_lu(part_def):
    """Return height in LDraw units for a part."""
    if part_def["height_type"] == "brick":
        return BRICK_H
    elif part_def["height_type"] == "plate":
        return PLATE_H
    return BRICK_H

def compile_assembly(assembly_spec: dict) -> str:
    """
    Compile a DSL assembly spec to LDraw format string.

    Returns LDraw file content as a string.
    Raises ValueError if spec is invalid.
    """
    parts_db = load_parts()
    bricks = assembly_spec.get("bricks", [])

    if not bricks:
        raise ValueError("Assembly has no bricks")

    lines = [
        "0 Compiled by MechE-Claude compiler",
        "0 Name: assembly.ldr",
        "0 Author: MechE-Claude",
        "",
    ]

    # Accumulate heights per column to track layer boundaries
    # (not needed for compilation, but useful for future reference)

    for brick in bricks:
        part_type = brick["type"]
        brick_id = brick.get("id", "?")

        if part_type not in parts_db:
            raise ValueError(f"Unknown brick type '{part_type}' (id={brick_id})")

        part_def = parts_db[part_type]
        pos = brick["pos"]
        rot = brick.get("rot", 0)
        color = brick.get("color", 4)  # default color 4 = red

        if rot not in ROTATION_MATRICES:
            raise ValueError(f"Invalid rotation {rot} for brick '{brick_id}' — must be 0/90/180/270")

        stud_x, stud_y, layer = pos

        # Convert DSL coords to LDraw units
        # LDraw origin: X right, Z forward, Y up (negative = up in LDraw convention)
        ldraw_x = stud_x * STUD
        ldraw_z = stud_y * STUD

        # Y: compute cumulative height for this layer
        # Layer 0 = ground level (y=0 in our system, but LDraw Y is negative-up)
        # We compute based on layer index, assuming all bricks below are same type.
        # More sophisticated: validate at L2. For now, use layer * BRICK_H.
        height_lu = get_height_lu(part_def)
        ldraw_y = -(layer * BRICK_H)  # negative because LDraw Y goes down

        # Center offset: LDraw places bricks at their geometric center.
        # A 2x4 brick has its center at stud (0.5, 1.5) relative to bottom-left stud.
        # Our DSL pos is the bottom-left (min stud) corner.
        w = part_def["width_studs"]
        d = part_def["depth_studs"]

        # Without rotation: center_x = pos_x + (w-1)/2 * STUD, center_z = pos_y + (d-1)/2 * STUD
        # With rotation, we rotate the offset vector.
        half_w = (w - 1) / 2 * STUD
        half_d = (d - 1) / 2 * STUD

        rot_rad = math.radians(rot)
        # Use absolute trig values so pos is always the min-stud corner regardless of rotation.
        # rot=0/180: brick is w studs in X, d studs in Z → center at (half_w, half_d)
        # rot=90/270: brick is d studs in X, w studs in Z → center at (half_d, half_w)
        cos_r = abs(math.cos(rot_rad))
        sin_r = abs(math.sin(rot_rad))
        offset_x = half_w * cos_r + half_d * sin_r
        offset_z = half_d * cos_r + half_w * sin_r

        center_x = ldraw_x + offset_x
        center_z = ldraw_z + offset_z
        center_y = ldraw_y  # center of brick vertically = top stud level (LDraw convention for bricks)

        rot_matrix = ROTATION_MATRICES[rot]
        ldraw_id = part_def["ldraw_id"]

        # LDraw line type 1: 1 <color> <x> <y> <z> <a> <b> <c> <d> <e> <f> <g> <h> <i> <file>
        line = f"1 {color} {center_x:.2f} {center_y:.2f} {center_z:.2f} {rot_matrix} {ldraw_id}.dat"

        lines.append(f"0 STEP  // brick {brick_id}")
        lines.append(line)

    lines.append("")
    lines.append("0 NOFILE")

    return "\n".join(lines)


def compile_file(input_path: str, output_path: str) -> dict:
    """
    Read JSON spec from input_path, compile to LDraw, write to output_path.
    Returns {"ok": True} or {"ok": False, "errors": [...]}
    """
    with open(input_path) as f:
        spec = json.load(f)

    try:
        ldr_content = compile_assembly(spec)
    except ValueError as e:
        return {"ok": False, "errors": [str(e)]}

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(ldr_content)

    return {"ok": True, "output": output_path}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python compiler.py <input.json> <output.ldr>")
        sys.exit(1)
    result = compile_file(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
