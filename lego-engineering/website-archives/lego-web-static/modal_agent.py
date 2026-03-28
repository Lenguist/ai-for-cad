"""
LEGO Mechanic Agent — Modal endpoint
Uses Claude Sonnet 4.6 with tool use to generate + validate LEGO assemblies.
Deploy: modal deploy modal_agent.py
"""

import modal
import json
import math
import os

app = modal.App("lego-mechanic-agent")

image = (
    modal.Image.debian_slim()
    .pip_install("anthropic", "fastapi", "uvicorn")
)

# ── Parts library (embedded) ──────────────────────────────────────────────────

PARTS_LIBRARY = {
  "beam-3":  {"name":"Technic Beam 3","category":"beam","length":3,"radius_studs":None,"teeth":None,"description":"Straight beam with 3 holes"},
  "beam-5":  {"name":"Technic Beam 5","category":"beam","length":5,"radius_studs":None,"teeth":None,"description":"Straight beam with 5 holes"},
  "beam-7":  {"name":"Technic Beam 7","category":"beam","length":7,"radius_studs":None,"teeth":None,"description":"Straight beam with 7 holes"},
  "beam-9":  {"name":"Technic Beam 9","category":"beam","length":9,"radius_studs":None,"teeth":None,"description":"Straight beam with 9 holes"},
  "beam-11": {"name":"Technic Beam 11","category":"beam","length":11,"radius_studs":None,"teeth":None,"description":"Straight beam with 11 holes"},
  "beam-15": {"name":"Technic Beam 15","category":"beam","length":15,"radius_studs":None,"teeth":None,"description":"Straight beam with 15 holes"},
  "gear-8t": {"name":"Gear 8 Tooth","category":"gear","length":None,"radius_studs":1,"teeth":8,"description":"Small spur gear, 8 teeth. Radius 1 stud."},
  "gear-16t":{"name":"Gear 16 Tooth","category":"gear","length":None,"radius_studs":2,"teeth":16,"description":"Medium spur gear, 16 teeth. Radius 2 studs."},
  "gear-24t":{"name":"Gear 24 Tooth","category":"gear","length":None,"radius_studs":3,"teeth":24,"description":"Large spur gear, 24 teeth. Radius 3 studs."},
  "gear-40t":{"name":"Gear 40 Tooth","category":"gear","length":None,"radius_studs":5,"teeth":40,"description":"Extra-large spur gear, 40 teeth. Radius 5 studs."},
  "gear-worm":{"name":"Worm Gear","category":"gear","length":None,"radius_studs":1,"teeth":1,"description":"Worm gear. 1 tooth effective. Meshes with spur gears for high reduction."},
  "rack-4":  {"name":"Rack Gear 1x4","category":"rack","length":4,"radius_studs":None,"teeth":4,"description":"Rack gear, 4 studs long. Converts rotation to linear motion."},
  "axle-3":  {"name":"Axle 3","category":"axle","length":3,"radius_studs":None,"teeth":None,"description":"Axle 3 studs long."},
  "axle-4":  {"name":"Axle 4","category":"axle","length":4,"radius_studs":None,"teeth":None,"description":"Axle 4 studs long."},
  "axle-5":  {"name":"Axle 5","category":"axle","length":5,"radius_studs":None,"teeth":None,"description":"Axle 5 studs long."},
  "axle-6":  {"name":"Axle 6","category":"axle","length":6,"radius_studs":None,"teeth":None,"description":"Axle 6 studs long."},
  "axle-8":  {"name":"Axle 8","category":"axle","length":8,"radius_studs":None,"teeth":None,"description":"Axle 8 studs long."},
  "axle-10": {"name":"Axle 10","category":"axle","length":10,"radius_studs":None,"teeth":None,"description":"Axle 10 studs long."},
  "pin":      {"name":"Technic Pin","category":"pin","length":1,"radius_studs":None,"teeth":None,"description":"Standard pin, 1 stud."},
  "pin-friction":{"name":"Pin with Friction","category":"pin","length":1,"radius_studs":None,"teeth":None,"description":"Friction pin."},
  "pin-long": {"name":"Pin 3L Long","category":"pin","length":3,"radius_studs":None,"teeth":None,"description":"Long pin, 3 studs."},
  "bush":     {"name":"Technic Bush","category":"connector","length":1,"radius_studs":None,"teeth":None,"description":"Axle bush / spacer."},
  "connector-2x2":{"name":"Connector 2x2","category":"connector","length":2,"radius_studs":None,"teeth":None,"description":"Perpendicular connector. Joins beams at 90 degrees."},
}

PARTS_SUMMARY = "\n".join(
    f"  {pid}: {spec['category']}"
    + (f", length={spec['length']}" if spec['length'] else "")
    + (f", teeth={spec['teeth']}, radius={spec['radius_studs']}" if spec['teeth'] is not None else "")
    + f" — {spec['description']}"
    for pid, spec in PARTS_LIBRARY.items()
)

