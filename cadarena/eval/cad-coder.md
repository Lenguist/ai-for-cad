# Model Notes: CAD-Coder (CADCODER/CAD-Coder)

**Type:** Academic (multimodal LLM → CadQuery Python, 13B)
**Weights:** `CADCODER/CAD-Coder` on HuggingFace (LLaVA-based, 13B)
**Infrastructure:** Modal A100 GPU (needed for 13B)
**Modal app:** Not yet written
**Runner:** Not yet written
**Status:** NOT YET STARTED

---

## Architecture

CAD-Coder is a 13B multimodal LLM (LLaVA architecture) fine-tuned to generate CadQuery Python code from text (and optionally image) inputs. Being LLaVA-based means it has:
- A vision encoder (CLIP ViT-L/14) for image inputs
- A 13B language model base (LLaMA-2-13B or similar)
- Instruction tuning on CAD descriptions

Output is **CadQuery Python** — drops directly into our existing execute.py validator.

---

## Infrastructure Requirements

- **GPU:** 13B model needs ~26GB VRAM — requires A100 (40GB) on Modal, not A10G (24GB)
- **Dual environment:** LLaVA requires specific versions of transformers + llava package that may conflict with standard HF setup
- **Loading:** Use `AutoModelForCausalLM.from_pretrained` with `load_in_4bit=True` (bitsandbytes 4-bit quantization) to fit in 24GB A10G, or use full precision on A100

---

## Known Risks (Pre-run)

### Risk 1: Dual environment complexity
- LLaVA models require `llava` package or a specific transformers version patched for LLaVA
- May need to install from source: `pip install git+https://github.com/haotian-liu/LLaVA`

### Risk 2: Vision input not needed
- Our benchmark is text-only; we don't have reference images
- CAD-Coder may have been trained primarily on (image, description) → code pairs
- Text-only performance may be lower than reported accuracy (which may include image conditioning)

### Risk 3: GPU cost
- A100 on Modal is ~$3/hour vs ~$1/hour for A10G
- 20-prompt benchmark ≈ 40-60min inference = ~$2-3 per run

---

## Decision: OUT OF SCOPE for text-only benchmark

**Verified 2026-03-14:** CAD-Coder is vision-first and cannot do text-only inference.

- The eval script (`llava.eval.model_vqa_loader`) unconditionally requires an image file per prompt
- The prompt is hardcoded as: `"Generate the CadQuery code needed to create the CAD for the provided image. Just the code, no other words."`
- There is no text-only inference path

CAD-Coder will be listed in the model catalog as "image-conditioned" and excluded from the text-to-CAD leaderboard. Could be revisited if we add an image-conditioned track (e.g. sketch → CAD).
