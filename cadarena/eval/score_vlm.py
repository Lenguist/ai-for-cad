"""
VLM geometry scoring pass.

For each .stl in method outputs:
  1. Render to PNG (headless, trimesh + pyrender or matplotlib fallback)
  2. Send image + original prompt to Claude Sonnet with a scoring rubric
  3. Parse 0-10 score + short reasoning
  4. Write back into <pid>.json as vlm_score / vlm_reasoning

Usage:
    python score_vlm.py --method claude-opus-4-6
    python score_vlm.py --all
    python score_vlm.py --method gpt-5.4 --prompts t1_01 t2_03
    python score_vlm.py --method zoo-ml-ephant --model gemini  # use Gemini instead

Requires: ANTHROPIC_API_KEY (default) or GOOGLE_API_KEY (--model gemini)
          trimesh, numpy, Pillow
          Optional: pyrender (better renders) — falls back to matplotlib
"""

import argparse
import base64
import io
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

EVAL_DIR    = Path(__file__).parent
STATIC_DIR  = EVAL_DIR.parent / "text2cad" / "static"
METHODS_DIR = STATIC_DIR / "methods"

load_dotenv(EVAL_DIR / ".env")
load_dotenv()

SCORING_PROMPT = """\
You are evaluating a 3D CAD model generated from a text prompt.

Text prompt: "{prompt}"

I am showing you a rendered image of the generated 3D shape. Please score it on two dimensions:

1. **Geometric correctness** (0-5): Does the shape have the right structure, proportions, and features?
   - 0: No recognizable shape / complete failure
   - 1: Wrong shape entirely
   - 2: Roughly the right type but major features missing or wrong
   - 3: Correct overall shape, some features missing or inaccurate
   - 4: Correct shape and most features, minor inaccuracies
   - 5: Correct shape with all requested features accurately represented

2. **Dimensional accuracy** (0-5): Are sizes, ratios, and specified dimensions reflected?
   - 0: No resemblance to specified dimensions
   - 1: Gross mismatch in proportions
   - 2: Roughly right proportions but significant mismatch
   - 3: Reasonable proportions, some dimensions off
   - 4: Good dimensional accuracy, minor deviations
   - 5: Dimensions appear correct as specified

Reply in this exact format:
GEOMETRIC: <0-5>
DIMENSIONAL: <0-5>
TOTAL: <0-10>
REASONING: <1-2 sentences explaining the score>
"""


def render_stl_to_png(stl_path: Path, size: int = 512) -> bytes | None:
    """Render STL to PNG bytes. Returns None on failure."""
    try:
        import trimesh
        import numpy as np
        mesh = trimesh.load(str(stl_path), force="mesh")
        if not isinstance(mesh, trimesh.Trimesh) or len(mesh.faces) == 0:
            return None

        # Center and normalize
        mesh.apply_translation(-mesh.centroid)
        scale = mesh.bounding_box.extents.max()
        if scale > 0:
            mesh.apply_scale(1.0 / scale)

        # Try pyrender first (better quality)
        try:
            import pyrender
            scene = pyrender.Scene(ambient_light=[0.3, 0.3, 0.3])
            r_mesh = pyrender.Mesh.from_trimesh(mesh)
            scene.add(r_mesh)

            # Camera: isometric-ish view
            import pyrender
            from pyrender import PerspectiveCamera, DirectionalLight
            camera = PerspectiveCamera(yfov=0.8)
            import numpy as np
            # Position camera at 45° elevation, 45° azimuth
            cam_pose = np.array([
                [ 0.707, -0.408,  0.577, 2.0],
                [ 0.707,  0.408, -0.577,-2.0],
                [ 0.000,  0.816,  0.577, 2.0],
                [ 0.000,  0.000,  0.000, 1.0],
            ])
            scene.add(camera, pose=cam_pose)
            light = DirectionalLight(color=[1,1,1], intensity=3.0)
            scene.add(light, pose=cam_pose)

            renderer = pyrender.OffscreenRenderer(size, size)
            color, _ = renderer.render(scene)
            renderer.delete()

            from PIL import Image
            img = Image.fromarray(color)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()

        except ImportError:
            pass

        # Matplotlib fallback: simple 3D wireframe/surface
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        import numpy as np

        fig = plt.figure(figsize=(size / 100, size / 100), dpi=100)
        ax = fig.add_subplot(111, projection="3d")
        verts = mesh.vertices
        faces = mesh.faces
        poly = Poly3DCollection(verts[faces], alpha=0.7, edgecolor="none",
                                facecolor="#6090c0")
        ax.add_collection3d(poly)
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
        ax.set_box_aspect([1, 1, 1])
        ax.view_init(elev=30, azim=45)
        ax.set_axis_off()
        plt.tight_layout(pad=0)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        plt.close(fig)
        return buf.getvalue()

    except Exception as e:
        print(f"    render failed: {e}")
        return None