SYSTEM_PROMPT = f"""You are a LEGO Technic assembly designer. Your job is to generate valid LEGO Technic assemblies from text prompts.

AVAILABLE PARTS:
{PARTS_SUMMARY}

ASSEMBLY JSON FORMAT:
{{
  "name": "descriptive name",
  "parts": [
    {{"id": "unique_id", "type": "part-type", "pos": [x, y, z], "axis": "x|y|z"}}
  ]
}}

CRITICAL RULES:
1. Every part needs: unique id, valid type from the list above, pos [x,y,z] in stud units, axis (x/y/z)
2. Default axes: beams → "x", gears/axles → "y"
3. GEAR MESHING: Two spur gears mesh when their centers are EXACTLY (r1 + r2) studs apart AND they share the same axis.
   - gear-8t (r=1) + gear-24t (r=3): centers must be 4.0 studs apart, same axis
   - gear-8t (r=1) + gear-16t (r=2): centers must be 3.0 studs apart, same axis
   - gear-8t (r=1) + gear-40t (r=5): centers must be 6.0 studs apart, same axis
   - gear-24t (r=3) + gear-40t (r=5): centers must be 8.0 studs apart, same axis
4. RACK AND PINION: gear-8t (r=1) meshes with rack-4 when gear center is EXACTLY 1.0 stud perpendicular to the rack's axis direction.
5. WORM GEAR: gear-worm (r=1) meshes with spur gears when their axes are PERPENDICULAR (not the same).

Use integer or simple decimal positions. Call write_assembly with your design. Fix any validation errors and try again.
"""

# ── Validator (ported from validator.py) ─────────────────────────────────────

def _euclidean(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def _dist_perp(gear_pos, rack_pos, rack_axis):
    gx, gy, gz = gear_pos
    rx, ry, rz = rack_pos
    if rack_axis == "x":
        return math.sqrt((gy - ry) ** 2 + (gz - rz) ** 2)
    elif rack_axis == "y":
        return math.sqrt((gx - rx) ** 2 + (gz - rz) ** 2)
    else:
        return math.sqrt((gx - rx) ** 2 + (gy - ry) ** 2)

def validate_assembly(assembly, parts_library):
    errors, warnings = [], []
    parts = assembly.get("parts", [])
    if not parts:
        errors.append("Assembly has no parts.")
        return errors, warnings
    seen = set()
    valid_parts = []
    for part in parts:
        pid = part.get("id", "?")
        ptype = part.get("type", "")
        pos = part.get("pos")
        axis = part.get("axis", "y")
        if not ptype:
            errors.append(f"Part '{pid}': missing 'type'.")
            continue
        if ptype not in parts_library:
            errors.append(f"Part '{pid}': unknown type '{ptype}'. Valid: {', '.join(sorted(parts_library.keys()))}")
            continue
        if pid in seen:
            errors.append(f"Duplicate part ID: '{pid}'")
            continue
        seen.add(pid)
        if pos is None or not isinstance(pos, list) or len(pos) != 3:
            errors.append(f"Part '{pid}': 'pos' must be [x,y,z].")
            continue
        if axis not in ("x", "y", "z"):
            errors.append(f"Part '{pid}': 'axis' must be x, y, or z.")
            continue
        valid_parts.append(part)
    return errors, warnings

def compute_kinematics(assembly, parts_library):
    parts = assembly.get("parts", [])
    result = {}
    gears, racks = [], []
    for part in parts:
        pt = part.get("type", "")
        if pt not in parts_library:
            continue
        spec = parts_library[pt]
        if spec.get("category") == "gear":
            gears.append({"id": part["id"], "type": pt, "teeth": spec["teeth"],
                          "radius": spec["radius_studs"], "pos": part.get("pos", [0,0,0]),
                          "axis": part.get("axis", "y")})
        elif spec.get("category") == "rack":
            racks.append({"id": part["id"], "pos": part.get("pos", [0,0,0]),
                          "axis": part.get("axis", "x")})
    gear_pairs = []
    for i in range(len(gears)):
        for j in range(i + 1, len(gears)):
            g1, g2 = gears[i], gears[j]
            is_worm = g1["teeth"] == 1 or g2["teeth"] == 1
            if not is_worm and g1["axis"] != g2["axis"]:
                continue
            if is_worm and g1["axis"] == g2["axis"]:
                continue
            dist = _euclidean(g1["pos"], g2["pos"])
            expected = g1["radius"] + g2["radius"]
            if abs(dist - expected) < 0.75:
                ratio = round(g2["teeth"] / g1["teeth"], 3)
                gear_pairs.append({"gear1": g1["id"], "gear2": g2["id"],
                                   "teeth1": g1["teeth"], "teeth2": g2["teeth"],
                                   "ratio": ratio, "ratio_str": f"{g2['teeth']}:{g1['teeth']}"})
    if gear_pairs:
        result["gear_pairs"] = gear_pairs
        r = gear_pairs[0]["ratio"]
        result["summary"] = f"{gear_pairs[0]['ratio_str']} ({'speed up' if r < 1 else 'speed down'}, {r:.2f}x)"
    rack_pinion = []
    for rack in racks:
        for gear in gears:
            dist = _dist_perp(gear["pos"], rack["pos"], rack["axis"])
            if abs(dist - gear["radius"]) < 0.75:
                rack_pinion.append({"gear": gear["id"], "rack": rack["id"],
                    "note": f"Gear '{gear['id']}' ({gear['teeth']}T) drives rack '{rack['id']}' → rotational→linear"})
    if rack_pinion:
        result["rack_pinion"] = rack_pinion
        result["motion_type"] = "Rotational → Linear"
    return result

# ── FastAPI app ───────────────────────────────────────────────────────────────

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

web_app = FastAPI()
web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

TOOLS = [
    {
        "name": "write_assembly",
        "description": (
            "Submit a LEGO Technic assembly for validation. "
            "Returns a list of errors. If empty, the assembly is valid and you are done. "
            "If there are errors, fix them and call again."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "assembly_json": {
                    "type": "string",
                    "description": "The complete assembly as a JSON string with 'name' and 'parts' fields."
                }
            },
            "required": ["assembly_json"]
        }
    }
]

