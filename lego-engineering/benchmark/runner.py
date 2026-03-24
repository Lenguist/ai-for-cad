#!/usr/bin/env python3
"""
runner.py — Lego Engineering Benchmark Runner

Usage:
    python runner.py --task T2-01 --model claude-sonnet-4-6
    python runner.py --task T2-01 --model gpt-4o --rounds 2
    python runner.py --all --model claude-sonnet-4-6 --output results/run_01.json
    python runner.py --tier 2 --model claude-sonnet-4-6

Models supported:
    claude-sonnet-4-6, claude-opus-4-6, claude-haiku-4-5-20251001
    gpt-4o, gpt-4o-mini, o3, o4-mini
    gemini-2.5-pro, gemini-2.0-flash
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "mar11-demo-attempt"))
from validator import validate_assembly, compute_kinematics
from checker import check_task

# ─── Paths ────────────────────────────────────────────────────────────────────

BENCHMARK_DIR = Path(__file__).parent
TASKS_FILE = BENCHMARK_DIR / "tasks.json"
PARTS_FILE = BENCHMARK_DIR.parent / "mar11-demo-attempt" / "parts_library.json"
RESULTS_DIR = BENCHMARK_DIR / "results"

# ─── System prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT_TEMPLATE = """You are a Lego Technic mechanical engineer. Your job is to design Lego Technic assemblies.

## Output Format

You MUST respond with a JSON object in this exact format:
```json
{{
  "reasoning": "Brief explanation of your design choices",
  "parts": [
    {{"id": "unique_id", "type": "part_type", "pos": [x, y, z], "axis": "x|y|z"}},
    ...
  ]
}}
```

Rules:
- Every part needs a unique "id" (e.g. "g1", "beam1", "axle_input")
- "type" must be exactly one of the part types listed below
- "pos" is [x, y, z] position in stud units (integers preferred)
- "axis" is the orientation: "x", "y", or "z" — the axis the part lies along
- For gears: "pos" is the center of the gear, "axis" is the rotation axis (axle direction)
- For beams: "pos" is one end, "axis" is the direction the beam extends
- For axles: "pos" is one end, "axis" is the direction the axle extends
- Gears mesh when their centers are exactly (radius1 + radius2) studs apart, and they share the same axis

## Parts Library

{parts_json}

## Key Mechanical Facts

