"""
Modal runner for Text-to-CadQuery models.

Runs ricemonster/qwen2.5-3B-SFT (default) or ricemonster/Mistral-7B-lora on
our 20-prompt benchmark. Output is CadQuery Python — drops straight into the
existing execute.py validator.

Usage:
    modal run modal_text2cadquery.py                          # full benchmark
    modal run modal_text2cadquery.py --prompts "A cube 20mm"  # quick test
    modal run modal_text2cadquery.py --model mistral-7b       # use 7B model
    modal run modal_text2cadquery.py --out results/text2cadquery/
"""

import json
import time
from pathlib import Path

import modal

# ── Images ────────────────────────────────────────────────────────────────────

BASE_IMAGE = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.4.1",
        "transformers>=4.45.0,<5.0.0",
        "peft>=0.10.0",
        "accelerate>=0.28.0",
        "bitsandbytes>=0.43.0",
        "huggingface_hub>=0.22.0",
        "sentencepiece",
        "protobuf",
    )
)

app = modal.App("cad-arena-text2cadquery")

# ── Qwen2.5-3B (SFT fine-tune, no LoRA) ──────────────────────────────────────

@app.function(
    image=BASE_IMAGE,
    gpu="A10G",
    timeout=600,
    memory=16384,
)
def run_qwen(prompts: list[str]) -> list[dict]:
    """Run ricemonster/qwen2.5-3B-SFT on a list of prompts."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    MODEL_ID = "ricemonster/qwen2.5-3B-SFT"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[Text2CadQuery/Qwen] Loading {MODEL_ID} on {device}")
    t0 = time.time()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()
    print(f"[Text2CadQuery/Qwen] Loaded in {time.time()-t0:.1f}s")

    results = []
    for prompt in prompts:
        t1 = time.time()
        row = {"prompt": prompt, "model": "ricemonster/qwen2.5-3B-SFT",
               "code": None, "error": None, "latency_s": 0.0}
        try:
            # Qwen SFT models use a chat template
            messages = [
                {"role": "system", "content": "Generate CadQuery Python code for the following CAD design description. Output only the Python code, no explanation."},
                {"role": "user", "content": prompt},
            ]
            text = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = tokenizer(text, return_tensors="pt").to(device)

            with torch.no_grad():
                output_ids = model.generate(
                    **inputs,
                    max_new_tokens=1024,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id,
                )
            # Decode only the newly generated tokens
            new_ids = output_ids[0][inputs["input_ids"].shape[1]:]
            raw = tokenizer.decode(new_ids, skip_special_tokens=True).strip()

            # Strip markdown fences if present
            import re
            m = re.search(r"```python\s*\n(.*?)```", raw, re.DOTALL)
            if m:
                raw = m.group(1).strip()
            else:
                m = re.search(r"```\s*\n(.*?)```", raw, re.DOTALL)
                if m:
                    raw = m.group(1).strip()

            row["code"] = raw
            print(f"[Text2CadQuery/Qwen] ✓ {prompt[:60]!r}  ({time.time()-t1:.1f}s)")
        except Exception as e:
            import traceback
            row["error"] = f"{e}\n{traceback.format_exc()}"
            print(f"[Text2CadQuery/Qwen] ✗ {prompt[:60]!r}  {e}")

        row["latency_s"] = round(time.time() - t1, 2)
        results.append(row)

    return results


# ── Mistral-7B LoRA ───────────────────────────────────────────────────────────

@app.function(
    image=BASE_IMAGE,
    gpu="A10G",
    timeout=600,
    memory=24576,
)
def run_mistral(prompts: list[str]) -> list[dict]:
    """Run ricemonster/Mistral-7B-lora (LoRA on Mistral-7B-Instruct-v0.3)."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    BASE_ID = "mistralai/Mistral-7B-Instruct-v0.3"
    LORA_ID = "ricemonster/Mistral-7B-lora"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[Text2CadQuery/Mistral] Loading {BASE_ID} + LoRA {LORA_ID}")
    t0 = time.time()

    tokenizer = AutoTokenizer.from_pretrained(BASE_ID)
    base = AutoModelForCausalLM.from_pretrained(
        BASE_ID,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        load_in_4bit=True,
    )
    model = PeftModel.from_pretrained(base, LORA_ID)
    model.eval()
    print(f"[Text2CadQuery/Mistral] Loaded in {time.time()-t0:.1f}s")

    results = []
    for prompt in prompts:
        t1 = time.time()
        row = {"prompt": prompt, "model": "ricemonster/Mistral-7B-lora",
               "code": None, "error": None, "latency_s": 0.0}
        try:
            messages = [
                {"role": "user", "content": f"Generate CadQuery Python code for: {prompt}\nOutput only Python code."},
            ]
            text = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = tokenizer(text, return_tensors="pt").to(device)

            with torch.no_grad():
                output_ids = model.generate(
                    **inputs,
                    max_new_tokens=512,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id,
                )
            new_ids = output_ids[0][inputs["input_ids"].shape[1]:]
            raw = tokenizer.decode(new_ids, skip_special_tokens=True).strip()

            import re
            m = re.search(r"```python\s*\n(.*?)```", raw, re.DOTALL)
            if m:
                raw = m.group(1).strip()
            else:
                m = re.search(r"```\s*\n(.*?)```", raw, re.DOTALL)
                if m:
                    raw = m.group(1).strip()

            row["code"] = raw
            print(f"[Text2CadQuery/Mistral] ✓ {prompt[:60]!r}  ({time.time()-t1:.1f}s)")
        except Exception as e:
            import traceback
            row["error"] = f"{e}\n{traceback.format_exc()}"
            print(f"[Text2CadQuery/Mistral] ✗ {prompt[:60]!r}  {e}")

        row["latency_s"] = round(time.time() - t1, 2)
        results.append(row)

    return results


# ── Local entrypoint ──────────────────────────────────────────────────────────

@app.local_entrypoint()
def main(
    prompt: str = "",
    model: str = "qwen",
    out: str = "results/text2cadquery",
):
    """
    Args:
        prompt: single prompt to test (empty = run full benchmark)
        model: qwen or mistral
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

    print(f"\nSubmitting {len(prompts)} prompt(s) → Modal ({model}) ...")
    t0 = time.time()

    fn = run_qwen if model == "qwen" else run_mistral
    results = fn.remote(prompts)

    out_dir = Path(out) / model
    out_dir.mkdir(parents=True, exist_ok=True)

    n_ok = 0
    for r in results:
        slug = r["prompt"][:40].replace(" ", "_").replace("/", "-")
        if r["code"]:
            (out_dir / f"{slug}.py").write_text(r["code"])
            n_ok += 1
        print(f"  {'✓' if r['code'] else '✗'}  {r['prompt'][:60]!r}  ({r['latency_s']}s)")

    with open(out_dir / "results.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps({k: v for k, v in r.items() if k != "code"}) + "\n")

    print(f"\nDone: {n_ok}/{len(results)} generated in {time.time()-t0:.1f}s")
    print(f"Output: {out_dir}/")
