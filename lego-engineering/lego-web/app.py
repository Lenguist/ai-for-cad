from flask import Flask, render_template, jsonify, request
import json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "mar11-demo-attempt"))
sys.path.insert(0, str(Path(__file__).parent.parent / "lego-assembly-compiler"))

from validator import validate_assembly, compute_kinematics

PARTS_FILE = Path(__file__).parent.parent / "mar11-demo-attempt" / "parts_library.json"
TASKS_FILE = Path(__file__).parent.parent / "benchmark" / "tasks.json"

with open(PARTS_FILE) as f:
    PARTS = json.load(f)
with open(TASKS_FILE) as f:
    TASKS = json.load(f)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/parts")
def get_parts():
    q = request.args.get("q", "").lower()
    cat = request.args.get("category", "")
    result = {}
    for k, v in PARTS.items():
        if cat and v["category"] != cat:
            continue
        if q and q not in k.lower() and q not in v["name"].lower() and q not in v["description"].lower():
            continue
        result[k] = v
    return jsonify(result)


@app.route("/api/parts/categories")
def get_categories():
    cats = sorted(set(v["category"] for v in PARTS.values()))
    return jsonify(cats)


@app.route("/api/tasks")
def get_tasks():
    return jsonify(TASKS)


@app.route("/api/compile", methods=["POST"])
def compile_assembly():
    try:
        assembly = request.get_json()
    except Exception as e:
        return jsonify({"ok": False, "errors": [str(e)]}), 400

    errors, warnings = validate_assembly(assembly, PARTS)
    kinematics = compute_kinematics(assembly, PARTS) if not errors else {}

    # Connection checks
    conn_results = check_connections(assembly, PARTS)

    # Bounding box
    bbox = compute_bbox(assembly, PARTS)

    return jsonify({
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "kinematics": kinematics,
        "connections": conn_results,
        "bbox": bbox,
        "part_count": len(assembly.get("parts", [])),
    })


def check_connections(assembly, lib):
    results = []
    parts_map = {p["id"]: p for p in assembly.get("parts", [])}

    def get_spec(pid):
        p = parts_map.get(pid)
        if p and p.get("type") in lib:
            return lib[p["type"]], p
        return None, None

    for conn in assembly.get("connections", []):
        ctype = conn.get("type", "?")
        r = {"type": ctype, "ok": False, "msg": ""}

        if ctype == "gear_mesh":
            pids = conn.get("parts", [])
            if len(pids) != 2:
                r["msg"] = "Need exactly 2 parts"
            else:
                sa, pa = get_spec(pids[0])
                sb, pb = get_spec(pids[1])
                if not sa or not sb:
                    r["msg"] = f"Part not found"
                elif sa["category"] != "gear" or sb["category"] != "gear":
                    r["msg"] = "Both must be gears"
                else:
                    expected = sa["radius_studs"] + sb["radius_studs"]
                    actual = dist3(pa["pos"], pb["pos"])
                    is_worm = sa["teeth"] == 1 or sb["teeth"] == 1
                    if is_worm and pa.get("axis") == pb.get("axis"):
                        r["msg"] = f"Worm mesh: axes must be perpendicular (both '{pa['axis']}')"
                    elif not is_worm and pa.get("axis") != pb.get("axis"):
                        r["msg"] = f"Spur mesh: axes must match ('{pa['axis']}' vs '{pb['axis']}')"
                    elif abs(actual - expected) > 0.75:
                        r["msg"] = f"Distance {actual:.2f} studs, need {expected:.1f} (r1+r2). Move {pids[1]} {expected-actual:+.1f} studs."
                    else:
                        ratio = sb["teeth"] / sa["teeth"]
                        r["ok"] = True
                        r["msg"] = f"{pids[0]}({sa['teeth']}T) ↔ {pids[1]}({sb['teeth']}T)  dist={actual:.2f}/{expected}  ratio={ratio:.2f}:1"
                        r["ratio"] = ratio

        elif ctype == "rack_pinion":
            g_id, rack_id = conn.get("gear"), conn.get("rack")
            sg, pg = get_spec(g_id)
            sr, pr = get_spec(rack_id)
            if not sg or not sr:
                r["msg"] = "Part not found"
            else:
                g_r = sg["radius_studs"]
                d = dist_perp(pg["pos"], pr["pos"], pr.get("axis", "x"))
                if abs(d - g_r) > 0.6:
                    r["msg"] = f"Gear {g_id} is {d:.2f} studs from rack, need {g_r} (gear radius). Move gear {g_r - d:+.2f} studs."
                else:
                    r["ok"] = True
                    r["msg"] = f"Gear {g_id} ({sg['teeth']}T) drives rack {rack_id}  d={d:.2f}/{g_r}  → rotation→linear"

        elif ctype == "axle_through":
            ax_id, pt_id = conn.get("axle"), conn.get("part")
            sax, pax = get_spec(ax_id)
            spt, ppt = get_spec(pt_id)
            if not sax or not spt:
                r["msg"] = "Part not found"
            else:
                d = dist_perp(ppt["pos"], pax["pos"], pax.get("axis", "x"))
                if d > 0.6:
                    r["msg"] = f"Axle {ax_id} misses {pt_id} by {d:.2f} studs. Align {pt_id} with axle line."
                else:
                    r["ok"] = True
                    r["msg"] = f"Axle {ax_id} → {pt_id}  d={d:.2f}"

        elif ctype == "bush_on_axle":
            ax_id, bush_id = conn.get("axle"), conn.get("bush")
            sax, pax = get_spec(ax_id)
            sb, pb = get_spec(bush_id)
            if not sax or not sb:
                r["msg"] = "Part not found"
            else:
                d = dist_perp(pb["pos"], pax["pos"], pax.get("axis", "x"))
                if d > 0.6:
                    r["msg"] = f"Bush {bush_id} not on axle {ax_id} (d={d:.2f})"
                else:
                    r["ok"] = True
                    r["msg"] = f"Bush {bush_id} on axle {ax_id} ✓"

        elif ctype == "pin_in_beam":
            beam_id = conn.get("beam")
            hole = conn.get("hole")
            sb, _ = get_spec(beam_id)
            if not sb:
                r["msg"] = f"Beam {beam_id} not found"
            elif hole not in sb.get("holes", []):
                r["msg"] = f"Beam {beam_id} has no hole at index {hole} (holes: {sb.get('holes')})"
            else:
                r["ok"] = True
                r["msg"] = f"Pin in beam {beam_id} hole {hole} ✓"
        else:
            r["msg"] = f"Unknown connection type '{ctype}'"

        r["raw"] = conn
        results.append(r)

    return results


def dist3(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def dist_perp(point, origin, axis):
    px, py, pz = point
    ox, oy, oz = origin
    if axis == "x":
        return math.sqrt((py - oy) ** 2 + (pz - oz) ** 2)
    elif axis == "y":
        return math.sqrt((px - ox) ** 2 + (pz - oz) ** 2)
    else:
        return math.sqrt((px - ox) ** 2 + (py - oy) ** 2)


def compute_bbox(assembly, lib):
    parts = assembly.get("parts", [])
    if not parts:
        return None
    xs, ys, zs = [], [], []
    for p in parts:
        if p.get("type") not in lib:
            continue
        pos = p.get("pos", [0, 0, 0])
        xs.append(pos[0]); ys.append(pos[1]); zs.append(pos[2])
    if not xs:
        return None
    return {
        "min": [min(xs), min(ys), min(zs)],
        "max": [max(xs), max(ys), max(zs)],
        "size": [max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)]
    }


if __name__ == "__main__":
    app.run(debug=True, port=5050)
