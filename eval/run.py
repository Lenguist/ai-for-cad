"""
Main benchmark runner.

Usage:
    python run.py                          # run all available models on all prompts
    python run.py --models gpt-4o claude  # specific models only
    python run.py --tiers 1 2             # specific tiers only
    python run.py --dry-run               # print what would run, don't call APIs

Results are saved to: results/<run_id>/
  results.jsonl          — one JSON line per (model, prompt) result
  summary.json           — aggregate stats per model
  <model>/<prompt>.py    — generated CadQuery code
  <model>/<prompt>.stl   — exported mesh (if execution succeeded)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # load .env from eval/ directory

from prompts import PROMPTS
from models import load_available_models
from execute import validate_cadquery, validate_zoo_stl


# ── CLI ───────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="CAD Arena benchmark runner")
    p.add_argument("--models", nargs="+", default=None,
                   help="Model IDs to run (default: all available)")
    p.add_argument("--tiers", nargs="+", type=int, default=None,
                   help="Tiers to run (default: all 1-4)")
    p.add_argument("--dry-run", action="store_true",
                   help="Print plan without calling any APIs")
    p.add_argument("--no-execute", action="store_true",
                   help="Skip CadQuery execution (API calls only)")
    p.add_argument("--run-id", default=None,
                   help="Custom run ID (default: timestamp)")
    return p.parse_args()


# ── Helpers ───────────────────────────────────────────────────────────────

def status_icon(result: dict) -> str:
    if result.get("error"):
        return "✗"
    sv = result.get("exec_result", {}).get("syntax_valid")
    ev = result.get("exec_result", {}).get("exec_valid")
    se = result.get("exec_result", {}).get("stl_exported")
    if se:
        return "✓"
    if ev is True:
        return "~"   # executed but no STL
    if ev is None:
        return "?"   # cadquery not installed
    if sv is False:
        return "S"   # syntax error
    return "✗"


def print_live_row(model_id: str, prompt_id: str, icon: str, latency: float, note: str = ""):
    print(f"  {icon}  {model_id:<22}  {prompt_id:<8}  {latency:5.1f}s  {note}")


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # Select prompts
    prompts = PROMPTS
    if args.tiers:
        prompts = [p for p in prompts if p["tier"] in args.tiers]

    # Create run directory
    run_id = args.run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(__file__).parent / "results" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    results_file = run_dir / "results.jsonl"

    print(f"\n{'='*60}")
    print(f"  CAD Arena Benchmark Run: {run_id}")
    print(f"  Prompts : {len(prompts)} ({', '.join(f'T{t}' for t in sorted(set(p['tier'] for p in prompts)))})")
    print(f"  Results : {run_dir}")
    print(f"{'='*60}")

    if args.dry_run:
        print("\n[DRY RUN — no API calls will be made]\n")

    # Load models
    print("\nLoading models...")
    if args.dry_run:
        available = {m: None for m in (args.models or ["gpt-4o", "claude-sonnet-4-6", "gemini-2.0-flash", "zoo-ml-ephant"])}
    else:
        available = load_available_models()
        if args.models:
            available = {k: v for k, v in available.items() if k in args.models}

    if not available:
        print("\nNo models available. Check your .env file.")
        sys.exit(1)

    print(f"\nRunning {len(available)} model(s) × {len(prompts)} prompt(s) "
          f"= {len(available) * len(prompts)} total generations\n")

    if args.dry_run:
        for model_id in available:
            for prompt in prompts:
                print(f"  would run: {model_id}  ×  {prompt['id']}")
        return

    # Save run metadata
    meta = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "models": list(available.keys()),
        "prompt_ids": [p["id"] for p in prompts],
        "execute": not args.no_execute,
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    # ── Main loop ─────────────────────────────────────────────────────────
    all_results = []

    for model_id, model in available.items():
        model_dir = run_dir / model_id
        model_dir.mkdir(exist_ok=True)
        print(f"\n── {model_id} ──")

        for prompt in prompts:
            pid = prompt["id"]

            # Generate
            gen = model.generate(prompt["id"], prompt["prompt"])
            row = gen.to_dict()

            # Execute (CadQuery models)
            exec_result = {}
            if not args.no_execute and not gen.error:
                if gen.output_type == "cadquery" and gen.code:
                    exec_result = validate_cadquery(
                        gen.code, model_dir, pid, timeout=45
                    )
                elif gen.output_type == "zoo_stl":
                    stl_b64  = gen.metadata.get("stl_bytes")
                    step_b64 = gen.metadata.get("step_bytes")
                    exec_result = validate_zoo_stl(stl_b64, step_b64, model_dir, pid)

            row["exec_result"] = exec_result

            # Save code file
            if gen.code and gen.output_type == "cadquery":
                (model_dir / f"{pid}.py").write_text(gen.code, encoding="utf-8")

            # Log to JSONL
            with open(results_file, "a") as f:
                f.write(json.dumps(row) + "\n")

            all_results.append(row)

            icon = status_icon(row)
            note = gen.error or exec_result.get("exec_error", "")
            if note and len(note) > 60:
                note = note[:57] + "..."
            print_live_row(model_id, pid, icon, gen.latency_s, note)

    # ── Summary ───────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")

    summary = {}
    for model_id in available:
        rows = [r for r in all_results if r["model_id"] == model_id]
        n = len(rows)
        n_api_ok    = sum(1 for r in rows if not r.get("error"))
        n_syn_ok    = sum(1 for r in rows if r.get("exec_result", {}).get("syntax_valid"))
        n_exec_ok   = sum(1 for r in rows if r.get("exec_result", {}).get("exec_valid") is True)
        n_stl_ok    = sum(1 for r in rows if r.get("exec_result", {}).get("stl_exported"))
        avg_latency = sum(r["latency_s"] for r in rows) / n if n else 0

        summary[model_id] = {
            "total": n,
            "api_success": n_api_ok,
            "api_success_pct": round(100 * n_api_ok / n, 1) if n else 0,
            "syntax_valid": n_syn_ok,
            "syntax_valid_pct": round(100 * n_syn_ok / n, 1) if n else 0,
            "exec_valid": n_exec_ok,
            "exec_valid_pct": round(100 * n_exec_ok / n, 1) if n else 0,
            "stl_exported": n_stl_ok,
            "stl_exported_pct": round(100 * n_stl_ok / n, 1) if n else 0,
            "avg_latency_s": round(avg_latency, 2),
        }

        print(f"\n  {model_id}")
        print(f"    API success  : {n_api_ok}/{n}  ({summary[model_id]['api_success_pct']}%)")
        print(f"    Syntax valid : {n_syn_ok}/{n}  ({summary[model_id]['syntax_valid_pct']}%)")
        print(f"    Exec valid   : {n_exec_ok}/{n}  ({summary[model_id]['exec_valid_pct']}%)")
        print(f"    STL exported : {n_stl_ok}/{n}  ({summary[model_id]['stl_exported_pct']}%)")
        print(f"    Avg latency  : {summary[model_id]['avg_latency_s']}s")

    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\n  Full results saved to: {run_dir}\n")


if __name__ == "__main__":
    main()
