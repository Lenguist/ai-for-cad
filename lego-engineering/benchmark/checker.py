"""
checker.py — Evaluate success criteria for each benchmark task.

Takes:
  - task: dict from tasks.json
  - parts: list of parts from the model's assembly
  - validation_errors: list from validator.validate_assembly
  - kinematics: dict from validator.compute_kinematics
  - parts_library: dict

Returns:
  - score: 2 (full pass), 1 (partial), 0 (fail / invalid)
  - checks: list of {name, passed, note}
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mar11-demo-attempt"))


def check_task(task, assembly, validation_errors, kinematics, parts_library):
    """Return (score, checks_list)."""
    criteria = task.get("success_criteria", {})
    parts = assembly.get("parts", [])
    checks = []

    # --- 1. Valid assembly (no errors) ---
    if criteria.get("valid_assembly", False):
        passed = len(validation_errors) == 0
        checks.append({
            "name": "valid_assembly",
            "passed": passed,
            "note": "No validation errors" if passed else f"{len(validation_errors)} error(s): {validation_errors[0][:80]}"
        })
        if not passed:
            # Hard fail — don't bother checking the rest
            return 0, checks

    # --- 2. Part count checks ---
    part_count = len(parts)
    if "min_parts" in criteria:
        mn = criteria["min_parts"]
        passed = part_count >= mn
        checks.append({"name": "min_parts", "passed": passed,
                        "note": f"{part_count} parts (need ≥{mn})"})

    if "max_parts" in criteria:
        mx = criteria["max_parts"]
        passed = part_count <= mx
        checks.append({"name": "max_parts", "passed": passed,
                        "note": f"{part_count} parts (need ≤{mx})"})

    if "exact_part_count" in criteria:
        target = criteria["exact_part_count"]
        passed = part_count == target
        checks.append({"name": "exact_part_count", "passed": passed,
                        "note": f"{part_count} parts (need exactly {target})"})

    # --- 3. Part category requirements ---
    if "part_categories_required" in criteria:
        present_cats = {
            parts_library[p["type"]]["category"]
            for p in parts
            if p.get("type") in parts_library
        }
        required = criteria["part_categories_required"]
        for cat in required:
            passed = cat in present_cats
            checks.append({"name": f"category_{cat}", "passed": passed,
                            "note": f"Category '{cat}' {'present' if passed else 'MISSING'}"})

    # --- 4. Specific part type requirements ---
    if "part_types_required" in criteria:
        present_types = {p.get("type") for p in parts}
        for pt in criteria["part_types_required"]:
            passed = pt in present_types
            checks.append({"name": f"type_{pt}", "passed": passed,
                            "note": f"Part type '{pt}' {'present' if passed else 'MISSING'}"})

    # --- 5. Gear count ---
    gear_parts = [p for p in parts if p.get("type") in parts_library
                  and parts_library[p["type"]]["category"] == "gear"]
    gear_count = len(gear_parts)

    if "min_gear_count" in criteria:
        mn = criteria["min_gear_count"]
        passed = gear_count >= mn
        checks.append({"name": "min_gear_count", "passed": passed,
                        "note": f"{gear_count} gears (need ≥{mn})"})

    if "exact_gear_count" in criteria:
        target = criteria["exact_gear_count"]
        passed = gear_count == target
        checks.append({"name": "exact_gear_count", "passed": passed,
                        "note": f"{gear_count} gears (need exactly {target})"})

    # --- 6. Axle count ---
    axle_parts = [p for p in parts if p.get("type") in parts_library
                  and parts_library[p["type"]]["category"] == "axle"]
    axle_count = len(axle_parts)

    if "min_axle_count" in criteria:
        mn = criteria["min_axle_count"]
        # Axles at distinct positions along different axes count as separate axles
        # We count distinct axle positions (grouping by axis + transverse position)
        distinct_axles = count_distinct_axles(axle_parts)
        passed = distinct_axles >= mn
        checks.append({"name": "min_axle_count", "passed": passed,
                        "note": f"{distinct_axles} distinct axles (need ≥{mn})"})

    # --- 7. Gear ratio checks ---
    gear_pairs = kinematics.get("gear_pairs", [])
    computed_ratio = compute_chain_ratio(gear_pairs, parts)

    if "gear_ratio_target" in criteria:
        target = criteria["gear_ratio_target"]
        tol = criteria.get("gear_ratio_tolerance", 0.05)
        if computed_ratio is None:
            passed = False
            note = "No gear pairs detected — cannot compute ratio"
        else:
            passed = abs(computed_ratio - target) <= tol
            note = f"Ratio {computed_ratio:.3f} (target {target} ± {tol})"
        checks.append({"name": "gear_ratio_target", "passed": passed, "note": note})

    if "gear_ratio_min" in criteria:
        mn = criteria["gear_ratio_min"]
        if computed_ratio is None:
            passed = False
            note = "No gear pairs detected"
        else:
            passed = computed_ratio >= mn
            note = f"Ratio {computed_ratio:.3f} (need ≥{mn})"
        checks.append({"name": "gear_ratio_min", "passed": passed, "note": note})

    if "gear_ratio_max" in criteria:
        mx = criteria["gear_ratio_max"]
        if computed_ratio is None:
            passed = False
            note = "No gear pairs detected"
        else:
            passed = computed_ratio <= mx
            note = f"Ratio {computed_ratio:.3f} (need ≤{mx})"
        checks.append({"name": "gear_ratio_max", "passed": passed, "note": note})

    # --- 8. Motion type ---
    if "motion_type" in criteria:
        expected = criteria["motion_type"]
        rack_pinion = kinematics.get("rack_pinion", [])
        if expected == "rotational_to_linear":
            passed = len(rack_pinion) > 0
            note = f"Rack-and-pinion {'detected' if passed else 'NOT detected'}"
        else:
            passed = False
            note = f"Unknown motion_type check: {expected}"
        checks.append({"name": "motion_type", "passed": passed, "note": note})

    # --- 9. Bounding box ---
    if "bounding_box_max" in criteria:
        bbox = criteria["bounding_box_max"]
        actual_bbox = compute_bounding_box(parts, parts_library)
        if actual_bbox is None:
            passed = False
            note = "Could not compute bounding box"
        else:
            passed = all(actual_bbox[i] <= bbox[i] for i in range(3))
            note = f"BBox {actual_bbox} (max allowed {bbox})"
        checks.append({"name": "bounding_box", "passed": passed, "note": note})

    # --- Score ---
    all_checks = [c["passed"] for c in checks]
    if not all_checks:
        score = 1  # no checks defined, assume partial
    elif all(all_checks):
        score = 2
    elif any(all_checks):
        score = 1
    else:
        score = 0

    return score, checks


def compute_chain_ratio(gear_pairs, parts):
    """
    Compute the total gear ratio through the chain.
    For a compound train: multiply ratios of each stage.
    Simple heuristic: find the longest chain from input to output.
    For a single pair: trivial.
    For multiple pairs: product of ratios along the path.
    """
    if not gear_pairs:
        return None

    if len(gear_pairs) == 1:
        return gear_pairs[0]["ratio"]

    # Try to build a chain: output of one pair is input of next
    # Gear is "intermediate" if it appears as gear2 of one pair AND gear1 of another
    # Simple greedy: find pairs that don't share a driven gear
    # This handles compound trains correctly

    # Build adjacency: gear_id -> list of (partner_id, ratio)
    from collections import defaultdict
    mesh = defaultdict(list)
    for pair in gear_pairs:
        g1, g2 = pair["gear1"], pair["gear2"]
        ratio = pair["ratio"]
        mesh[g1].append((g2, ratio))
        mesh[g2].append((g1, 1.0 / ratio))

    # Find all gear IDs
    gear_ids = set()
    for pair in gear_pairs:
        gear_ids.add(pair["gear1"])
        gear_ids.add(pair["gear2"])

    # Find gears that appear in exactly 1 pair (input or output end of chain)
    degree = defaultdict(int)
    for pair in gear_pairs:
        degree[pair["gear1"]] += 1
        degree[pair["gear2"]] += 1

    endpoints = [g for g, d in degree.items() if d == 1]

    if len(endpoints) < 2:
        # All gears are intermediate (loop) or only 1 endpoint
        # Just multiply all ratios > 1 as approximation
        total = 1.0
        for pair in gear_pairs:
            if pair["ratio"] > 1:
                total *= pair["ratio"]
        return round(total, 4) if total != 1.0 else gear_pairs[0]["ratio"]

    # DFS from one endpoint to another
    start = endpoints[0]
    best_ratio = None
    best_len = 0

    def dfs(node, visited, current_ratio, depth):
        nonlocal best_ratio, best_len
        if depth > best_len:
            best_len = depth
            best_ratio = current_ratio
        for neighbor, edge_ratio in mesh[node]:
            if neighbor not in visited:
                dfs(neighbor, visited | {neighbor}, current_ratio * edge_ratio, depth + 1)

    dfs(start, {start}, 1.0, 0)
    return round(best_ratio, 4) if best_ratio is not None else None


def count_distinct_axles(axle_parts):
    """Count distinct axle lines (same axis + same transverse position = same axle)."""
    seen = set()
    for part in axle_parts:
        pos = part.get("pos", [0, 0, 0])
        axis = part.get("axis", "x")
        if axis == "x":
            key = ("x", pos[1], pos[2])
        elif axis == "y":
            key = ("y", pos[0], pos[2])
        else:
            key = ("z", pos[0], pos[1])
        seen.add(key)
    return len(seen)


def compute_bounding_box(parts, parts_library):
    """Return [width, height, depth] bounding box of all parts."""
    if not parts:
        return None

    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")

    for part in parts:
        pt = part.get("type", "")
        pos = part.get("pos", [0, 0, 0])
        axis = part.get("axis", "x")

        if pt not in parts_library:
            continue

        spec = parts_library[pt]
        length = spec.get("length", 1) or 1
        radius = spec.get("radius_studs", 0) or 0

        # Extent along axis
        if axis == "x":
            x0, x1 = pos[0], pos[0] + length
            y0, y1 = pos[1] - radius, pos[1] + radius
            z0, z1 = pos[2] - radius, pos[2] + radius
        elif axis == "y":
            x0, x1 = pos[0] - radius, pos[0] + radius
            y0, y1 = pos[1], pos[1] + length
            z0, z1 = pos[2] - radius, pos[2] + radius
        else:
            x0, x1 = pos[0] - radius, pos[0] + radius
            y0, y1 = pos[1] - radius, pos[1] + radius
            z0, z1 = pos[2], pos[2] + length

        min_x, max_x = min(min_x, x0), max(max_x, x1)
        min_y, max_y = min(min_y, y0), max(max_y, y1)
        min_z, max_z = min(min_z, z0), max(max_z, z1)

    return [
        round(max_x - min_x, 2),
        round(max_y - min_y, 2),
        round(max_z - min_z, 2),
    ]
