"""
Modal runner for Text2CAD (NeurIPS 2024 Spotlight).

Text2CAD generates CAD command sequences from text descriptions, using the
DeepCAD format (sketch + extrude operations). This runner:
  1. Loads the Text2CAD model weights from HuggingFace on an A10G GPU
  2. Accepts a list of text prompts
  3. Returns decoded CAD sequences + exported STL bytes

Usage (local, calls Modal):
    python modal_text2cad.py --prompts "A cube 20mm" "A cylinder 10mm diameter"
    python modal_text2cad.py --prompts-file prompts_text.txt --out results/text2cad/

Requires:
    pip install modal
    modal token new   # authenticate once

Environment variables needed in Modal secrets:
    (none — model weights are downloaded from public HuggingFace)

References:
    Paper:   https://sadilkhan.github.io/text2cad-project/
    GitHub:  https://github.com/SadilKhan/Text2CAD
    Weights: https://huggingface.co/sadilkhan/Text2CAD (verify slug)
"""

import json
import sys
import time
from pathlib import Path

# ── NOTE ──────────────────────────────────────────────────────────────────
# This scaffold is ready to run once:
#   1. modal is installed:  pip install modal
#   2. You're authenticated: modal token new
#   3. We confirm the HuggingFace model slug for Text2CAD weights
#      (check: https://huggingface.co/sadilkhan)
#
# The GPU image build (~5-10 min first time) is cached by Modal automatically.
# Subsequent cold starts take ~30-60s; warm inference ~2-5s per prompt.
# ─────────────────────────────────────────────────────────────────────────

import modal

# ── Docker image ──────────────────────────────────────────────────────────
# Builds once, cached. Installs Text2CAD + its CAD reconstruction dependencies.

TEXT2CAD_IMAGE = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install(
        "git", "wget", "libgl1", "libglib2.0-0",
        # OpenCASCADE dependencies for pythonocc (needed to export STEP/STL)
        "libboost-all-dev",
    )
    .pip_install(
        "torch==2.2.0",
        "transformers>=4.40.0",
        "huggingface_hub>=0.22.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "trimesh>=4.0.0",
        "tqdm",
    )
    # Clone Text2CAD repo (contains model code + reconstruction utilities)
    .run_commands(
        "git clone https://github.com/SadilKhan/Text2CAD /opt/text2cad",
        # Install Text2CAD's own requirements if present
        "pip install -r /opt/text2cad/requirements.txt || true",
    )
)

app = modal.App("cad-arena-text2cad")

# ── Modal function ────────────────────────────────────────────────────────