def parse_vlm_response(text: str) -> dict:
    """Parse GEOMETRIC/DIMENSIONAL/TOTAL/REASONING from VLM output."""
    lines = {line.split(":")[0].strip(): line.split(":", 1)[1].strip()
             for line in text.strip().splitlines() if ":" in line}
    try:
        geo  = int(lines.get("GEOMETRIC", "0").split()[0])
        dim  = int(lines.get("DIMENSIONAL", "0").split()[0])
        tot  = int(lines.get("TOTAL", str(geo + dim)).split()[0])
        reason = lines.get("REASONING", "")
    except (ValueError, IndexError):
        geo = dim = tot = 0
        reason = f"parse error: {text[:200]}"
    return {"geometric": geo, "dimensional": dim, "total": tot, "reasoning": reason}


def score_with_claude(png_bytes: bytes, prompt: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    b64 = base64.standard_b64encode(png_bytes).decode()
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64",
                                              "media_type": "image/png",
                                              "data": b64}},
                {"type": "text", "text": SCORING_PROMPT.format(prompt=prompt)},
            ],
        }],
    )
    return parse_vlm_response(resp.content[0].text)


def score_with_gemini(png_bytes: bytes, prompt: str) -> dict:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    b64 = base64.standard_b64encode(png_bytes).decode()
    resp = client.models.generate_content(
        model="gemini-3.1-pro",
        contents=[
            types.Part.from_bytes(data=png_bytes, mime_type="image/png"),
            SCORING_PROMPT.format(prompt=prompt),
        ],
    )
    return parse_vlm_response(resp.text)


def score_method(method_id: str, scorer: str = "claude", prompt_filter: list = None):
    out_dir = METHODS_DIR / method_id / "outputs"
    if not out_dir.exists():
        print(f"  No outputs dir for {method_id}")
        return

    json_files = sorted(out_dir.glob("*.json"))
    json_files = [f for f in json_files if f.name != "summary.json"]
    if prompt_filter:
        json_files = [f for f in json_files if f.stem in prompt_filter]

    if not json_files:
        print(f"  [{method_id}] no result files")
        return

    print(f"\n[{method_id}]  scorer={scorer}")
    scores = []

    for jf in json_files:
        with open(jf) as f:
            record = json.load(f)

        # Find STL
        stl_path = out_dir / f"{jf.stem}.stl"
        if not stl_path.exists():
            sp = record.get("stl_path")
            if sp:
                stl_path = Path(sp)

        if not stl_path.exists():
            print(f"  [-] {jf.stem}  no STL")
            continue

        prompt = record.get("prompt", "")
        png = render_stl_to_png(stl_path)
        if png is None:
            print(f"  [!] {jf.stem}  render failed")
            record["vlm_score"] = None
            record["vlm_reasoning"] = "render failed"
        else:
            try:
                if scorer == "gemini":
                    result = score_with_gemini(png, prompt)
                else:
                    result = score_with_claude(png, prompt)
                record["vlm_score"] = result["total"]
                record["vlm_score_detail"] = result
                scores.append(result["total"])
                print(f"  [{result['total']:2d}/10] {jf.stem}  {result['reasoning'][:60]}")
            except Exception as e:
                print(f"  [!] {jf.stem}  VLM error: {e}")
                record["vlm_score"] = None
                record["vlm_reasoning"] = str(e)

        with open(jf, "w") as f:
            json.dump(record, f, indent=2)

    if scores:
        avg = sum(scores) / len(scores)
        print(f"  → avg VLM score: {avg:.1f}/10  (n={len(scores)})")


def main():
    p = argparse.ArgumentParser(description="VLM scoring pass for CAD Arena")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--method", help="Single method ID")
    grp.add_argument("--all",    action="store_true")
    p.add_argument("--model", default="claude", choices=["claude", "gemini"],
                   help="Which VLM to use for scoring (default: claude)")
    p.add_argument("--prompts", nargs="+", default=None)
    args = p.parse_args()

    if args.all:
        methods = sorted(
            d.name for d in METHODS_DIR.iterdir()
            if d.is_dir() and (d / "outputs").exists()
        )
        for m in methods:
            score_method(m, args.model, args.prompts)
    else:
        score_method(args.method, args.model, args.prompts)

    print("\nDone. vlm_score written into each <pid>.json")


if __name__ == "__main__":
    main()
