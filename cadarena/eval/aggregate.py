"""
Aggregate benchmark results across all methods into summary tables.

Reads:  text2cad/static/methods/*/outputs/*.json
Writes: text2cad/static/evaluation/results/
          summary_table.csv     — one row per method, all metrics
          per_tier.csv          — valid_stl_pct broken down by tier
          per_prompt.csv        — full (method × prompt) matrix
          summary_table.md      — markdown version of summary_table

Usage:
    python aggregate.py
    python aggregate.py --methods claude-opus-4-6 gpt-5.4
    python aggregate.py --out my_results/
"""

import argparse
import json
import csv
import sys
from pathlib import Path
from collections import defaultdict

EVAL_DIR    = Path(__file__).parent
STATIC_DIR  = EVAL_DIR.parent / "text2cad" / "static"
METHODS_DIR = STATIC_DIR / "methods"
RESULTS_DIR = STATIC_DIR / "evaluation" / "results"


def load_meta(method_id: str) -> dict:
    meta_path = METHODS_DIR / method_id / "meta.json"
    if meta_path.exists():
        with open(meta_path) as f:
            return json.load(f)
    return {"id": method_id, "name": method_id, "type": "unknown"}


def load_outputs(method_id: str) -> list[dict]:
    out_dir = METHODS_DIR / method_id / "outputs"
    if not out_dir.exists():
        return []
    records = []
    for jf in sorted(out_dir.glob("*.json")):
        if jf.name == "summary.json":
            continue
        with open(jf) as f:
            records.append(json.load(f))
    return records


def compute_method_stats(method_id: str, records: list[dict]) -> dict:
    if not records:
        return {}

    meta = load_meta(method_id)
    total = len(records)

    # Valid STL
    valid = sum(1 for r in records if r.get("exec_result", {}).get("stl_exported"))

    # Watertight
    wt = [r for r in records if r.get("mesh_quality", {}).get("watertight")]
    watertight = len(wt)

    # Positive volume
    pv = [r for r in records if r.get("mesh_quality", {}).get("positive_volume")]
    pos_vol = len(pv)

    # VLM score
    vlm_scores = [r["vlm_score"] for r in records
                  if r.get("vlm_score") is not None]
    vlm_avg = round(sum(vlm_scores) / len(vlm_scores), 1) if vlm_scores else None

    # Human pass
    human_pass = [r for r in records if r.get("human_pass") is True]
    human_fail = [r for r in records if r.get("human_pass") is False]
    human_reviewed = len(human_pass) + len(human_fail)
    human_pct = round(100 * len(human_pass) / human_reviewed) if human_reviewed else None

    # Latency
    latencies = [r["latency_s"] for r in records if r.get("latency_s")]
    avg_latency = round(sum(latencies) / len(latencies), 1) if latencies else None

    # Attempts (SC models)
    attempts = [r["attempts"] for r in records if r.get("attempts")]
    avg_attempts = round(sum(attempts) / len(attempts), 2) if attempts else None

    return {
        "method_id":       method_id,
        "name":            meta.get("name", method_id),
        "type":            meta.get("type", ""),
        "provider":        meta.get("provider", ""),
        "output_format":   meta.get("output", ""),
        "prompts_total":   total,
        "valid_stl":       valid,
        "valid_stl_pct":   round(100 * valid / total) if total else 0,
        "watertight":      watertight,
        "watertight_pct":  round(100 * watertight / total) if total else None,
        "pos_volume":      pos_vol,
        "pos_volume_pct":  round(100 * pos_vol / total) if total else None,
        "vlm_score_avg":   vlm_avg,
        "vlm_score_n":     len(vlm_scores),
        "human_pass":      len(human_pass) if human_reviewed else None,
        "human_pct":       human_pct,
        "human_reviewed":  human_reviewed,
        "avg_latency_s":   avg_latency,
        "avg_attempts":    avg_attempts,
    }


def compute_per_tier(method_id: str, records: list[dict]) -> dict:
    """Returns {tier: {valid_pct, watertight_pct, vlm_avg, human_pct, n}}."""
    by_tier = defaultdict(list)
    for r in records:
        by_tier[r.get("tier", 0)].append(r)

    result = {}
    for tier, recs in sorted(by_tier.items()):
        n = len(recs)
        valid = sum(1 for r in recs if r.get("exec_result", {}).get("stl_exported"))
        wt    = sum(1 for r in recs if r.get("mesh_quality", {}).get("watertight"))
        vlm   = [r["vlm_score"] for r in recs if r.get("vlm_score") is not None]
        hp    = [r for r in recs if r.get("human_pass") is not None]
        hp_pass = sum(1 for r in hp if r["human_pass"] is True)
        result[tier] = {
            "n":              n,
            "valid_stl_pct":  round(100 * valid / n) if n else 0,
            "watertight_pct": round(100 * wt / n) if n else None,
            "vlm_avg":        round(sum(vlm) / len(vlm), 1) if vlm else None,
            "human_pct":      round(100 * hp_pass / len(hp)) if hp else None,
        }
    return result


def to_pct(v):
    return f"{v}%" if v is not None else ""

def to_val(v):
    return str(v) if v is not None else ""


