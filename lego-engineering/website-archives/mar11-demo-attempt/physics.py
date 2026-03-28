"""
physics.py — Geometry-driven kinematic compiler and simulator.

Pipeline:
    assembly JSON + parts_library
        ↓  compile
    physics world  (rigid bodies at positions, no semantic labels)
        ↓  detect contacts
    constraint graph  (axle couplings, rolling contacts, rack contacts)
        ↓  propagate from motor input
    kinematic state  (angular/linear velocities for every body)
        ↓  format
    output dict  (compatible with checker.py)

The compiler uses ONLY geometry from the parts_library:
    radius_studs, length, rpm_no_load, stall_torque_ncm

It does NOT read: category, name, description, teeth, holes.
All constraints emerge from spatial relationships between shapes.

If two gears are placed at the wrong distance → no contact detected →
no constraint created → no motion transmitted.  The checker sees failure.
"""

import math
from collections import defaultdict

# ── Tolerance constants (studs) ──────────────────────────────────────────────

AXLE_ALIGN_TOL   = 0.15   # how close axle center lines must be to couple
ROLLING_TOL      = 0.30   # surface-to-surface gap allowed for rolling contact
RACK_TOL         = 0.30   # gap allowed for gear-rack contact
WORM_TOL         = 0.40   # slightly looser for worm (perpendicular axes)

# LEGO standard: teeth = radius_studs × 8  (verified: 8T→r=1, 16T→r=2, 24T→r=3, 40T→r=5)
TEETH_PER_RADIUS = 8


# ── Public API ───────────────────────────────────────────────────────────────

def compile_and_simulate(assembly, parts_library):
    """
    Main entry point. Replaces validator.compute_kinematics().
    Returns a dict compatible with checker.py's kinematics expectations.
    """
    parts = assembly.get("parts", [])

    # 1. Build geometry-only body representations
    bodies = {}
    for part in parts:
        pt = part.get("type", "")
        if pt not in parts_library:
            continue
        body = _make_body(part, parts_library[pt])
        bodies[body["id"]] = body

    # 2. Detect constraints purely from geometry
    axle_groups     = _detect_axle_couplings(bodies)
    rolling         = _detect_rolling_contacts(bodies)
    worm_contacts   = _detect_worm_contacts(bodies)
    rack_contacts   = _detect_rack_contacts(bodies)
    motors          = _find_motors(bodies)

    # 3. Propagate kinematics from motor inputs
    angular, linear = _propagate(
        axle_groups, rolling, worm_contacts, rack_contacts, motors
    )

    # 4. Format output for checker.py
    return _format_output(
        bodies, rolling, worm_contacts, rack_contacts,
        motors, angular, linear
    )


# ── Body construction ────────────────────────────────────────────────────────

def _make_body(part, spec):
    """
    Extract only geometric properties from spec.
    No 'category', 'name', 'description', or 'teeth' used here.
    """
    radius = spec.get("radius_studs")   # None for beams, racks, connectors
    length = spec.get("length") or 1

    # Shape classification from geometry alone:
    #   thin cylinder  → radius ≤ 0.25  (axle, pin)
    #   disk           → radius > 0.25  (gear, worm gear)
    #   linear body    → no radius      (beam, rack, connector)
    has_radius  = radius is not None and radius > 0
    is_thin     = has_radius and radius <= 0.25   # axle-like
    is_disk     = has_radius and radius > 0.25    # gear-like

    return {
        "id":           part["id"],
        "pos":          list(part.get("pos", [0, 0, 0])),
        "axis":         part.get("axis", "x"),
        "radius":       radius,
        "length":       length,
        "has_radius":   has_radius,
        "is_thin":      is_thin,
        "is_disk":      is_disk,
        # Motor properties (None if not a motor)
        "motor_rpm":    spec.get("rpm_no_load"),
        "motor_torque": spec.get("stall_torque_ncm"),
        "motor_power":  spec.get("rated_power_w"),
        "is_motor":     spec.get("rpm_no_load") is not None,
        # Kept for output formatting only — not used in physics logic
        "_type":        part.get("type"),
    }


