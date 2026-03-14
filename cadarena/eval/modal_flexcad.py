"""
Modal runner for FlexCAD (ICLR 2025, microsoft/FlexCAD).

FlexCAD is an 8B LoRA on Llama-3 that generates quantized CAD sequences,
then reconstructs them to STL via a DeepCAD-compatible pipeline.

Pipeline on Modal:
  1. sample.py (mask_type=unconditional, conditioned on text via --text_prompt)
  2. utils/parser.py  → OBJ files
  3. utils/visual_obj.py (pythonocc) → STL files

NOTE: FlexCAD's sample.py is designed for batch eval over a dataset file.
Text-only conditioning (no existing CAD as anchor) is possible via
mask_type=unconditional but the model was trained on DeepCAD sequences, not
natural language descriptions — so quality on our text prompts may be limited.
This runner attempts it and records what comes out.

Usage:
    modal run modal_flexcad.py                          # full benchmark
    modal run modal_flexcad.py --prompts "A cube 20mm"  # quick test
"""

import json
import time
from pathlib import Path

import modal

FLEXCAD_IMAGE = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install(
        "git", "wget", "libgl1", "libglib2.0-0",
        "libboost-all-dev", "libocct-foundation-dev",
        "libocct-modeling-algorithms-dev", "libocct-modeling-data-dev",
        "libocct-visualization-dev", "libocct-ocaf-dev",
    )
    .pip_install(
        "torch==2.2.0",
        "transformers==4.38.2",
        "accelerate==0.28.0",
        "peft==0.9.0",
        "huggingface_hub>=0.22.0",
        "safetensors",
        "numpy",
        "scipy",
    )
    # pythonocc must be installed via conda-forge; use pip wheel as fallback
    .pip_install("pythonocc-core==7.7.2")
    .run_commands(
        "git clone https://github.com/microsoft/FlexCAD /opt/flexcad",
    )
)

app = modal.App("cad-arena-flexcad")

hf_secret = modal.Secret.from_name("huggingface")


@app.function(
    image=FLEXCAD_IMAGE,
    gpu="A10G",
    timeout=900,
    memory=24576,
    secrets=[hf_secret],
)
def run_flexcad(prompts: list[str]) -> list[dict]:
    """
    Run FlexCAD unconditional generation for each prompt.

    Because FlexCAD was trained on geometric sequences (not natural language),
    this uses unconditional sampling and records whether the reconstruction
    produces valid geometry. Text prompts are stored for reference only.

    Returns list of dicts: prompt, stl_bytes, success, error, latency_s
    """
    import sys, os, subprocess, tempfile, traceback
    import torch

    sys.path.insert(0, "/opt/flexcad")

    BASE_MODEL = "meta-llama/Meta-Llama-3-8B"
    LORA_ADAPTER = "microsoft/FlexCAD"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[FlexCAD] Device: {device}")

    results = []

    for prompt in prompts:
        t0 = time.time()
        row = {
            "prompt": prompt,
            "success": False,
            "stl_bytes": None,
            "cad_sequence": None,
            "error": None,
            "latency_s": 0.0,
        }

        try:
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                out_jsonl = tmp / "samples.jsonl"
                obj_dir = tmp / "objs"
                stl_dir = tmp / "stls"
                obj_dir.mkdir()
                stl_dir.mkdir()

                # Step 1: sample.py — unconditional generation, 1 sample
                result = subprocess.run(
                    [
                        "python3", "/opt/flexcad/sample.py",
                        "--model_path", LORA_ADAPTER,
                        "--num_samples", "1",
                        "--model_name", "8B",
                        "--mask_type", "unconditional",
                        "--out_path", str(out_jsonl),
                    ],
                    capture_output=True, text=True, timeout=300,
                    env={**os.environ, "CUDA_VISIBLE_DEVICES": "0"},
                )
                if result.returncode != 0:
                    row["error"] = f"sample.py failed: {result.stderr[-500:]}"
                    results.append({**row, "latency_s": round(time.time()-t0, 2)})
                    continue

                if not out_jsonl.exists():
                    row["error"] = "sample.py produced no output file"
                    results.append({**row, "latency_s": round(time.time()-t0, 2)})
                    continue

                # Grab the sequence for logging
                with open(out_jsonl) as f:
                    sample_data = [json.loads(l) for l in f if l.strip()]
                if sample_data:
                    row["cad_sequence"] = sample_data[0].get("output", "")

                # Step 2: parser.py → OBJ
                subprocess.run(
                    ["python3", "/opt/flexcad/utils/parser.py",
                     "--in_path", str(out_jsonl),
                     "--out_path", str(obj_dir)],
                    capture_output=True, text=True, timeout=120,
                )

                # Step 3: visual_obj.py → STL
                subprocess.run(
                    ["python3", "/opt/flexcad/utils/visual_obj.py",
                     "--data_folder", str(obj_dir)],
                    capture_output=True, text=True, timeout=180,
                )

                # Find any STL that was produced
                stl_files = list(obj_dir.rglob("*.stl"))
                if stl_files:
                    row["stl_bytes"] = stl_files[0].read_bytes()
                    row["success"] = True
                    print(f"[FlexCAD] ✓ {prompt[:60]!r}")
                else:
                    row["error"] = "Reconstruction produced no STL"
                    print(f"[FlexCAD] ✗ {prompt[:60]!r} — no STL")

        except Exception as e:
            row["error"] = f"{e}\n{traceback.format_exc()}"
            print(f"[FlexCAD] ✗ {prompt[:60]!r}  {e}")

        row["latency_s"] = round(time.time() - t0, 2)
        results.append(row)

    return results


@app.local_entrypoint()
def main(
    prompt: str = "",
    out: str = "results/flexcad",
):
    """
    Args:
        prompt: single prompt for a quick test (empty = run full benchmark)
        out: output directory
    """
    import sys
    if prompt:
        prompts = [prompt]
    else:
        sys.path.insert(0, str(Path(__file__).parent))
        from prompts import PROMPTS
        prompts = [p["prompt"] for p in PROMPTS]
        print(f"Running all {len(prompts)} benchmark prompts")

    print(f"Submitting {len(prompts)} prompts → Modal (FlexCAD 8B)...")
    t0 = time.time()
    results = run_flexcad.remote(prompts)

    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    n_ok = 0
    for r in results:
        stl = r.pop("stl_bytes", None)
        if stl:
            slug = r["prompt"][:40].replace(" ", "_").replace("/", "-")
            (out_dir / f"{slug}.stl").write_bytes(stl)
            n_ok += 1
        with open(out_dir / "results.jsonl", "a") as f:
            f.write(json.dumps(r) + "\n")

    print(f"\nDone: {n_ok}/{len(results)} successful in {time.time()-t0:.1f}s")
