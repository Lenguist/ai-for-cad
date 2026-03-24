#!/usr/bin/env python3
"""
compile.py — Verify placement and connections of a Lego Technic assembly.

Usage:
    python compile.py assembly.json
    python compile.py assembly.json --task T2-01   # also check success criteria

Input JSON format:
{
  "parts": [
    {"id": "g1", "type": "gear-8t",  "pos": [0,0,0], "axis": "y"},
    {"id": "g2", "type": "gear-24t", "pos": [4,0,0], "axis": "y"}
  ],
  "connections": [
    {"type": "gear_mesh",    "parts": ["g1", "g2"]},
    {"type": "axle_through", "axle": "ax1", "part": "g1"},
    {"type": "pin_in_beam",  "beam": "b1",  "hole": 0, "part": "p1"}
  ]
}

Connection types:
  gear_mesh       — two gears mesh (spur-spur or worm-spur)
  axle_through    — axle passes through a gear/beam hole
  pin_in_beam     — pin connects two beams at a hole position
  bush_on_axle    — bush fixes position on axle
  rack_pinion     — gear drives rack (linear motion)
"""

import json
import math
import sys
import argparse
from pathlib import Path

PARTS_FILE = Path(__file__).parent.parent / "mar11-demo-attempt" / "parts_library.json"
TASKS_FILE = Path(__file__).parent.parent / "benchmark" / "tasks.json"

RESET  = "\033[0m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"


def ok(msg):   return f"{GREEN}✓{RESET} {msg}"
def err(msg):  return f"{RED}✗{RESET} {msg}"
def warn(msg): return f"{YELLOW}⚠{RESET} {msg}"
def info(msg): return f"{CYAN}→{RESET} {msg}"


def load_parts():
    with open(PARTS_FILE) as f:
        return json.load(f)


def load_assembly(path):
    with open(path) as f:
        return json.load(f)


