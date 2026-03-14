
import sys, json, traceback, os

code_file  = sys.argv[1]
output_json = sys.argv[2]
stl_out    = sys.argv[3]

with open(code_file) as f:
    code = f.read()

result_data = {}

# 1. Syntax check
try:
    import ast as _ast
    _ast.parse(code)
    result_data["syntax_valid"] = True
except SyntaxError as e:
    result_data["syntax_valid"] = False
    result_data["syntax_error"] = str(e)
    with open(output_json, "w") as f:
        json.dump(result_data, f, indent=2)
    sys.exit(0)

# 2. Execution check (requires cadquery)
try:
    import cadquery as cq
    exec_globals = {"cq": cq}
    exec(code, exec_globals)
    res = exec_globals.get("result")
    if res is None:
        result_data["exec_valid"] = False
        result_data["exec_error"] = "No variable named 'result' found after exec()"
    else:
        result_data["exec_valid"] = True
        # Bounding box
        try:
            bb = res.val().BoundingBox()
            result_data["bbox"] = {
                "x": round(bb.xmax - bb.xmin, 3),
                "y": round(bb.ymax - bb.ymin, 3),
                "z": round(bb.zmax - bb.zmin, 3),
            }
            vol_bb = (bb.xmax-bb.xmin)*(bb.ymax-bb.ymin)*(bb.zmax-bb.zmin)
            result_data["bbox_volume_mm3"] = round(vol_bb, 3)
        except Exception as e:
            result_data["bbox_error"] = str(e)
        # STL export
        try:
            import cadquery as cq
            cq.exporters.export(res, stl_out)
            result_data["stl_exported"] = True
            result_data["stl_size_bytes"] = os.path.getsize(stl_out)
        except Exception as e:
            result_data["stl_error"] = str(e)
            result_data["stl_exported"] = False
except ImportError:
    result_data["exec_valid"] = None   # unknown — cadquery not installed
    result_data["note"] = "cadquery_not_installed_syntax_only"
except Exception as e:
    result_data["exec_valid"] = False
    result_data["exec_error"] = str(e)
    result_data["traceback"] = traceback.format_exc()

with open(output_json, "w") as f:
    json.dump(result_data, f, indent=2)