@web_app.get("/health")
async def health():
    return {"ok": True}

@web_app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "").strip()
    if not prompt:
        return {"error": "no prompt"}

    async def event_stream():
        import anthropic
        client = anthropic.AsyncAnthropic()

        messages = [{"role": "user", "content": f"Design a LEGO Technic assembly for: {prompt}"}]
        max_rounds = 4
        last_assembly = None

        for round_num in range(1, max_rounds + 1):
            # Stream assistant response
            thinking_buf = ""
            response = None

            async with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            ) as stream:
                async for event in stream:
                    if hasattr(event, 'type') and event.type == 'content_block_delta':
                        if hasattr(event, 'delta') and hasattr(event.delta, 'text'):
                            chunk = event.delta.text
                            thinking_buf += chunk
                            yield f"data: {json.dumps({'type': 'thinking', 'text': chunk})}\n\n"
                response = await stream.get_final_message()

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                if last_assembly:
                    yield f"data: {json.dumps({'type': 'done', 'assembly': last_assembly, 'rounds': round_num - 1})}\n\n"
                else:
                    yield f"data: {json.dumps({'type': 'error', 'message': 'Claude finished without generating an assembly.'})}\n\n"
                return

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type != "tool_use" or block.name != "write_assembly":
                        continue

                    yield f"data: {json.dumps({'type': 'tool_call', 'round': round_num})}\n\n"

                    try:
                        assembly = json.loads(block.input["assembly_json"])
                        last_assembly = assembly
                        errors, warnings = validate_assembly(assembly, PARTS_LIBRARY)
                        kinematics = compute_kinematics(assembly, PARTS_LIBRARY) if not errors else {}
                        valid = not errors

                        yield f"data: {json.dumps({'type': 'validation', 'valid': valid, 'errors': errors, 'warnings': warnings, 'round': round_num, 'kinematics': kinematics})}\n\n"

                        if valid:
                            yield f"data: {json.dumps({'type': 'done', 'assembly': assembly, 'rounds': round_num})}\n\n"
                            return

                        result_text = f"Validation round {round_num} — ERRORS:\n"
                        result_text += "\n".join(f"- {e}" for e in errors)
                        if warnings:
                            result_text += "\nWARNINGS:\n" + "\n".join(f"- {w}" for w in warnings)
                        if round_num >= max_rounds:
                            result_text += f"\n\nThis was round {max_rounds} (max). Return the best assembly you have."

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_text,
                        })

                    except (json.JSONDecodeError, KeyError) as e:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"JSON parse error: {e}. Make sure assembly_json is valid JSON.",
                            "is_error": True,
                        })

                if tool_results:
                    messages.append({"role": "user", "content": tool_results})

                if round_num >= max_rounds:
                    if last_assembly:
                        yield f"data: {json.dumps({'type': 'done', 'assembly': last_assembly, 'rounds': round_num, 'note': 'max rounds'})}\n\n"
                    else:
                        yield f"data: {json.dumps({'type': 'error', 'message': 'Max rounds reached without valid assembly.'})}\n\n"
                    return

        if last_assembly:
            yield f"data: {json.dumps({'type': 'done', 'assembly': last_assembly, 'rounds': max_rounds})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("anthropic-secret")],
    timeout=120,
)
@modal.asgi_app()
def fastapi_app():
    return web_app
