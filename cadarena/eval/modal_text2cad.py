"""
Modal runner for Text2CAD (NeurIPS 2024 Spotlight, SadilKhan/Text2CAD).

Text2CAD generates CAD command sequences from natural language using a
BERT-large encoder + custom 8-layer transformer decoder trained on the
DeepCAD dataset with text annotations. Outputs STEP files.

Pipeline:
  1. Weights (Text2CAD_1.0.pth) pre-downloaded in image build from HF dataset
  2. BERT-large-uncased pre-downloaded in image build
  3. Prompts written to a temp file → YAML config → subprocess inference script
  4. Output .stp files found in dated subdirectory created by the script
  5. Each STEP converted to STL via pythonocc (BRepMesh + StlAPI_Writer)

Notes:
  - Unlike FlexCAD, Text2CAD IS text-conditioned — trained on natural language
  - Outputs STEP (B-rep), not CadQuery. Score = STL valid (geometry correct,
    dimensions not enforced by evaluation).
  - No HF token needed — weights are in a public dataset repo.

Usage:
    modal run eval/modal_text2cad.py                         # full benchmark
    modal run eval/modal_text2cad.py --prompt "A cube 20mm"  # quick test
"""

import json
import time
from pathlib import Path

import modal

TEXT2CAD_IMAGE = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install(
        "git", "wget", "libgl1", "libglib2.0-0",
        "libboost-all-dev",
        "libocct-foundation-dev",
        "libocct-modeling-algorithms-dev",
        "libocct-modeling-data-dev",
        "libocct-visualization-dev",
        "libocct-ocaf-dev",
    )
    .pip_install(
        "torch==2.2.0",
        "transformers>=4.40.0",
        "huggingface_hub>=0.22.0",
        "loguru",
        "rich",
        "pyyaml",
        "numpy",
        "scipy",
        "tqdm",
        "einops",
        "pythonocc-core==7.7.2",
    )
    .run_commands(
        # Clone the repo (contains CadSeqProc + Cad_VLM packages)
        "git clone https://github.com/SadilKhan/Text2CAD /opt/text2cad",
        "pip install -r /opt/text2cad/Cad_VLM/requirements.txt 2>/dev/null || true",
        # Pre-download BERT-large-uncased into the image (avoids cold-start re-download)
        "python3 -c \"from transformers import AutoTokenizer, AutoModel; "
        "AutoTokenizer.from_pretrained('bert-large-uncased', cache_dir='/opt/hf_cache'); "
        "AutoModel.from_pretrained('bert-large-uncased', cache_dir='/opt/hf_cache')\"",
        # Pre-download Text2CAD checkpoint (~400MB) from HF dataset repo
        "python3 -c \"from huggingface_hub import hf_hub_download; "
        "hf_hub_download(repo_id='SadilKhan/Text2CAD', filename='Text2CAD_1.0.pth', "
        "repo_type='dataset', local_dir='/opt/text2cad_weights')\"",
    )
)

app = modal.App("cad-arena-text2cad")