- Gear ratio = driven_teeth / driving_teeth
- Two spur gears mesh when: distance between centers = radius1 + radius2 (in studs)
- Gear radii in studs: 8T=1, 16T=2, 24T=3, 40T=5, worm=1
- So: 8T+24T centers must be 1+3=4 studs apart for meshing
- Worm gear meshes with spur gears with PERPENDICULAR axes
- Rack-and-pinion: gear center must be exactly gear_radius studs from the rack centerline
- Compound gearing: mount a small gear and large gear on same axle to chain stages
"""

# ─── Model API calls ──────────────────────────────────────────────────────────


def call_model(model: str, system: str, messages: list, max_tokens: int = 4096) -> str:
    """Call the appropriate model API and return the text response."""
    if model.startswith("claude"):
        return call_anthropic(model, system, messages, max_tokens)
    elif model.startswith("gpt") or model.startswith("o3") or model.startswith("o4"):
        return call_openai(model, system, messages, max_tokens)
    elif model.startswith("gemini"):
        return call_gemini(model, system, messages, max_tokens)
    else:
        raise ValueError(f"Unknown model: {model}")


def call_anthropic(model, system, messages, max_tokens):
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    return response.content[0].text


def call_openai(model, system, messages, max_tokens):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    openai_messages = [{"role": "system", "content": system}] + messages
    kwargs = {"model": model, "messages": openai_messages}
    # o-series models use max_completion_tokens
    if model.startswith("o"):
        kwargs["max_completion_tokens"] = max_tokens * 4
    else:
        kwargs["max_tokens"] = max_tokens
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def call_gemini(model, system, messages, max_tokens):
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    gmodel = genai.GenerativeModel(model_name=model, system_instruction=system)
    # Flatten messages to a single string for simplicity
    prompt = "\n\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in messages
    )
    response = gmodel.generate_content(prompt)
    return response.text


# ─── JSON extraction ──────────────────────────────────────────────────────────


def extract_json(text: str) -> dict | None:
    """Extract JSON from model response (handles markdown code blocks)."""
    # Try to find ```json ... ``` block
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Try raw JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


# ─── Feedback message ─────────────────────────────────────────────────────────


def build_feedback(validation_errors, kinematics, score, checks, task):
    """Build a feedback message to send back to the model for revision."""
    lines = ["Your assembly has issues. Please fix them and provide a corrected JSON.\n"]

    if validation_errors:
        lines.append("**Validation errors:**")
        for e in validation_errors:
            lines.append(f"  - {e}")

    failed = [c for c in checks if not c["passed"]]
    if failed:
        lines.append("\n**Failed success criteria:**")
        for c in failed:
            lines.append(f"  - {c['name']}: {c['note']}")

    passed = [c for c in checks if c["passed"]]
    if passed:
        lines.append("\n**What's correct (keep these):**")
        for c in passed:
            lines.append(f"  ✓ {c['name']}: {c['note']}")

    if kinematics.get("gear_pairs"):
        lines.append(f"\n**Detected gear pairs:** {kinematics['gear_pairs']}")
    if kinematics.get("rack_pinion"):
        lines.append(f"**Detected rack-and-pinion:** {kinematics['rack_pinion']}")

    lines.append("\nRespond with the corrected JSON only.")
    return "\n".join(lines)


# ─── Run a single task ────────────────────────────────────────────────────────


def run_task(task: dict, model: str, parts_library: dict, rounds: int = 0, verbose: bool = True) -> dict:
    """Run a single task against a model. Returns result dict."""
    task_id = task["id"]
    if verbose:
        print(f"\n{'='*60}")
        print(f"Task {task_id}: {task['name']}")
        print(f"Model: {model}  |  Feedback rounds: {rounds}")
        print(f"{'='*60}")

    # Build system prompt with parts library
    parts_json = json.dumps(parts_library, indent=2)
    system = SYSTEM_PROMPT_TEMPLATE.format(parts_json=parts_json)

    # Initial user message
    user_prompt = task["prompt"]
    messages = [{"role": "user", "content": user_prompt}]

    result = {
        "task_id": task_id,
        "task_name": task["name"],
        "tier": task["tier"],
        "model": model,
        "rounds_used": 0,
        "score": 0,
        "checks": [],
        "turns": [],
        "final_assembly": None,
        "validation_errors": [],
        "kinematics": {},
        "timestamp": datetime.now().isoformat(),
    }

    for round_num in range(rounds + 1):  # round 0 = initial attempt
        if verbose:
            print(f"\n--- Round {round_num} ---")

        # Call model
        t0 = time.time()
        try:
            response_text = call_model(model, system, messages)
        except Exception as e:
            result["error"] = str(e)
            if verbose:
                print(f"  ERROR calling model: {e}")
            break
        elapsed = time.time() - t0

        if verbose:
            print(f"  Model responded in {elapsed:.1f}s")

        # Extract JSON
        assembly = extract_json(response_text)
        turn = {
            "round": round_num,
            "response": response_text[:2000],  # truncate for storage
            "assembly": assembly,
            "elapsed_s": round(elapsed, 2),
        }

        if assembly is None:
            if verbose:
                print("  ERROR: Could not extract JSON from response")
            turn["error"] = "no_json"
            result["turns"].append(turn)
            # Give model one more chance with explicit error
            if round_num < rounds:
                messages.append({"role": "assistant", "content": response_text})
                messages.append({"role": "user", "content":
                    "Your response did not contain valid JSON. Please respond with ONLY a JSON object in the specified format."})
            continue

        # Validate
        errors, warnings = validate_assembly(assembly, parts_library)
        kinematics = compute_kinematics(assembly, parts_library)
        score, checks = check_task(task, assembly, errors, kinematics, parts_library)

        turn["validation_errors"] = errors
        turn["validation_warnings"] = warnings
        turn["kinematics"] = kinematics
        turn["score"] = score
        turn["checks"] = checks
        result["turns"].append(turn)

        if verbose:
            print(f"  Validation: {len(errors)} errors, {len(warnings)} warnings")
            print(f"  Score: {score}/2")
            for c in checks:
                status = "✓" if c["passed"] else "✗"
                print(f"    {status} {c['name']}: {c['note']}")

        result["rounds_used"] = round_num
        result["score"] = score
        result["checks"] = checks
        result["final_assembly"] = assembly
        result["validation_errors"] = errors
        result["kinematics"] = kinematics

        # Full pass — stop
        if score == 2:
            if verbose:
                print(f"  PASSED on round {round_num}")
            break

        # Still have feedback rounds left
        if round_num < rounds:
            feedback = build_feedback(errors, kinematics, score, checks, task)
            if verbose:
                print(f"  Sending feedback for round {round_num + 1}")
            messages.append({"role": "assistant", "content": response_text})
            messages.append({"role": "user", "content": feedback})

    return result


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Lego Engineering Benchmark Runner")
    parser.add_argument("--task", help="Task ID (e.g. T2-01)")
    parser.add_argument("--tier", type=int, help="Run all tasks in a tier (1-5)")
    parser.add_argument("--all", action="store_true", help="Run all 20 tasks")
    parser.add_argument("--model", default="claude-sonnet-4-6", help="Model to use")
    parser.add_argument("--rounds", type=int, default=0, help="Feedback rounds (0=zero-shot)")
    parser.add_argument("--output", help="Output JSON file (default: results/run_<timestamp>.json)")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose output")
    args = parser.parse_args()

    # Load data
    with open(TASKS_FILE) as f:
        all_tasks = json.load(f)
    with open(PARTS_FILE) as f:
        parts_library = json.load(f)

    # Select tasks
    if args.task:
        tasks = [t for t in all_tasks if t["id"] == args.task]
        if not tasks:
            print(f"Task {args.task} not found. Available: {[t['id'] for t in all_tasks]}")
            sys.exit(1)
    elif args.tier:
        tasks = [t for t in all_tasks if t["tier"] == args.tier]
    elif args.all:
        tasks = all_tasks
    else:
        parser.print_help()
        sys.exit(1)

    print(f"Running {len(tasks)} task(s) with model={args.model}, rounds={args.rounds}")

    # Run
    results = []
    for task in tasks:
        result = run_task(task, args.model, parts_library, rounds=args.rounds, verbose=not args.quiet)
        results.append(result)

    # Summary
    total = len(results)
    full_pass = sum(1 for r in results if r["score"] == 2)
    partial = sum(1 for r in results if r["score"] == 1)
    fail = sum(1 for r in results if r["score"] == 0)

    print(f"\n{'='*60}")
    print(f"RESULTS: {full_pass}/{total} full pass | {partial} partial | {fail} fail")
    print(f"Score: {full_pass*2 + partial} / {total*2} ({(full_pass*2+partial)/(total*2)*100:.0f}%)")

    # Per-tier breakdown if running multiple tasks
    if total > 1:
        tiers = sorted(set(r["tier"] for r in results))
        for tier in tiers:
            tier_results = [r for r in results if r["tier"] == tier]
            tier_pass = sum(1 for r in tier_results if r["score"] == 2)
            print(f"  Tier {tier}: {tier_pass}/{len(tier_results)} pass  "
                  f"({', '.join(r['task_id'] + ':' + str(r['score']) for r in tier_results)})")

    # Save
    RESULTS_DIR.mkdir(exist_ok=True)
    if args.output:
        output_path = Path(args.output)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = RESULTS_DIR / f"run_{args.model.replace('/', '-')}_{ts}.json"

    output = {
        "model": args.model,
        "rounds": args.rounds,
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": total,
            "full_pass": full_pass,
            "partial": partial,
            "fail": fail,
            "score_pct": round((full_pass * 2 + partial) / (total * 2) * 100, 1),
        },
        "results": results,
    }
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