# ── Geometry helpers ─────────────────────────────────────────────────────────

def _dist3(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def _axis_index(axis):
    return {"x": 0, "y": 1, "z": 2}[axis]


def _perp_dist(center, origin, along_axis):
    """
    Distance from 'center' to the infinite line through 'origin'
    in the direction of 'along_axis', measured perpendicularly.
    """
    ax = _axis_index(along_axis)
    deltas = [center[i] - origin[i] for i in range(3)]
    deltas[ax] = 0.0   # zero out the axial component
    return math.sqrt(sum(d * d for d in deltas))


def _point_on_line(point, line_origin, line_axis, body_length):
    """
    Check whether 'point' lies within the finite extent of a line segment.
    Line starts at line_origin and extends 'body_length' along line_axis.
    """
    ax = _axis_index(line_axis)
    start = line_origin[ax]
    end   = start + body_length
    p     = point[ax]
    return (start - 0.5) <= p <= (end + 0.5)


# ── Constraint detection ─────────────────────────────────────────────────────

def _detect_axle_couplings(bodies):
    """
    Group bodies that share the same rotation axis line.

    Two bodies are on the same axle if:
      • same axis direction
      • their center lines are within AXLE_ALIGN_TOL of each other
      • at least one body is thin (axle/pin) and its length covers the other,
        OR both are disks at the same transverse position (stacked on one axle)

    Returns: list of frozensets of body IDs (only groups with ≥ 2 members).
    """
    body_list = list(bodies.values())

    # Union-Find
    parent = {b["id"]: b["id"] for b in body_list}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        parent[find(x)] = find(y)

    for i, b1 in enumerate(body_list):
        for b2 in body_list[i + 1:]:
            if b1["axis"] != b2["axis"]:
                continue

            # Perpendicular distance between their center lines
            d = _perp_dist(b2["pos"], b1["pos"], b1["axis"])
            if d > AXLE_ALIGN_TOL:
                continue

            # If b1 is an axle/pin, check its length covers b2's position
            if b1["is_thin"] and not _point_on_line(
                b2["pos"], b1["pos"], b1["axis"], b1["length"]
            ):
                continue

            # If b2 is an axle/pin, check its length covers b1's position
            if b2["is_thin"] and not _point_on_line(
                b1["pos"], b2["pos"], b2["axis"], b2["length"]
            ):
                continue

            union(b1["id"], b2["id"])

    groups = defaultdict(set)
    for b in body_list:
        groups[find(b["id"])].add(b["id"])

    return [g for g in groups.values() if len(g) > 1]


def _detect_rolling_contacts(bodies):
    """
    Detect rolling contact between disk bodies with PARALLEL axes.
    (Spur gears, idler gears.)

    Contact condition: dist(centers) ≈ r1 + r2  (surfaces tangent)
    Constraint:        ω₂ = −(r₁/r₂) × ω₁       (opposite rotation)

    The ratio r₁/r₂ is derived from geometry alone.
    teeth count is inferred from radius using the LEGO standard (×8).
    """
    disks = [b for b in bodies.values() if b["is_disk"]]
    contacts = []

    for i, b1 in enumerate(disks):
        for b2 in disks[i + 1:]:
            if b1["axis"] != b2["axis"]:
                continue   # parallel axes only — worm handled separately

            d        = _dist3(b1["pos"], b2["pos"])
            expected = b1["radius"] + b2["radius"]

            if abs(d - expected) <= ROLLING_TOL:
                contacts.append({
                    "body1":   b1["id"],
                    "body2":   b2["id"],
                    "radius1": b1["radius"],
                    "radius2": b2["radius"],
                    # Ratio from geometry (not from spec teeth count)
                    "ratio":   round(b2["radius"] / b1["radius"], 4),
                })

    return contacts


def _detect_worm_contacts(bodies):
    """
    Detect worm-gear contacts: a small disk (worm, radius ≤ 1.1)
    meshing with a larger disk along a PERPENDICULAR axis.

    Geometry: the worm's pitch cylinder is tangent to the driven gear's
    pitch cylinder at a point where the two axes are closest.

    Contact condition:
      • axes are perpendicular
      • minimum distance between the two axis lines ≈ r_worm + r_gear

    Constraint: ω_gear = ω_worm × (r_worm / r_gear)
    (one tooth of worm advances one tooth of gear per revolution,
     which falls out of the radii for LEGO standard tooth pitch)
    """
    disks = [b for b in bodies.values() if b["is_disk"]]
    contacts = []

    for i, b1 in enumerate(disks):
        for b2 in disks[i + 1:]:
            ax1, ax2 = b1["axis"], b2["axis"]
            if ax1 == ax2:
                continue  # not perpendicular

            # Identify worm (smaller) and gear (larger)
            if b1["radius"] <= b2["radius"]:
                worm, gear = b1, b2
            else:
                worm, gear = b2, b1

            # Only treat as worm if worm radius is very small (≤ 1.1 studs)
            if worm["radius"] > 1.1:
                continue

            # Distance between perpendicular axis lines
            # For two perpendicular lines, use the formula for skew lines
            d = _skew_line_dist(
                worm["pos"], worm["axis"],
                gear["pos"], gear["axis"]
            )
            expected = worm["radius"] + gear["radius"]

            if abs(d - expected) <= WORM_TOL:
                contacts.append({
                    "worm":        worm["id"],
                    "gear":        gear["id"],
                    "radius_worm": worm["radius"],
                    "radius_gear": gear["radius"],
                    # ω_gear = ω_worm × (r_worm / r_gear)
                    "ratio":       round(worm["radius"] / gear["radius"], 4),
                })

    return contacts


def _skew_line_dist(p1, ax1, p2, ax2):
    """
    Minimum distance between two skew lines in 3D.
    Each line defined by a point and an axis string ('x','y','z').
    """
    d1 = [1 if ax1 == a else 0 for a in "xyz"]
    d2 = [1 if ax2 == a else 0 for a in "xyz"]

    # Cross product d1 × d2
    n = [
        d1[1]*d2[2] - d1[2]*d2[1],
        d1[2]*d2[0] - d1[0]*d2[2],
        d1[0]*d2[1] - d1[1]*d2[0],
    ]
    n_mag = math.sqrt(sum(x*x for x in n))

    if n_mag < 1e-9:
        # Parallel lines — use regular perp distance
        return _perp_dist(p2, p1, ax1)

    # Distance = |( p2 - p1 ) · n| / |n|
    diff = [p2[i] - p1[i] for i in range(3)]
    return abs(sum(diff[i] * n[i] for i in range(3))) / n_mag


def _detect_rack_contacts(bodies):
    """
    Detect contacts between disk bodies and linear (non-circular) bodies.
    (Gear driving a rack.)

    Contact condition:
      • disk axis ≠ linear body axis  (rack travels perpendicular to pinion axis)
      • perpendicular distance from disk center to linear body center ≈ disk radius

    Constraint: v_rack = r_pinion × ω_pinion
    """
    disks   = [b for b in bodies.values() if b["is_disk"]]
    linears = [b for b in bodies.values() if not b["has_radius"] and b["length"] > 1]
    contacts = []

    for disk in disks:
        for linear in linears:
            if disk["axis"] == linear["axis"]:
                continue  # rack moves along a different axis than pinion rotates

            d = _perp_dist(disk["pos"], linear["pos"], linear["axis"])

            if abs(d - disk["radius"]) <= RACK_TOL:
                contacts.append({
                    "gear":   disk["id"],
                    "rack":   linear["id"],
                    "radius": disk["radius"],
                })

    return contacts


# ── Motor detection ──────────────────────────────────────────────────────────

def _find_motors(bodies):
    """
    Bodies with rpm_no_load set are motors — they provide the velocity input.
    """
    return [
        {
            "body_id": b["id"],
            "rpm":     b["motor_rpm"],
            "torque":  b["motor_torque"],
            "power":   b["motor_power"],
            "_type":   b["_type"],
        }
        for b in bodies.values()
        if b["is_motor"]
    ]


# ── Kinematic propagation ────────────────────────────────────────────────────

def _propagate(axle_groups, rolling, worm_contacts, rack_contacts, motors):
    """
    Given motor inputs, propagate angular and linear velocities through
    all constraints using iterative BFS.

    angular[body_id] = ω in RPM (sign encodes direction)
    linear[body_id]  = linear speed (RPM × radius, proportional)
    """
    angular = {}   # body_id → ω (RPM, signed)
    linear  = {}   # body_id → v (linear, proportional)

    # Build axle-group lookup for fast propagation
    body_to_group = {}
    for grp in axle_groups:
        for bid in grp:
            body_to_group[bid] = grp

    # Seed from motors
    for m in motors:
        angular[m["body_id"]] = m["rpm"]

    changed = True
    while changed:
        changed = False

        # 1. Axle coupling: all bodies in a group share ω
        for grp in axle_groups:
            knowns = [angular[bid] for bid in grp if bid in angular]
            if knowns:
                omega = knowns[0]
                for bid in grp:
                    if bid not in angular:
                        angular[bid] = omega
                        changed = True

        # 2. Spur gear rolling contact: ω₂ = −(r₁/r₂) × ω₁
        for c in rolling:
            b1, b2 = c["body1"], c["body2"]
            r1, r2 = c["radius1"], c["radius2"]
            if b1 in angular and b2 not in angular:
                angular[b2] = -angular[b1] * (r1 / r2)
                changed = True
            elif b2 in angular and b1 not in angular:
                angular[b1] = -angular[b2] * (r2 / r1)
                changed = True

        # 3. Worm contact: ω_gear = ω_worm × (r_worm / r_gear)
        for c in worm_contacts:
            w, g = c["worm"], c["gear"]
            rw, rg = c["radius_worm"], c["radius_gear"]
            if w in angular and g not in angular:
                angular[g] = angular[w] * (rw / rg)
                changed = True
            elif g in angular and w not in angular:
                angular[w] = angular[g] * (rg / rw)
                changed = True

        # 4. Rack contact: v_rack = r_pinion × |ω_pinion|
        for c in rack_contacts:
            gear_id, rack_id = c["gear"], c["rack"]
            r = c["radius"]
            if gear_id in angular and rack_id not in linear:
                linear[rack_id] = angular[gear_id] * r
                changed = True

    return angular, linear


# ── Output formatting ────────────────────────────────────────────────────────

def _format_output(bodies, rolling, worm_contacts, rack_contacts,
                   motors, angular, linear):
    """
    Produce a dict matching what checker.py expects from compute_kinematics():
        gear_pairs, rack_pinion, motors, motor_output,
        angular_velocities, linear_velocities
    """
    result = {}

    # gear_pairs — from rolling contacts (spur gears)
    gear_pairs = []
    for c in rolling:
        b1, b2 = c["body1"], c["body2"]
        r1, r2 = c["radius1"], c["radius2"]
        # Infer teeth from geometry using LEGO standard (teeth = radius × 8)
        t1 = round(r1 * TEETH_PER_RADIUS)
        t2 = round(r2 * TEETH_PER_RADIUS)
        gear_pairs.append({
            "gear1":     b1,
            "gear2":     b2,
            "teeth1":    t1,
            "teeth2":    t2,
            "ratio":     round(r2 / r1, 3),
            "ratio_str": f"{t2}:{t1}",
        })

    # Add worm contacts into gear_pairs with their effective ratio
    for c in worm_contacts:
        w, g = c["worm"], c["gear"]
        rw, rg = c["radius_worm"], c["radius_gear"]
        tw = round(rw * TEETH_PER_RADIUS)
        tg = round(rg * TEETH_PER_RADIUS)
        gear_pairs.append({
            "gear1":     w,
            "gear2":     g,
            "teeth1":    tw,
            "teeth2":    tg,
            "ratio":     round(rg / rw, 3),
            "ratio_str": f"{tg}:{tw}",
        })

    if gear_pairs:
        result["gear_pairs"] = gear_pairs

    # rack_pinion
    rack_pinion = []
    for c in rack_contacts:
        gear_id, rack_id = c["gear"], c["rack"]
        rack_pinion.append({
            "gear": gear_id,
            "rack": rack_id,
            "note": (
                f"Gear '{gear_id}' (r={c['radius']}) drives rack '{rack_id}'"
                f" → rotational→linear"
            ),
        })
    if rack_pinion:
        result["rack_pinion"]  = rack_pinion
        result["motion_type"]  = "Rotational → Linear (rack and pinion)"

    # motors
    motor_list = []
    for m in motors:
        motor_list.append({
            "id":               m["body_id"],
            "type":             m["_type"],
            "rpm_no_load":      m["rpm"],
            "stall_torque_ncm": m["torque"],
            "rated_power_w":    m["power"] or 0,
            "pos":              bodies[m["body_id"]]["pos"],
            "axis":             bodies[m["body_id"]]["axis"],
        })
    if motor_list:
        result["motors"] = motor_list

    # motor_output — compute from geometry-derived gear ratio chain
    if motor_list:
        total_ratio = _compute_chain_ratio(gear_pairs) if gear_pairs else 1.0
        motor       = motor_list[0]
        output_rpm  = motor["rpm_no_load"] / total_ratio
        output_torq = motor["stall_torque_ncm"] * total_ratio * 0.85
        result["motor_output"] = {
            "motor_id":          motor["id"],
            "gear_ratio":        round(total_ratio, 3),
            "output_rpm":        round(output_rpm, 1),
            "output_torque_ncm": round(output_torq, 1),
            "note": (
                f"{motor['rpm_no_load']} RPM ÷ {total_ratio:.2f}"
                f" = {output_rpm:.1f} RPM out,"
                f" torque × {total_ratio:.2f} × 0.85"
                f" = {output_torq:.1f} Ncm"
            ),
        }

    # Raw velocities (useful for animation and debugging)
    if angular:
        result["angular_velocities"] = {k: round(v, 3) for k, v in angular.items()}
    if linear:
        result["linear_velocities"]  = {k: round(v, 3) for k, v in linear.items()}

    if gear_pairs and len(gear_pairs) == 1:
        r = gear_pairs[0]["ratio"]
        result["summary"] = (
            f"Single gear pair: {gear_pairs[0]['ratio_str']} "
            f"({'speed up' if r < 1 else 'speed down'}, ratio {r:.2f}x)"
        )
    elif gear_pairs:
        result["summary"] = f"{len(gear_pairs)} gear pair(s) detected."

    return result


def _compute_chain_ratio(gear_pairs):
    """
    Compute total gear ratio through the longest chain.
    Same algorithm as checker.py but self-contained here.
    """
    if not gear_pairs:
        return 1.0
    if len(gear_pairs) == 1:
        return gear_pairs[0]["ratio"]

    from collections import defaultdict as _dd

    mesh = _dd(list)
    for p in gear_pairs:
        g1, g2, r = p["gear1"], p["gear2"], p["ratio"]
        mesh[g1].append((g2,      r))
        mesh[g2].append((g1, 1.0/r))

    degree = _dd(int)
    for p in gear_pairs:
        degree[p["gear1"]] += 1
        degree[p["gear2"]] += 1

    endpoints = [g for g, d in degree.items() if d == 1]
    if len(endpoints) < 2:
        total = 1.0
        for p in gear_pairs:
            if p["ratio"] > 1:
                total *= p["ratio"]
        return round(total, 4) if total != 1.0 else gear_pairs[0]["ratio"]

    best_ratio, best_len = None, 0

    def dfs(node, visited, cur, depth):
        nonlocal best_ratio, best_len
        if depth > best_len:
            best_len  = depth
            best_ratio = cur
        for nbr, edge_r in mesh[node]:
            if nbr not in visited:
                dfs(nbr, visited | {nbr}, cur * edge_r, depth + 1)

    dfs(endpoints[0], {endpoints[0]}, 1.0, 0)
    return round(best_ratio, 4) if best_ratio is not None else gear_pairs[0]["ratio"]
