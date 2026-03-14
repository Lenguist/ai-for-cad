"""
Merge a human_review_<method>.json (exported from review.html) back into
each per-prompt output JSON so aggregate.py can pick it up.

Usage:
    python import_human_review.py human_review_claude-opus-4-6.json
    python import_human_review.py *.json
"""

import json
import sys
from pathlib import Path

METHODS_DIR = Path(__file__).parent.parent / "text2cad" / "static" / "methods"


def import_review(review_path: Path):
    with open(review_path) as f:
        review = json.load(f)

    method_id = review.get("method_id")
    results   = review.get("results", {})

    if not method_id:
        print(f"ERROR: {review_path.name} has no method_id field")
        return

    out_dir = METHODS_DIR / method_id / "outputs"
    if not out_dir.exists():
        print(f"ERROR: outputs dir not found for {method_id}")
        return

    updated = skipped = 0
    for pid, verdict in results.items():
        jf = out_dir / f"{pid}.json"
        if not jf.exists():
            print(f"  [!] {pid}.json not found — skipping")
            skipped += 1
            continue
        with open(jf) as f:
            rec = json.load(f)
        rec["human_pass"]  = verdict.get("pass")
        rec["human_notes"] = verdict.get("notes", "")
        with open(jf, "w") as f:
            json.dump(rec, f, indent=2)
        updated += 1

    print(f"[{method_id}] updated {updated} records, skipped {skipped}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_human_review.py <human_review_*.json> ...")
        sys.exit(1)

    for arg in sys.argv[1:]:
        for path in Path(".").glob(arg) if "*" in arg else [Path(arg)]:
            print(f"Importing {path.name}...")
            import_review(path)
