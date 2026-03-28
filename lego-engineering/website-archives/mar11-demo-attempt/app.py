from flask import Flask, render_template, request, jsonify
import json
import os
from validator import validate_assembly, compute_kinematics

app = Flask(__name__)

BASE = os.path.dirname(__file__)
with open(os.path.join(BASE, "parts_library.json")) as f:
    PARTS = json.load(f)

CATEGORIES = sorted(set(v["category"] for v in PARTS.values()))

EXAMPLES = [
    {
        "name": "3:1 Gear Pair (8T + 24T)",
        "assembly": {
            "name": "3:1 Gear Pair",
            "parts": [
                {"id": "gear1", "type": "gear-8t",  "pos": [0, 0, 0], "axis": "y"},
                {"id": "gear2", "type": "gear-24t", "pos": [4, 0, 0], "axis": "y"},
                {"id": "axle1", "type": "axle-3",   "pos": [0, -1, 0], "axis": "y"},
                {"id": "axle2", "type": "axle-3",   "pos": [4, -1, 0], "axis": "y"},
                {"id": "beam1", "type": "beam-5",   "pos": [0, -2, 0], "axis": "x"},
            ]
        }
    },
    {
        "name": "Rack and Pinion (Rotation → Linear)",
        "assembly": {
            "name": "Rack and Pinion",
            "parts": [
                {"id": "rack1",  "type": "rack-4",  "pos": [0, 0, 0], "axis": "x"},
                {"id": "gear1",  "type": "gear-8t", "pos": [2, 1, 0], "axis": "y"},
                {"id": "axle1",  "type": "axle-5",  "pos": [2, -1, 0], "axis": "y"},
                {"id": "beam1",  "type": "beam-5",  "pos": [0, 2, -1], "axis": "x"},
                {"id": "beam2",  "type": "beam-5",  "pos": [0, 2, 1],  "axis": "x"},
            ]
        }
    },
    {
        "name": "Compound Gear Train (9:1 reduction)",
        "assembly": {
            "name": "9:1 Gear Train",
            "parts": [
                {"id": "g1", "type": "gear-8t",  "pos": [0, 0, 0], "axis": "y"},
                {"id": "g2", "type": "gear-24t", "pos": [4, 0, 0], "axis": "y"},
                {"id": "g3", "type": "gear-8t",  "pos": [4, 0, 0], "axis": "y"},
                {"id": "g4", "type": "gear-24t", "pos": [8, 0, 0], "axis": "y"},
                {"id": "a1", "type": "axle-5",   "pos": [0, -2, 0], "axis": "y"},
                {"id": "a2", "type": "axle-5",   "pos": [4, -2, 0], "axis": "y"},
                {"id": "a3", "type": "axle-5",   "pos": [8, -2, 0], "axis": "y"},
                {"id": "b1", "type": "beam-9",   "pos": [0, -3, -1], "axis": "x"},
                {"id": "b2", "type": "beam-9",   "pos": [0, -3, 1],  "axis": "x"},
            ]
        }
    },
    {
        "name": "Simple Beam Frame",
        "assembly": {
            "name": "Beam Frame",
            "parts": [
                {"id": "b1", "type": "beam-9",  "pos": [0, 0, 0], "axis": "x"},
                {"id": "b2", "type": "beam-9",  "pos": [0, 0, 8], "axis": "x"},
                {"id": "b3", "type": "beam-7",  "pos": [0, 0, 0], "axis": "z"},
                {"id": "b4", "type": "beam-7",  "pos": [8, 0, 0], "axis": "z"},
                {"id": "p1", "type": "pin",     "pos": [0, 0, 0], "axis": "y"},
                {"id": "p2", "type": "pin",     "pos": [8, 0, 0], "axis": "y"},
                {"id": "p3", "type": "pin",     "pos": [0, 0, 8], "axis": "y"},
                {"id": "p4", "type": "pin",     "pos": [8, 0, 8], "axis": "y"},
            ]
        }
    },
]


@app.route("/")
def index():
    return render_template("parts.html", parts=PARTS, categories=CATEGORIES,
                           current_category="all", query="")


@app.route("/parts")
def parts():
    category = request.args.get("category", "all")
    q = request.args.get("q", "").lower().strip()
    filtered = {
        k: v for k, v in PARTS.items()
        if (category == "all" or v["category"] == category)
        and (not q or q in v["name"].lower() or q in k.lower() or q in v["description"].lower())
    }
    return render_template("parts.html", parts=filtered, categories=CATEGORIES,
                           current_category=category, query=q)


@app.route("/assemble")
def assemble():
    return render_template("assemble.html", parts=PARTS, examples=EXAMPLES)


@app.route("/api/assemble", methods=["POST"])
def api_assemble():
    data = request.get_json(force=True)
    assembly = data.get("assembly", {})

    errors, warnings = validate_assembly(assembly, PARTS)

    kinematics = {}
    if not errors:
        kinematics = compute_kinematics(assembly, PARTS)

    geometry = build_geometry(assembly)

    return jsonify({
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "kinematics": kinematics,
        "geometry": geometry,
        "part_count": len(assembly.get("parts", [])),
    })


def build_geometry(assembly):
    result = []
    for part in assembly.get("parts", []):
        pt = part.get("type", "")
        if pt not in PARTS:
            continue
        spec = PARTS[pt]
        result.append({
            "id": part.get("id", ""),
            "type": pt,
            "category": spec["category"],
            "name": spec["name"],
            "pos": part.get("pos", [0, 0, 0]),
            "axis": part.get("axis", "x"),
            "color": spec.get("color", "#aaaaaa"),
            "length": spec.get("length"),
            "radius_studs": spec.get("radius_studs"),
            "teeth": spec.get("teeth"),
        })
    return result


if __name__ == "__main__":
    app.run(debug=True, port=5050)
