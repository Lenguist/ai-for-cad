"""
Print a summary table from a completed benchmark run.

Usage:
    python analyze.py                          # latest run
    python analyze.py --run 20260303_142000    # specific run
    python analyze.py --run 20260303_142000 --tier 2
"""

import argparse
import json
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--run", default=None, help="Run ID (default: latest)")
    p.add_argument("--tier", type=int, default=None, help="Filter by tier")
    return p.parse_args()


def load_run(run_id: str | None) -> tuple[Path, list[dict]]:
    results_dir = Path(__file__).parent / "results"
    if run_id:
        run_dir = results_dir / run_id
    else:
        runs = sorted(results_dir.iterdir())
        runs = [r for r in runs if r.is_dir() and not r.name.startswith(".")]
        if not runs:
            raise FileNotFoundError("No runs found in results/")
        run_dir = runs[-1]

    results_file = run_dir / "results.jsonl"
    rows = []
    with open(results_file) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return run_dir, rows


def main():
    args = parse_args()
    run_dir, rows = load_run(args.run)

    if args.tier:
        # Need to load prompts to filter by tier
        from prompts import PROMPTS
        tier_ids = {p["id"] for p in PROMPTS if p["tier"] == args.tier}
        rows = [r for r in rows if r["prompt_id"] in tier_ids]

    models = sorted(set(r["model_id"] for r in rows))
    prompt_ids = sorted(set(r["prompt_id"] for r in rows))

    # Per-model stats
    print(f"\nRun: {run_dir.name}")
    print(f"{'Model':<25} {'API%':>6} {'Syntax%':>8} {'Exec%':>7} {'STL%':>6} {'Lat(s)':>7}")
    print("─" * 62)

    for model_id in models:
        model_rows = [r for r in rows if r["model_id"] == model_id]
        n = len(model_rows)
        api_pct  = 100 * sum(1 for r in model_rows if not r.get("error")) / n
        syn_pct  = 100 * sum(1 for r in model_rows if r.get("exec_result", {}).get("syntax_valid")) / n
        exec_pct = 100 * sum(1 for r in model_rows if r.get("exec_result", {}).get("exec_valid") is True) / n
        stl_pct  = 100 * sum(1 for r in model_rows if r.get("exec_result", {}).get("stl_exported")) / n
        lat      = sum(r["latency_s"] for r in model_rows) / n
        print(f"{model_id:<25} {api_pct:>5.0f}% {syn_pct:>7.0f}% {exec_pct:>6.0f}% {stl_pct:>5.0f}% {lat:>6.1f}s")

    # Per-prompt breakdown
    print(f"\n{'Prompt':<10}", end="")
    for m in models:
        short = m[:8]
        print(f"  {short:>8}", end="")
    print()
    print("─" * (10 + 10 * len(models)))

    for pid in prompt_ids:
        print(f"{pid:<10}", end="")
        for model_id in models:
            match = next((r for r in rows if r["model_id"] == model_id and r["prompt_id"] == pid), None)
            if not match:
                print(f"  {'—':>8}", end="")
                continue
            er = match.get("exec_result", {})
            if match.get("error"):
                icon = " ✗ API"
            elif er.get("stl_exported"):
                icon = "  ✓ STL"
            elif er.get("exec_valid") is True:
                icon = " ~ exec"
            elif er.get("exec_valid") is None:
                icon = "  ? cq?"
            elif er.get("syntax_valid") is False:
                icon = " S syn"
            else:
                icon = "  ✗ err"
            print(f"  {icon:>8}", end="")
        print()

    print("\nLegend: ✓ STL exported  ~ executed (no STL)  ? cadquery not installed  S syntax error  ✗ error\n")


if __name__ == "__main__":
    main()