@app.function(
    image=TEXT2CAD_IMAGE,
    gpu="A10G",
    timeout=900,
    memory=16384,
)
def run_text2cad(prompts: list[str]) -> list[dict]:
    """
    Run Text2CAD inference on a list of text prompts.

    All prompts are processed in a single subprocess call (more efficient
    than spawning one process per prompt). The script saves .stp files
    in a dated subdirectory; we collect them and convert to STL.

    Returns list of dicts: prompt, stl_bytes, step_bytes, success, error, latency_s
    """
    import sys, os, subprocess, tempfile, traceback, yaml

    CHECKPOINT = "/opt/text2cad_weights/Text2CAD_1.0.pth"
    HF_CACHE = "/opt/hf_cache"

    results = [
        {"prompt": p, "success": False, "stl_bytes": None,
         "step_bytes": None, "error": None, "latency_s": 0.0}
        for p in prompts
    ]

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        prompt_file = tmp / "prompts.txt"
        log_dir = tmp / "output"
        log_dir.mkdir()
        cfg_path = tmp / "config.yaml"

        prompt_file.write_text("\n".join(prompts))

        config = {
            "text_encoder": {
                "text_embedder": {
                    "model_name": "bert_large_uncased",
                    "max_seq_len": 512,
                    "cache_dir": HF_CACHE,
                },
                "adaptive_layer": {
                    "in_dim": 1024, "out_dim": 1024,
                    "num_heads": 8, "dropout": 0.1,
                },
            },
            "cad_decoder": {
                "tdim": 1024, "cdim": 256,
                "num_layers": 8, "num_heads": 8,
                "dropout": 0.1, "ca_level_start": 2,
            },
            "test": {
                "batch_size": 1,
                "num_workers": 4,
                "prefetch_factor": 2,
                "log_dir": str(log_dir),
                "checkpoint_path": CHECKPOINT,
                "nucleus_prob": 0,
                "sampling_type": "max",
                "prompt_file": str(prompt_file),
            },
            "debug": False,
            "info": "Inference",
        }
        with open(cfg_path, "w") as f:
            yaml.dump(config, f)

        t0 = time.time()
        proc = subprocess.run(
            ["python3", "Cad_VLM/test_user_input.py", "-c", str(cfg_path)],
            capture_output=True, text=True, timeout=750,
            cwd="/opt/text2cad",
        )
        elapsed = time.time() - t0
        print(f"[Text2CAD] inference subprocess finished in {elapsed:.1f}s "
              f"(returncode={proc.returncode})")
        if proc.stdout:
            print(f"[Text2CAD] stdout: {proc.stdout[-500:]}")
        if proc.returncode != 0:
            print(f"[Text2CAD] stderr: {proc.stderr[-800:]}")

        # The script creates: log_dir/YYYY-MM-DD/HH:MM_d256_nl8_ca2/
        # Find that subdirectory by looking for output.pkl
        stp_dir = None
        for pkl in sorted(log_dir.rglob("output.pkl")):
            stp_dir = pkl.parent
            break

        if stp_dir is None:
            err = f"No output.pkl found — inference failed. stderr: {proc.stderr[-300:]}"
            for r in results:
                r["error"] = err
            return results

        # Collect per-prompt results (outputs saved as {index}/pred.stp)
        for i, (prompt, row) in enumerate(zip(prompts, results)):
            t1 = time.time()
            stp_file = stp_dir / str(i) / "pred.stp"
            if not stp_file.exists():
                row["error"] = f"No pred.stp for prompt index {i}"
                print(f"[Text2CAD] ✗ {prompt[:60]!r} — no STP output")
                continue

            row["step_bytes"] = stp_file.read_bytes()

            # STEP → STL via pythonocc
            try:
                from OCC.Extend.DataExchange import read_step_file
                from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
                from OCC.Core.StlAPI import StlAPI_Writer

                shape = read_step_file(str(stp_file))
                mesh = BRepMesh_IncrementalMesh(shape, 0.1, False, 0.5)
                mesh.Perform()

                stl_path = stp_dir / str(i) / "pred.stl"
                writer = StlAPI_Writer()
                writer.Write(shape, str(stl_path))

                if stl_path.exists() and stl_path.stat().st_size > 0:
                    row["stl_bytes"] = stl_path.read_bytes()
                    row["success"] = True
                    print(f"[Text2CAD] ✓ {prompt[:60]!r}")
                else:
                    row["error"] = "STEP→STL produced empty file"
                    print(f"[Text2CAD] ✗ {prompt[:60]!r} — empty STL")

            except Exception as e:
                row["error"] = f"STEP→STL failed: {e}\n{traceback.format_exc()}"
                print(f"[Text2CAD] ✗ {prompt[:60]!r} — {e}")

            row["latency_s"] = round(time.time() - t1, 2)

    return results


@app.local_entrypoint()
def main(
    prompt: str = "",
    out: str = "results/text2cad",
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

    print(f"Submitting {len(prompts)} prompt(s) → Modal (Text2CAD)...")
    t0 = time.time()
    results = run_text2cad.remote(prompts)

    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    n_ok = 0
    for r in results:
        slug = r["prompt"][:40].replace(" ", "_").replace("/", "-")
        stl = r.pop("stl_bytes", None)
        step = r.pop("step_bytes", None)
        if stl:
            (out_dir / f"{slug}.stl").write_bytes(stl)
            n_ok += 1
        if step:
            (out_dir / f"{slug}.stp").write_bytes(step)
        status = "✓" if r["success"] else "✗"
        err = f"  [{r['error'][:60]}]" if r.get("error") else ""
        print(f"  {status}  {r['prompt'][:60]!r}{err}")
        with open(out_dir / "results.jsonl", "a") as f:
            f.write(json.dumps(r) + "\n")

    print(f"\nDone: {n_ok}/{len(results)} successful in {time.time()-t0:.1f}s")
    print(f"Output: {out_dir}/")
