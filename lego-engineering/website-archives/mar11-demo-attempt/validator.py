import math


def validate_assembly(assembly, parts_library):
    errors = []
    warnings = []

    parts = assembly.get("parts", [])
    if not parts:
        errors.append("Assembly has no parts.")
        return errors, warnings

    # Check duplicate IDs
    ids = [p.get("id") for p in parts]
    seen = set()
    for id_ in ids:
        if not id_:
            errors.append("A part is missing an 'id' field.")
        elif id_ in seen:
            errors.append(f"Duplicate part ID: '{id_}'")
        seen.add(id_)

    # Check each part
    valid_parts = []
    for part in parts:
        part_id = part.get("id", "?")
        part_type = part.get("type", "")
        pos = part.get("pos", None)
        axis = part.get("axis", "x")

        if not part_type:
            errors.append(f"Part '{part_id}': missing 'type'.")
            continue

        if part_type not in parts_library:
            errors.append(
                f"Part '{part_id}': unknown type '{part_type}'. "
                f"Available types: {', '.join(sorted(parts_library.keys()))}"
            )
            continue

        if pos is None:
            errors.append(f"Part '{part_id}': missing 'pos'.")
            continue

        if not isinstance(pos, list) or len(pos) != 3:
            errors.append(f"Part '{part_id}': 'pos' must be [x, y, z] list.")
            continue

        if axis not in ("x", "y", "z"):
            errors.append(f"Part '{part_id}': 'axis' must be 'x', 'y', or 'z'.")
            continue

        valid_parts.append(part)

    if errors:
        return errors, warnings

    # Overlap detection (bounding box per part, in stud units)
    occupied = {}  # cell tuple -> part_id
    for part in valid_parts:
        part_id = part["id"]
        spec = parts_library[part["type"]]
        cells = get_occupied_cells(spec, part["pos"], part["axis"])
        for cell in cells:
            key = tuple(cell)
            if key in occupied:
                warnings.append(
                    f"Possible overlap: '{part_id}' and '{occupied[key]}' at {list(key)}"
                )
            else:
                occupied[key] = part_id

    return errors, warnings


def get_occupied_cells(spec, pos, axis):
    """Return list of integer grid cells [x,y,z] the part occupies."""
    category = spec.get("category", "")
    px, py, pz = int(pos[0]), int(pos[1]), int(pos[2])

    if category in ("beam", "axle", "pin"):
        length = spec.get("length", 1)
        cells = []
        for i in range(length):
            if axis == "x":
                cells.append([px + i, py, pz])
            elif axis == "y":
                cells.append([px, py + i, pz])
            else:
                cells.append([px, py, pz + i])
        return cells

    elif category == "rack":
        length = spec.get("length", 4)
        cells = []
        for i in range(length):
            if axis == "x":
                cells.append([px + i, py, pz])
            elif axis == "y":
                cells.append([px, py + i, pz])
            else:
                cells.append([px, py, pz + i])
        return cells

    elif category == "gear":
        # Gears occupy a disk — approximate as center cell only for overlap
        return [[px, py, pz]]

    else:
        return [[px, py, pz]]


def compute_kinematics(assembly, parts_library):
    """Analyse gear meshes, compute ratios, detect motion conversion."""
    parts = assembly.get("parts", [])
    result = {}

    # Collect gears and racks
    gears = []
    racks = []
    for part in parts:
        pt = part.get("type", "")
        if pt not in parts_library:
            continue
        spec = parts_library[pt]
        cat = spec.get("category")
        if cat == "gear":
            gears.append({
                "id": part["id"],
                "type": pt,
                "teeth": spec["teeth"],
                "radius": spec["radius_studs"],
                "pos": part.get("pos", [0, 0, 0]),
                "axis": part.get("axis", "x"),
            })
        elif cat == "rack":
            racks.append({
                "id": part["id"],
                "type": pt,
                "pos": part.get("pos", [0, 0, 0]),
                "axis": part.get("axis", "x"),
                "length": spec.get("length", 4),
            })

    # Find meshing gear pairs
    gear_pairs = []
    for i in range(len(gears)):
        for j in range(i + 1, len(gears)):
            g1, g2 = gears[i], gears[j]
            # Only mesh if axes are parallel
            if g1["axis"] != g2["axis"]:
                continue
            dist = euclidean(g1["pos"], g2["pos"])
            expected = g1["radius"] + g2["radius"]
            if abs(dist - expected) < 0.75:
                ratio = g2["teeth"] / g1["teeth"]
                gear_pairs.append({
                    "gear1": g1["id"],
                    "gear2": g2["id"],
                    "teeth1": g1["teeth"],
                    "teeth2": g2["teeth"],
                    "ratio": round(ratio, 3),
                    "ratio_str": f"{g2['teeth']}:{g1['teeth']}",
                })

    if gear_pairs:
        result["gear_pairs"] = gear_pairs
        # Overall ratio: product of driven/driving through the chain
        if len(gear_pairs) == 1:
            r = gear_pairs[0]["ratio"]
            result["summary"] = (
                f"Single gear pair: {gear_pairs[0]['ratio_str']} "
                f"({'speed up' if r < 1 else 'speed down'}, ratio {r:.2f}x)"
            )
        else:
            result["summary"] = f"{len(gear_pairs)} gear pair(s) detected."

    # Detect rack-and-pinion (gear near a rack)
    rack_pinion = []
    for rack in racks:
        for gear in gears:
            dist = euclidean_perpendicular(gear["pos"], rack["pos"], rack["axis"])
            if dist is not None and abs(dist - gear["radius"]) < 0.75:
                rack_pinion.append({
                    "gear": gear["id"],
                    "rack": rack["id"],
                    "note": f"Gear '{gear['id']}' ({gear['teeth']}T) drives rack '{rack['id']}' → rotational → linear motion",
                })

    if rack_pinion:
        result["rack_pinion"] = rack_pinion
        result["motion_type"] = "Rotational → Linear (rack and pinion)"

    if not gear_pairs and not rack_pinion and gears:
        result["summary"] = "Gears present but no meshing pairs detected. Check positions and axes."

    # Detect motors
    motors = []
    for part in parts:
        pt = part.get("type", "")
        if pt not in parts_library:
            continue
        spec = parts_library[pt]
        if spec.get("category") == "motor":
            motors.append({
                "id": part["id"],
                "type": pt,
                "rpm_no_load": spec.get("rpm_no_load", 0),
                "stall_torque_ncm": spec.get("stall_torque_ncm", 0),
                "rated_power_w": spec.get("rated_power_w", 0),
                "pos": part.get("pos", [0, 0, 0]),
                "axis": part.get("axis", "y"),
            })
    if motors:
        result["motors"] = motors

    return result


def euclidean(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def euclidean_perpendicular(gear_pos, rack_pos, rack_axis):
    """Distance from gear center to rack center line, perpendicular to rack axis."""
    gx, gy, gz = gear_pos
    rx, ry, rz = rack_pos
    if rack_axis == "x":
        return math.sqrt((gy - ry) ** 2 + (gz - rz) ** 2)
    elif rack_axis == "y":
        return math.sqrt((gx - rx) ** 2 + (gz - rz) ** 2)
    else:
        return math.sqrt((gx - rx) ** 2 + (gy - ry) ** 2)
