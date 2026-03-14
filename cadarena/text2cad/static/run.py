"""
Static benchmark runner for text2cad.

Reads:   dataset/prompts.json
Runs:    methods/<method_id>/  (via models.py)
Writes:  methods/<method_id>/outputs/<prompt_id>.json
         methods/<method_id>/outputs/<prompt_id>.py   (generated code)
         methods/<method_id>/outputs/<prompt_id>.stl  (if execution succeeded)

Usage:
    python run.py --method claude-opus-4-6
    python run.py --method gpt-4o --tiers 1 2
    python run.py --method claude-sonnet-4-6 --prompts t1_01 t1_02
    python run.py --method deepseek-v3 --dry-run
    python run.py --method zoo-ml-ephant --no-execute
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# ── Paths ──────────────────────────────────────────────────────────────────

STATIC_DIR  = Path(__file__).parent
DATASET_DIR = STATIC_DIR / "dataset"
METHODS_DIR = STATIC_DIR / "methods"
EVAL_DIR    = STATIC_DIR.parent.parent / "eval"  # cadarena/eval/

# Load .env from eval dir (where API keys live)
load_dotenv(EVAL_DIR / ".env")
load_dotenv()  # also check cwd

# Add eval/ to path so we can import models.py, execute.py
sys.path.insert(0, str(EVAL_DIR))

from models import load_model, ALL_MODELS
from execute import validate_cadquery, validate_zoo_stl


# ── CLI ────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="CAD Arena static benchmark runner")
    p.add_argument("--method", required=True,
                   help=f"Method ID to run. Available: {list(ALL_MODELS)}")
    p.add_argument("--tiers", nargs="+", type=int, default=None,
                   help="Filter to specific tiers (1-4). Default: all.")
    p.add_argument("--prompts", nargs="+", default=None,
                   help="Specific prompt IDs to run (e.g. t1_01 t2_03).")
    p.add_argument("--dry-run", action="store_true",
                   help="Print plan without calling any APIs.")
    p.add_argument("--no-execute", action="store_true",
                   help="Skip CadQuery execution (API calls + save code only).")
    p.add_argument("--resume", action="store_true",
                   help="Skip prompts that already have outputs.")
    return p.parse_args()


# ── Load prompts ───────────────────────────────────────────────────────────

def load_prompts(tiers=None, prompt_ids=None):
    path = DATASET_DIR / "prompts.json"
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(1)
    with open(path) as f:
        data = json.load(f)
    prompts = data["prompts"]
    if tiers:
        prompts = [p for p in prompts if p["tier"] in tiers]
    if prompt_ids:
        prompts = [p for p in prompts if p["id"] in prompt_ids]
    return prompts


# ── Status helpers ─────────────────────────────────────────────────────────

def icon(exec_result: dict) -> str:
    if exec_result.get("stl_exported"):
        return "✓"
    if exec_result.get("exec_valid") is False:
        return "✗"
    if exec_result.get("syntax_valid") is False:
        return "S"  # syntax error
    return "?"


def print_row(prompt_id, tier, latency, exec_result, attempts=1):
    ic = icon(exec_result)
    bbox = exec_result.get("bbox")
    bbox_str = f"  bbox={bbox['x']:.1f}×{bbox['y']:.1f}×{bbox['z']:.1f}" if bbox else ""
    sc_str = f"  attempts={attempts}" if attempts > 1 else ""
    print(f"  [{ic}] {prompt_id} (t{tier})  {latency:.1f}s{bbox_str}{sc_str}")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    method_id = args.method

    # Load prompts
    prompts = load_prompts(tiers=args.tiers, prompt_ids=args.prompts)
    if not prompts:
        print("No prompts matched the filters.")
        sys.exit(0)

    # Output directory
    out_dir = METHODS_DIR / method_id / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== CAD Arena Static Benchmark ===")
    print(f"Method : {method_id}")
    print(f"Prompts: {len(prompts)}")
    print(f"Output : {out_dir}")

    if args.dry_run:
        print("\n[DRY RUN] Would run:")
        for p in prompts:
            print(f"  {p['id']} (tier {p['tier']}): {p['prompt'][:60]}")
        return

    # Load model
    try:
        model = load_model(method_id)
    except Exception as e:
        print(f"\nERROR loading model: {e}")
        sys.exit(1)

    print()
    results = []
    passed = 0

    for p in prompts:
        pid   = p["id"]
        tier  = p["tier"]
        prompt = p["prompt"]

        # Resume: skip if already done
        result_file = out_dir / f"{pid}.json"
        if args.resume and result_file.exists():
            with open(result_file) as f:
                saved = json.load(f)
            se = saved.get("exec_result", {}).get("stl_exported")
            print(f"  [~] {pid} (t{tier})  skipped (already done, stl={se})")
            results.append(saved)
            if se:
                passed += 1
            continue

        # Generate
        gen = model.generate(pid, prompt)

        # Execute / validate
        exec_result: dict = {}
        if args.no_execute:
            exec_result = {"note": "execution skipped (--no-execute)"}
        elif gen.output_type == "kcl":
            stl_b64  = gen.metadata.get("stl_bytes")
            step_b64 = gen.metadata.get("step_bytes")
            exec_result = validate_zoo_stl(stl_b64, step_b64, out_dir, pid)
        elif gen.output_type == "cadquery" and gen.code and not gen.error:
            exec_result = validate_cadquery(gen.code, out_dir, pid, timeout=60)
        elif gen.error:
            exec_result = {"exec_valid": False, "exec_error": gen.error}

        # Save generated code
        if gen.code:
            ext = "scad" if gen.output_type == "openscad" else ("kcl" if gen.output_type == "kcl" else "py")
            (out_dir / f"{pid}.{ext}").write_text(gen.code, encoding="utf-8")

        # Copy STL to outputs if validated via Zoo path (stl_path already in out_dir)
        stl_path = exec_result.get("stl_path")

        # Build result record
        record = {
            "method_id":   method_id,
            "prompt_id":   pid,
            "tier":        tier,
            "prompt":      prompt,
            "latency_s":   round(gen.latency_s, 2),
            "output_type": gen.output_type,
            "attempts":    gen.attempts,
            "error":       gen.error,
            "exec_result": exec_result,
            "stl_path":    stl_path,
        }
        with open(result_file, "w") as f:
            json.dump(record, f, indent=2)

        if exec_result.get("stl_exported"):
            passed += 1

        print_row(pid, tier, gen.latency_s, exec_result, gen.attempts)
        results.append(record)

    # Summary
    total = len(prompts)
    pct = round(100 * passed / total) if total else 0
    print(f"\n=== Summary: {passed}/{total} valid STL ({pct}%) ===\n")

    summary = {
        "method_id":     method_id,
        "prompts_total": total,
        "prompts_passed": passed,
        "valid_stl_pct": pct,
        "run_date":      time.strftime("%Y-%m-%d"),
    }
    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary saved to {out_dir / 'summary.json'}")


if __name__ == "__main__":
    main()
