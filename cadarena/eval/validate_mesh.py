"""
Mesh validation pass: runs trimesh checks on every .stl in method outputs.
Writes results back into the existing <pid>.json files.

Usage:
    python validate_mesh.py --method claude-opus-4-6
    python validate_mesh.py --all
    python validate_mesh.py --method gpt-5.4 --prompts t1_01 t2_03
"""

import argparse
import json
import sys
from pathlib import Path

STATIC_DIR  = Path(__file__).parent.parent / "text2cad" / "static"
METHODS_DIR = STATIC_DIR / "methods"


def check_mesh(stl_path: Path) -> dict:
    """Load STL with trimesh and run quality checks. Returns a mesh_quality dict."""
    try:
        import trimesh
    except ImportError:
        return {"error": "trimesh not installed — run: pip install trimesh"}

    result = {
        "watertight": False,
        "positive_volume": False,
        "no_self_intersections": None,  # trimesh can't always check this cheaply
        "vertex_count": 0,
        "face_count": 0,
        "volume_mm3": None,
        "error": None,
    }

    try:
        mesh = trimesh.load(str(stl_path), force="mesh")
        if not isinstance(mesh, trimesh.Trimesh):
            result["error"] = f"Loaded as {type(mesh).__name__}, not Trimesh"
            return result

        result["vertex_count"] = len(mesh.vertices)
        result["face_count"]   = len(mesh.faces)
        result["watertight"]   = bool(mesh.is_watertight)

        if mesh.is_watertight:
            vol = float(mesh.volume)
            result["volume_mm3"]      = round(vol, 3)
            result["positive_volume"] = vol > 0

        # Self-intersection check (slower, optional)
        try:
            result["no_self_intersections"] = not mesh.is_self_intersecting
        except Exception:
            result["no_self_intersections"] = None

    except Exception as e:
        result["error"] = str(e)

    return result


def validate_method(method_id: str, prompt_filter: list = None):
    out_dir = METHODS_DIR / method_id / "outputs"
    if not out_dir.exists():
        print(f"  No outputs dir for {method_id}")
        return

    json_files = sorted(out_dir.glob("*.json"))
    json_files = [f for f in json_files if f.name not in ("summary.json",)]

    if prompt_filter:
        json_files = [f for f in json_files if f.stem in prompt_filter]

    if not json_files:
        print(f"  [{method_id}] no result files found")
        return

    print(f"\n[{method_id}]")
    ok = skip = fail = 0

    for jf in json_files:
        with open(jf) as f:
            record = json.load(f)

        # Find corresponding STL
        stl_path = out_dir / f"{jf.stem}.stl"
        if not stl_path.exists():
            # Maybe stl_path stored in record
            sp = record.get("stl_path")
            if sp:
                stl_path = Path(sp)

        if not stl_path.exists():
            skip += 1
            print(f"  [-] {jf.stem}  no STL")
            continue

        mq = check_mesh(stl_path)
        record["mesh_quality"] = mq

        with open(jf, "w") as f:
            json.dump(record, f, indent=2)

        wt = "W" if mq.get("watertight") else "w"
        pv = "V" if mq.get("positive_volume") else "v"
        si = ("S" if mq.get("no_self_intersections") else "s") if mq.get("no_self_intersections") is not None else "?"
        err = f"  err={mq['error']}" if mq.get("error") else ""
        vol = f"  vol={mq['volume_mm3']:.1f}mm³" if mq.get("volume_mm3") else ""
        print(f"  [{wt}{pv}{si}] {jf.stem}{vol}{err}")

        if mq.get("watertight") and mq.get("positive_volume"):
            ok += 1
        elif mq.get("error"):
            fail += 1
        else:
            fail += 1

    total = ok + skip + fail
    print(f"  → {ok}/{total} watertight+positive-volume  ({skip} no STL)")


def main():
    p = argparse.ArgumentParser(description="Mesh validation for CAD Arena outputs")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--method", help="Single method ID")
    grp.add_argument("--all",    action="store_true", help="Run on all methods with outputs")
    p.add_argument("--prompts",  nargs="+", default=None, help="Filter to specific prompt IDs")
    args = p.parse_args()

    if args.all:
        methods = sorted(
            d.name for d in METHODS_DIR.iterdir()
            if d.is_dir() and (d / "outputs").exists()
        )
        print(f"Validating {len(methods)} methods...")
        for m in methods:
            validate_method(m, args.prompts)
    else:
        validate_method(args.method, args.prompts)

    print("\nDone. mesh_quality written into each <pid>.json")


if __name__ == "__main__":
    main()
