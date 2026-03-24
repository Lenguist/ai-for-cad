#!/usr/bin/env python3
"""
parts.py — Browse the Lego Technic parts library.

Usage:
    python parts.py categories
    python parts.py list gear
    python parts.py list                  # all parts
    python parts.py get gear-8t
    python parts.py search worm
    python parts.py mesh gear-8t          # what can this part connect to?
"""

import json
import sys
from pathlib import Path

PARTS_FILE = Path(__file__).parent.parent / "mar11-demo-attempt" / "parts_library.json"


def load():
    with open(PARTS_FILE) as f:
        return json.load(f)


def cmd_categories(lib):
    cats = sorted(set(v["category"] for v in lib.values()))
    print("Categories:")
    for c in cats:
        parts = [k for k, v in lib.items() if v["category"] == c]
        print(f"  {c:15s} ({len(parts)} parts): {', '.join(parts)}")


def cmd_list(lib, category=None):
    parts = {k: v for k, v in lib.items()
             if category is None or v["category"] == category}
    if not parts:
        print(f"No parts in category '{category}'")
        print(f"Available categories: {sorted(set(v['category'] for v in lib.values()))}")
        return

    print(f"{'ID':<20} {'Name':<30} {'Key specs'}")
    print("-" * 75)
    for part_id, spec in sorted(parts.items()):
        cat = spec["category"]
        if cat == "gear":
            detail = f"teeth={spec['teeth']}, radius={spec['radius_studs']} studs"
        elif cat in ("beam", "axle", "rack"):
            detail = f"length={spec['length']} studs"
        elif cat == "pin":
            detail = f"length={spec['length']}"
        else:
            detail = spec.get("description", "")[:40]
        print(f"  {part_id:<18} {spec['name']:<30} {detail}")


def cmd_get(lib, part_id):
    if part_id not in lib:
        print(f"Unknown part: '{part_id}'")
        print(f"Available: {', '.join(sorted(lib.keys()))}")
        return
    spec = lib[part_id]
    print(f"\n=== {part_id} ===")
    print(f"  Name:        {spec['name']}")
    print(f"  Category:    {spec['category']}")
    print(f"  Description: {spec['description']}")
    if spec.get("teeth") is not None:
        print(f"  Teeth:       {spec['teeth']}")
    if spec.get("radius_studs") is not None:
        print(f"  Radius:      {spec['radius_studs']} studs")
    if spec.get("length") is not None:
        print(f"  Length:      {spec['length']} studs")
    if spec.get("holes"):
        print(f"  Holes at:    {spec['holes']}")
    print(f"  BrickLink:   {spec.get('bl_id', 'N/A')}")


def cmd_search(lib, query):
    q = query.lower()
    results = {k: v for k, v in lib.items()
               if q in k.lower() or q in v["name"].lower() or q in v["description"].lower()}
    if not results:
        print(f"No results for '{query}'")
        return
    print(f"Results for '{query}':")
    cmd_list({k: lib[k] for k in results}, category=None)


def cmd_mesh(lib, part_id):
    """Show what parts can connect/mesh with this part."""
    if part_id not in lib:
        print(f"Unknown part: '{part_id}'")
        return
    spec = lib[part_id]
    cat = spec["category"]
    print(f"\nConnection info for {part_id} ({spec['name']}):")

    if cat == "gear":
        r = spec["radius_studs"]
        t = spec["teeth"]
        print(f"\n  This gear: {t} teeth, radius {r} studs")
        print(f"  Meshes with (center-to-center distance):")
        for other_id, other in sorted(lib.items()):
            if other["category"] == "gear" and other_id != part_id:
                dist = r + other["radius_studs"]
                print(f"    {other_id:<18} ({other['teeth']}T, r={other['radius_studs']}) "
                      f"→ place centers {dist} studs apart, SAME axis direction")
        if spec.get("teeth") == 1:
            print(f"\n  Worm gear note: axis must be PERPENDICULAR to driven spur gear axis")
        print(f"\n  Fits on: any axle (axle_through connection)")

    elif cat == "rack":
        print(f"  Drives / is driven by: any gear")
        print(f"  Gear must be placed radius studs from rack centerline, PERPENDICULAR")
        print(f"  Best pairing: gear-8t (radius=1) → place gear 1 stud from rack center")

    elif cat == "axle":
        print(f"  Passes through: gear axle holes, beam holes, bushes, connectors")
        print(f"  Fix gear position with: bush (place at same pos, same axis)")

    elif cat == "beam":
        L = spec["length"]
        print(f"  Has {L} holes at positions 0 through {L-1} along its axis")
        print(f"  Connects via: pin or pin-friction through matching holes on other beams")
        print(f"  Axles can pass through any hole perpendicular to beam axis")

    elif cat in ("pin",):
        print(f"  Connects two beam holes that are aligned on the same axis")

    elif cat == "connector":
        print(f"  Joins beams at 90 degrees (perpendicular connector)")


def main():
    lib = load()
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        return

    cmd = args[0]
    if cmd == "categories":
        cmd_categories(lib)
    elif cmd == "list":
        cmd_list(lib, args[1] if len(args) > 1 else None)
    elif cmd == "get" and len(args) > 1:
        cmd_get(lib, args[1])
    elif cmd == "search" and len(args) > 1:
        cmd_search(lib, " ".join(args[1:]))
    elif cmd == "mesh" and len(args) > 1:
        cmd_mesh(lib, args[1])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