@app.function(
    image=TEXT2CAD_IMAGE,
    gpu="A10G",           # ~24GB VRAM — sufficient for Text2CAD
    timeout=600,          # 10 min max per batch
    memory=16384,         # 16GB RAM
)
def run_text2cad(prompts: list[str], model_variant: str = "base") -> list[dict]:
    """
    Run Text2CAD inference on a list of prompts.

    Args:
        prompts: list of text descriptions
        model_variant: "base" or "large" (default: "base")

    Returns:
        list of dicts, one per prompt:
        {
            "prompt": str,
            "success": bool,
            "stl_bytes": bytes | None,   # STL mesh bytes if successful
            "step_bytes": bytes | None,  # STEP bytes if successful
            "cad_sequence": list | None, # raw decoded CAD commands
            "error": str | None,
            "latency_s": float,
        }
    """
    import sys
    import traceback
    import torch
    sys.path.insert(0, "/opt/text2cad")

    # ── TODO: update these paths once we confirm the HF model slug ────────
    # Currently a placeholder — needs to be verified against:
    # https://huggingface.co/sadilkhan
    HF_MODEL_ID = "sadilkhan/Text2CAD"   # VERIFY THIS SLUG

    results = []

    print(f"[Text2CAD] Loading model: {HF_MODEL_ID}")
    t_load = time.time()

    try:
        # ── Model loading ─────────────────────────────────────────────────
        # Text2CAD uses a T5-based encoder + custom CAD decoder.
        # The exact loading API depends on the repo structure.
        # This is the expected interface based on the paper/repo README.

        from huggingface_hub import snapshot_download
        model_dir = snapshot_download(HF_MODEL_ID)

        # Import Text2CAD model class (adjust import path to match repo)
        try:
            from text2cad.model import Text2CADModel          # option A
        except ImportError:
            from model.text2cad import Text2CADModel          # option B

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[Text2CAD] Device: {device}, VRAM: {torch.cuda.get_device_properties(0).total_memory // 1e9:.0f}GB")

        model = Text2CADModel.from_pretrained(model_dir)
        model = model.to(device).eval()
        print(f"[Text2CAD] Model loaded in {time.time()-t_load:.1f}s")

    except Exception as e:
        # Model loading failed — return error for all prompts
        err = f"Model load failed: {e}\n{traceback.format_exc()}"
        print(f"[Text2CAD] ERROR: {err}")
        return [{"prompt": p, "success": False, "error": err, "latency_s": 0.0,
                 "stl_bytes": None, "step_bytes": None, "cad_sequence": None}
                for p in prompts]

    # ── Per-prompt inference ──────────────────────────────────────────────
    for prompt in prompts:
        t0 = time.time()
        row = {"prompt": prompt, "success": False, "stl_bytes": None,
               "step_bytes": None, "cad_sequence": None, "error": None}
        try:
            # Generate CAD command sequence from text
            with torch.no_grad():
                cad_sequence = model.generate(prompt)   # returns list of CAD commands

            row["cad_sequence"] = cad_sequence

            # ── Reconstruct geometry ──────────────────────────────────────
            # Text2CAD uses a DeepCAD-compatible reconstruction pipeline.
            # This converts command sequences → B-rep → STEP/STL.
            try:
                from text2cad.reconstruction import reconstruct_cad  # adjust to repo
                step_bytes, stl_bytes = reconstruct_cad(cad_sequence)
                row["stl_bytes"] = stl_bytes
                row["step_bytes"] = step_bytes
                row["success"] = True
            except Exception as e:
                # Sequence generated but reconstruction failed
                row["error"] = f"Reconstruction failed: {e}"
                row["success"] = False  # partial success — we have the sequence

        except Exception as e:
            row["error"] = f"Inference failed: {e}\n{traceback.format_exc()}"

        row["latency_s"] = round(time.time() - t0, 2)
        results.append(row)
        status = "✓" if row["success"] else "✗"
        print(f"[Text2CAD] {status} {prompt[:60]!r}  ({row['latency_s']}s)")

    return results


# ── Local entry point ─────────────────────────────────────────────────────

@app.local_entrypoint()
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run Text2CAD via Modal")
    parser.add_argument("--prompts", nargs="+", help="Text prompts to run")
    parser.add_argument("--prompts-file", help="File with one prompt per line")
    parser.add_argument("--out", default="results/text2cad", help="Output directory")
    args = parser.parse_args()

    # Collect prompts
    prompts = []
    if args.prompts:
        prompts.extend(args.prompts)
    if args.prompts_file:
        prompts.extend(Path(args.prompts_file).read_text().strip().splitlines())
    if not prompts:
        # Default: run Tier 1 prompts from our benchmark
        sys.path.insert(0, str(Path(__file__).parent))
        from prompts import PROMPTS
        prompts = [p["prompt"] for p in PROMPTS if p["tier"] == 1]
        print(f"No prompts specified — running {len(prompts)} Tier 1 benchmark prompts")

    print(f"\nSubmitting {len(prompts)} prompt(s) to Modal (Text2CAD on A10G)...")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    results = run_text2cad.remote(prompts)
    total = time.time() - t0

    # Save results
    out_file = out_dir / "results.jsonl"
    n_ok = 0
    for r in results:
        # Don't serialize bytes to JSONL — save separately
        stl_bytes = r.pop("stl_bytes", None)
        step_bytes = r.pop("step_bytes", None)
        if stl_bytes:
            slug = r["prompt"][:40].replace(" ", "_").replace("/", "-")
            (out_dir / f"{slug}.stl").write_bytes(stl_bytes)
        if step_bytes:
            slug = r["prompt"][:40].replace(" ", "_").replace("/", "-")
            (out_dir / f"{slug}.step").write_bytes(step_bytes)
        with open(out_file, "a") as f:
            f.write(json.dumps(r) + "\n")
        if r["success"]:
            n_ok += 1

    print(f"\nDone: {n_ok}/{len(results)} successful in {total:.1f}s")
    print(f"Results: {out_file}")