def dist3(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def dist_perpendicular(point, line_origin, line_axis):
    """Distance from point to an infinite line (defined by origin + axis direction)."""
    px, py, pz = point
    ox, oy, oz = line_origin
    if line_axis == "x":
        return math.sqrt((py - oy) ** 2 + (pz - oz) ** 2)
    elif line_axis == "y":
        return math.sqrt((px - ox) ** 2 + (pz - oz) ** 2)
    else:
        return math.sqrt((px - ox) ** 2 + (py - oy) ** 2)


# ─── Part inventory ───────────────────────────────────────────────────────────

def check_inventory(assembly, lib):
    print(f"\n{BOLD}── PART INVENTORY ──────────────────────────────────────{RESET}")
    parts = assembly.get("parts", [])
    errors = []

    ids_seen = set()
    valid_parts = {}

    for p in parts:
        pid = p.get("id", "?")
        ptype = p.get("type", "")
        pos = p.get("pos")
        axis = p.get("axis", "?")

        # Duplicate ID
        if pid in ids_seen:
            print(err(f"Duplicate ID: '{pid}'"))
            errors.append(f"duplicate_id:{pid}")
            continue
        ids_seen.add(pid)

        # Unknown type
        if ptype not in lib:
            print(err(f"'{pid}': unknown type '{ptype}'  (available: {', '.join(sorted(lib.keys()))})"))
            errors.append(f"unknown_type:{pid}")
            continue

        # Position
        if not isinstance(pos, list) or len(pos) != 3:
            print(err(f"'{pid}': pos must be [x,y,z], got: {pos}"))
            errors.append(f"bad_pos:{pid}")
            continue

        # Axis
        if axis not in ("x", "y", "z"):
            print(err(f"'{pid}': axis must be x/y/z, got: '{axis}'"))
            errors.append(f"bad_axis:{pid}")
            continue

        spec = lib[ptype]
        cat = spec["category"]
        if cat == "gear":
            detail = f"teeth={spec['teeth']}, r={spec['radius_studs']}, axis={axis}"
        elif cat in ("beam", "axle"):
            detail = f"length={spec['length']}, axis={axis}"
        else:
            detail = f"axis={axis}"

        print(ok(f"{pid:<12} type={ptype:<18} pos={pos}  {detail}"))
        valid_parts[pid] = {"spec": spec, "pos": pos, "axis": axis, "type": ptype}

    if not errors:
        print(info(f"Total: {len(valid_parts)} parts, all valid"))
    return valid_parts, errors


# ─── Connection verification ──────────────────────────────────────────────────

def check_connections(assembly, valid_parts, lib):
    print(f"\n{BOLD}── CONNECTION VERIFICATION ─────────────────────────────{RESET}")
    connections = assembly.get("connections", [])
    conn_errors = []
    conn_ok = []

    if not connections:
        print(warn("No connections declared."))
        return conn_errors, conn_ok

    for conn in connections:
        ctype = conn.get("type", "?")

        if ctype == "gear_mesh":
            result = check_gear_mesh(conn, valid_parts, lib)
        elif ctype == "axle_through":
            result = check_axle_through(conn, valid_parts, lib)
        elif ctype == "rack_pinion":
            result = check_rack_pinion(conn, valid_parts, lib)
        elif ctype == "pin_in_beam":
            result = check_pin_in_beam(conn, valid_parts, lib)
        elif ctype == "bush_on_axle":
            result = check_bush_on_axle(conn, valid_parts, lib)
        else:
            result = (False, f"Unknown connection type: '{ctype}'")

        passed, msg = result
        if passed:
            print(ok(f"[{ctype}] {msg}"))
            conn_ok.append(conn)
        else:
            print(err(f"[{ctype}] {msg}"))
            conn_errors.append((ctype, msg))

    return conn_errors, conn_ok


def check_gear_mesh(conn, parts, lib):
    pids = conn.get("parts", [])
    if len(pids) != 2:
        return False, f"gear_mesh needs exactly 2 parts, got {pids}"

    a_id, b_id = pids
    if a_id not in parts:
        return False, f"Part '{a_id}' not found"
    if b_id not in parts:
        return False, f"Part '{b_id}' not found"

    a, b = parts[a_id], parts[b_id]
    a_cat = a["spec"]["category"]
    b_cat = b["spec"]["category"]

    if a_cat != "gear" or b_cat != "gear":
        return False, f"gear_mesh requires two gears, got {a_cat} and {b_cat}"

    a_teeth = a["spec"]["teeth"]
    b_teeth = b["spec"]["teeth"]
    a_r = a["spec"]["radius_studs"]
    b_r = b["spec"]["radius_studs"]
    is_worm_a = a_teeth == 1
    is_worm_b = b_teeth == 1

    actual_dist = dist3(a["pos"], b["pos"])

    if is_worm_a or is_worm_b:
        # Worm gear: axes must be perpendicular
        if a["axis"] == b["axis"]:
            return False, (
                f"Worm mesh {a_id}+{b_id}: axes must be PERPENDICULAR "
                f"(both are '{a['axis']}'). "
                f"Fix: give the spur gear a different axis than the worm."
            )
        expected = a_r + b_r
        if abs(actual_dist - expected) > 0.75:
            return False, (
                f"Worm mesh {a_id}+{b_id}: center distance is {actual_dist:.2f}, "
                f"need ~{expected:.1f} studs. "
                f"Fix: move {b_id} to be {expected} studs from {a_id}."
            )
        ratio = max(a_teeth, b_teeth)
        return True, (
            f"{a_id}({a_teeth}T) worm→ {b_id}({b_teeth}T)  "
            f"dist={actual_dist:.2f}/{expected:.1f}  ratio={ratio}:1  axes ⊥ ✓"
        )
    else:
        # Spur-spur: axes must match
        if a["axis"] != b["axis"]:
            return False, (
                f"Spur mesh {a_id}+{b_id}: axes must match "
                f"('{a['axis']}' vs '{b['axis']}'). "
                f"Fix: set both gears to the same axis."
            )
        expected = a_r + b_r
        if abs(actual_dist - expected) > 0.75:
            return False, (
                f"Spur mesh {a_id}+{b_id}: center distance is {actual_dist:.2f}, "
                f"need exactly {expected:.1f} studs ({a_r}+{b_r}). "
                f"Fix: move {b_id} so its pos differs from {a_id} by {expected} along one axis."
            )
        ratio = b_teeth / a_teeth
        driven = b_id if ratio >= 1 else a_id
        return True, (
            f"{a_id}({a_teeth}T) ↔ {b_id}({b_teeth}T)  "
            f"dist={actual_dist:.2f}/{expected:.1f}  ratio={ratio:.2f}:1  same axis ✓"
        )


def check_axle_through(conn, parts, lib):
    axle_id = conn.get("axle")
    part_id = conn.get("part")
    if axle_id not in parts:
        return False, f"Axle '{axle_id}' not found"
    if part_id not in parts:
        return False, f"Part '{part_id}' not found"

    axle = parts[axle_id]
    part = parts[part_id]

    if axle["spec"]["category"] != "axle":
        return False, f"'{axle_id}' is not an axle (it's {axle['spec']['category']})"

    # Axle passes through gear/beam: the gear/beam center should be on the axle line
    d = dist_perpendicular(part["pos"], axle["pos"], axle["axis"])
    if d > 0.6:
        return False, (
            f"Axle '{axle_id}' does not pass through '{part_id}': "
            f"perpendicular distance is {d:.2f} studs (need < 0.5). "
            f"Fix: align {part_id} center with axle line (same coords perpendicular to axle axis)."
        )

    # Check axes: axle and gear should have same axis
    if axle["axis"] != part["axis"]:
        # Beam holes are perpendicular to beam axis — axle passes through, so axle axis ≠ beam axis is OK
        if part["spec"]["category"] == "beam":
            pass  # fine, axle perpendicular to beam
        else:
            return False, (
                f"Axle '{axle_id}' axis '{axle['axis']}' but '{part_id}' axis '{part['axis']}' — "
                f"for a gear, axle and gear should share the same rotation axis."
            )

    return True, f"axle '{axle_id}' passes through '{part_id}' (d={d:.2f}) ✓"


def check_rack_pinion(conn, parts, lib):
    gear_id = conn.get("gear")
    rack_id = conn.get("rack")
    if gear_id not in parts:
        return False, f"Gear '{gear_id}' not found"
    if rack_id not in parts:
        return False, f"Rack '{rack_id}' not found"

    gear = parts[gear_id]
    rack = parts[rack_id]

    if gear["spec"]["category"] != "gear":
        return False, f"'{gear_id}' is not a gear"
    if rack["spec"]["category"] != "rack":
        return False, f"'{rack_id}' is not a rack"

    # Gear axis must be perpendicular to rack axis? No — gear rotates, rack translates.
    # Gear center must be radius studs from rack centerline
    gear_r = gear["spec"]["radius_studs"]
    d = dist_perpendicular(gear["pos"], rack["pos"], rack["axis"])
    if abs(d - gear_r) > 0.6:
        return False, (
            f"Rack-pinion '{gear_id}'+'{rack_id}': gear center is {d:.2f} studs from rack, "
            f"need {gear_r:.1f} (gear radius). "
            f"Fix: move {gear_id} to be exactly {gear_r} studs from rack centerline "
            f"perpendicular to rack's '{rack['axis']}' axis."
        )

    return True, (
        f"gear '{gear_id}' ({gear['spec']['teeth']}T, r={gear_r}) drives rack '{rack_id}'  "
        f"d={d:.2f}/{gear_r}  → rotation→linear ✓"
    )


def check_pin_in_beam(conn, parts, lib):
    beam_id = conn.get("beam")
    part_id = conn.get("part")
    hole = conn.get("hole")

    if beam_id not in parts:
        return False, f"Beam '{beam_id}' not found"
    if part_id not in parts:
        return False, f"Part '{part_id}' not found"

    beam = parts[beam_id]
    if beam["spec"]["category"] != "beam":
        return False, f"'{beam_id}' is not a beam"

    spec = beam["spec"]
    holes = spec.get("holes", [])
    if hole not in holes:
        return False, (
            f"Beam '{beam_id}' has no hole at index {hole}. "
            f"Available holes: {holes} (beam length={spec['length']})"
        )

    return True, f"pin/axle '{part_id}' in beam '{beam_id}' hole {hole} ✓"


def check_bush_on_axle(conn, parts, lib):
    axle_id = conn.get("axle")
    bush_id = conn.get("bush")
    if axle_id not in parts:
        return False, f"Axle '{axle_id}' not found"
    if bush_id not in parts:
        return False, f"Bush '{bush_id}' not found"

    axle = parts[axle_id]
    bush = parts[bush_id]

    if axle["spec"]["category"] != "axle":
        return False, f"'{axle_id}' is not an axle"
    if bush["spec"]["category"] != "connector":
        return False, f"'{bush_id}' is not a connector/bush"

    d = dist_perpendicular(bush["pos"], axle["pos"], axle["axis"])
    if d > 0.6:
        return False, (
            f"Bush '{bush_id}' is not on axle '{axle_id}': "
            f"perpendicular distance {d:.2f} studs. "
            f"Fix: move bush so it's centered on the axle line."
        )

    return True, f"bush '{bush_id}' on axle '{axle_id}' ✓"


# ─── Auto-detect ──────────────────────────────────────────────────────────────

def auto_detect(valid_parts, lib, declared_conns):
    """Find connections that exist geometrically but weren't declared."""
    print(f"\n{BOLD}── AUTO-DETECTED CONNECTIONS ───────────────────────────{RESET}")

    declared_pairs = set()
    for conn in declared_conns:
        pids = conn.get("parts", [])
        if len(pids) == 2:
            declared_pairs.add(frozenset(pids))
        a = conn.get("gear") or conn.get("axle") or conn.get("beam")
        b = conn.get("part") or conn.get("rack") or conn.get("bush")
        if a and b:
            declared_pairs.add(frozenset([a, b]))

    gear_parts = [(pid, p) for pid, p in valid_parts.items()
                  if p["spec"]["category"] == "gear"]
    rack_parts = [(pid, p) for pid, p in valid_parts.items()
                  if p["spec"]["category"] == "rack"]

    found_any = False

    # Gear-gear meshes
    for i in range(len(gear_parts)):
        for j in range(i + 1, len(gear_parts)):
            a_id, a = gear_parts[i]
            b_id, b = gear_parts[j]
            if frozenset([a_id, b_id]) in declared_pairs:
                continue

            a_r = a["spec"]["radius_studs"]
            b_r = b["spec"]["radius_studs"]
            expected = a_r + b_r
            actual = dist3(a["pos"], b["pos"])

            # Spur-spur: same axis, correct distance
            if a["axis"] == b["axis"] and abs(actual - expected) < 0.75:
                print(warn(
                    f"Undeclared gear mesh: {a_id}({a['spec']['teeth']}T) ↔ {b_id}({b['spec']['teeth']}T)  "
                    f"dist={actual:.2f}/{expected:.1f}  — add to connections?"
                ))
                found_any = True

            # Worm-spur: perpendicular axes, correct distance
            elif a["axis"] != b["axis"] and abs(actual - expected) < 0.75:
                if a["spec"]["teeth"] == 1 or b["spec"]["teeth"] == 1:
                    print(warn(
                        f"Undeclared worm mesh: {a_id} ↔ {b_id}  "
                        f"dist={actual:.2f}/{expected:.1f}"
                    ))
                    found_any = True

    # Gear-rack proximity
    for g_id, g in gear_parts:
        for r_id, r in rack_parts:
            if frozenset([g_id, r_id]) in declared_pairs:
                continue
            g_r = g["spec"]["radius_studs"]
            d = dist_perpendicular(g["pos"], r["pos"], r["axis"])
            if abs(d - g_r) < 0.6:
                print(warn(f"Undeclared rack-pinion: {g_id} ↔ {r_id}  d={d:.2f}/{g_r}"))
                found_any = True

    if not found_any:
        print(info("None found (all geometric connections are declared)"))


# ─── ASCII Visualizer ─────────────────────────────────────────────────────────

def visualize(valid_parts):
    print(f"\n{BOLD}── VISUALIZATION (top view, X→Z↓) ─────────────────────{RESET}")

    if not valid_parts:
        print("  (no valid parts)")
        return

    all_pos = [p["pos"] for p in valid_parts.values()]
    xs = [p[0] for p in all_pos]
    zs = [p[2] for p in all_pos]

    min_x, max_x = min(xs), max(xs)
    min_z, max_z = min(zs), max(zs)

    # Pad
    min_x -= 1; max_x += 2
    min_z -= 1; max_z += 2

    # Keep grid reasonable
    if (max_x - min_x) > 40 or (max_z - min_z) > 20:
        print(info("Assembly too large for ASCII grid — showing part list instead"))
        for pid, p in sorted(valid_parts.items()):
            cat = p["spec"]["category"]
            sym = symbol(cat, p["spec"])
            print(f"  {sym} {pid:<12} pos={p['pos']}  axis={p['axis']}")
        return

    # Build grid
    W = int(max_x - min_x) + 1
    H = int(max_z - min_z) + 1
    grid = [["  " for _ in range(W)] for _ in range(H)]

    part_at = {}  # (col, row) -> pid

    # Priority: gear > rack > beam > axle > pin/connector (so gears show on top)
    priority = {"gear": 5, "rack": 4, "beam": 3, "axle": 2, "pin": 1, "connector": 1}
    placed = {}  # (col,row) -> (pid, prio)

    for pid, p in valid_parts.items():
        col = int(p["pos"][0] - min_x)
        row = int(p["pos"][2] - min_z)
        cat = p["spec"]["category"]
        prio = priority.get(cat, 0)
        existing = placed.get((col, row))
        if existing is None or prio > existing[1]:
            placed[(col, row)] = (pid, prio)

    for (col, row), (pid, _) in placed.items():
        p = valid_parts[pid]
        cat = p["spec"]["category"]
        sym = symbol(cat, p["spec"])
        label = (sym + pid)[:2].ljust(2)
        grid[row][col] = label
        part_at[(col, row)] = pid

    # X axis header
    header_vals = list(range(int(min_x), int(max_x) + 1))
    header = "   " + "".join(f"{v:<2}" for v in header_vals)
    print(f"\n{DIM}{header}{RESET}")

    for row in range(H):
        z_label = f"{int(min_z + row):<2} "
        line = z_label
        for col in range(W):
            cell = grid[row][col]
            pid = part_at.get((col, row))
            if pid:
                cat = valid_parts[pid]["spec"]["category"]
                line += colorize(cell, cat)
            else:
                line += f"{DIM}.{RESET} "
        print(line)

    # Legend
    print(f"\n{DIM}Legend:{RESET}")
    for pid, p in sorted(valid_parts.items()):
        cat = p["spec"]["category"]
        sym = symbol(cat, p["spec"])
        y_note = f"  y={p['pos'][1]}" if p["pos"][1] != 0 else ""
        print(f"  {colorize(sym, cat)} {pid:<12} {p['type']:<18} pos={p['pos']}  axis={p['axis']}{y_note}")


def symbol(cat, spec):
    if cat == "gear":
        t = spec.get("teeth", 0)
        if t == 1: return "W"   # worm
        if t == 8: return "g"
        if t == 16: return "G"
        if t == 24: return "O"
        if t == 40: return "@"
        return "?"
    elif cat == "axle":   return "+"
    elif cat == "beam":   return "="
    elif cat == "rack":   return "R"
    elif cat == "pin":    return "."
    elif cat == "connector": return "C"
    return "?"


def colorize(s, cat):
    colors = {
        "gear": "\033[93m",      # yellow
        "axle": "\033[90m",      # dark grey
        "beam": "\033[96m",      # cyan
        "rack": "\033[95m",      # magenta
        "pin":  "\033[37m",      # light grey
        "connector": "\033[94m", # blue
    }
    c = colors.get(cat, "")
    return f"{c}{s}{RESET}"


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Compile and verify a Lego Technic assembly")
    parser.add_argument("assembly", help="Path to assembly JSON file")
    args = parser.parse_args()

    lib = load_parts()
    try:
        assembly = load_assembly(args.assembly)
    except FileNotFoundError:
        print(err(f"File not found: {args.assembly}"))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(err(f"Invalid JSON: {e}"))
        sys.exit(1)

    if assembly.get("reasoning"):
        print(f"\n{BOLD}── REASONING ───────────────────────────────────────────{RESET}")
        print(f"  {assembly['reasoning']}")

    # 1. Inventory
    valid_parts, inv_errors = check_inventory(assembly, lib)

    if inv_errors:
        print(f"\n{RED}{BOLD}Stopped: fix inventory errors before checking connections.{RESET}")
        sys.exit(1)

    # 2. Connections
    conn_errors, conn_ok = check_connections(assembly, valid_parts, lib)

    # 3. Auto-detect
    auto_detect(valid_parts, lib, assembly.get("connections", []))

    # 4. Visualize
    visualize(valid_parts)

    # 5. Summary
    print(f"\n{BOLD}── SUMMARY ─────────────────────────────────────────────{RESET}")
    total_conns = len(assembly.get("connections", []))
    ok_count = len(conn_ok)
    fail_count = len(conn_errors)

    if fail_count == 0 and total_conns > 0:
        print(ok(f"All {ok_count}/{total_conns} connections valid"))
    elif fail_count == 0 and total_conns == 0:
        print(warn("No connections declared — parts placed but not connected"))
    else:
        print(err(f"{fail_count}/{total_conns} connections FAILED"))
        for ctype, msg in conn_errors:
            print(f"   {RED}→{RESET} [{ctype}] {msg}")

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