def write_summary_table(stats: list[dict], out_dir: Path):
    # CSV
    fieldnames = [
        "method_id", "name", "type", "provider", "output_format",
        "prompts_total", "valid_stl_pct", "watertight_pct", "pos_volume_pct",
        "vlm_score_avg", "human_pct", "avg_latency_s", "avg_attempts",
    ]
    csv_path = out_dir / "summary_table.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(stats)
    print(f"  wrote {csv_path}")

    # Markdown
    md_path = out_dir / "summary_table.md"
    with open(md_path, "w") as f:
        f.write("# CAD Arena — Text2CAD Benchmark Results\n\n")
        f.write(f"Methods: {len(stats)} | Prompts: {stats[0]['prompts_total'] if stats else 0}\n\n")
        f.write("| Method | Type | Valid STL | Watertight | VLM Score | Human Pass | Latency | Attempts |\n")
        f.write("|--------|------|-----------|------------|-----------|------------|---------|----------|\n")
        for s in stats:
            f.write(
                f"| **{s['name']}** "
                f"| {s['type']} "
                f"| {to_pct(s.get('valid_stl_pct'))} "
                f"| {to_pct(s.get('watertight_pct'))} "
                f"| {to_val(s.get('vlm_score_avg'))}/10 "
                f"| {to_pct(s.get('human_pct'))} "
                f"| {to_val(s.get('avg_latency_s'))}s "
                f"| {to_val(s.get('avg_attempts'))} |\n"
            )
    print(f"  wrote {md_path}")


def write_per_tier(all_tiers: dict[str, dict], out_dir: Path):
    # all_tiers: {method_id: {tier: stats}}
    rows = []
    for method_id, tier_data in all_tiers.items():
        meta = load_meta(method_id)
        for tier, ts in tier_data.items():
            rows.append({
                "method_id": method_id,
                "name":      meta.get("name", method_id),
                "tier":      tier,
                **{f"t{tier}_{k}": v for k, v in ts.items()},
                **ts,
            })
    if not rows:
        return
    csv_path = out_dir / "per_tier.csv"
    fieldnames = ["method_id", "name", "tier", "n", "valid_stl_pct",
                  "watertight_pct", "vlm_avg", "human_pct"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {csv_path}")


def write_per_prompt(all_records: dict[str, list], out_dir: Path):
    # Collect all prompt IDs
    all_pids = sorted({r["prompt_id"] for recs in all_records.values() for r in recs})
    csv_path = out_dir / "per_prompt.csv"
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["prompt_id", "tier", "prompt"] + list(all_records.keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()

        # Build lookup: method_id → {prompt_id → record}
        lookup = {}
        for method_id, recs in all_records.items():
            lookup[method_id] = {r["prompt_id"]: r for r in recs}

        for pid in all_pids:
            # Get tier + prompt text from any method that has it
            tier = prompt_text = ""
            for method_id in all_records:
                rec = lookup[method_id].get(pid)
                if rec:
                    tier = rec.get("tier", "")
                    prompt_text = rec.get("prompt", "")
                    break
            row = {"prompt_id": pid, "tier": tier, "prompt": prompt_text}
            for method_id in all_records:
                rec = lookup[method_id].get(pid)
                if rec:
                    stl = rec.get("exec_result", {}).get("stl_exported")
                    hp  = rec.get("human_pass")
                    vlm = rec.get("vlm_score")
                    cell = "✓" if stl else "✗"
                    if hp is True:   cell += " H✓"
                    elif hp is False: cell += " H✗"
                    if vlm is not None: cell += f" {vlm}/10"
                else:
                    cell = ""
                row[method_id] = cell
            w.writerow(row)
    print(f"  wrote {csv_path}")


def main():
    p = argparse.ArgumentParser(description="Aggregate CAD Arena benchmark results")
    p.add_argument("--methods", nargs="+", default=None,
                   help="Methods to include (default: all with outputs)")
    p.add_argument("--out", default=None,
                   help="Output directory (default: text2cad/static/evaluation/results/)")
    args = p.parse_args()

    out_dir = Path(args.out) if args.out else RESULTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # Discover methods
    if args.methods:
        methods = args.methods
    else:
        methods = sorted(
            d.name for d in METHODS_DIR.iterdir()
            if d.is_dir() and (d / "outputs").exists()
            and any((d / "outputs").glob("*.json"))
        )

    if not methods:
        print("No method outputs found.")
        sys.exit(0)

    print(f"Aggregating {len(methods)} methods: {methods}\n")

    all_stats   = []
    all_tiers   = {}
    all_records = {}

    for method_id in methods:
        records = load_outputs(method_id)
        if not records:
            print(f"  [{method_id}] no records — skipping")
            continue
        stats = compute_method_stats(method_id, records)
        tier_stats = compute_per_tier(method_id, records)
        all_stats.append(stats)
        all_tiers[method_id] = tier_stats
        all_records[method_id] = records
        print(f"  [{method_id}] {stats['valid_stl_pct']}% valid  "
              f"{stats['watertight_pct'] or '—'}% watertight  "
              f"VLM={stats['vlm_score_avg'] or '—'}  "
              f"human={stats['human_pct'] or '—'}%")

    print(f"\nWriting to {out_dir}/")
    write_summary_table(all_stats, out_dir)
    write_per_tier(all_tiers, out_dir)
    write_per_prompt(all_records, out_dir)
    print("\nDone.")


if __name__ == "__main__":
    main()
