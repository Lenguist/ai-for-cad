# Model Notes: FlexCAD (microsoft/FlexCAD)

**Type:** Academic (CAD sequence generation, ICLR 2025)
**Weights:** `microsoft/FlexCAD` on HuggingFace (8B LoRA on Llama-3)
**Infrastructure:** Modal A10G GPU (24GB VRAM)
**Modal app:** `cad-arena-flexcad`
**Runner:** `eval/modal_flexcad.py`
**Status:** Runner written — NOT YET RUN

---

## Architecture

FlexCAD is an 8B LoRA fine-tune on Meta-Llama-3-8B that generates **CAD construction sequences** (quantized B-rep feature commands), not Python code. Output is reconstructed to geometry via:

```
Text prompt → sample.py (Llama-3 + LoRA) → JSONL sequences
                                          → parser.py → OBJ mesh
                                          → visual_obj.py (pythonocc) → STL
```

**Key caveat:** FlexCAD was trained on the DeepCAD dataset (geometric sequences, not natural language). Text conditioning via `mask_type=unconditional` generates shapes unconditioned on the prompt. The model was not trained on text-to-CAD; it was trained on CAD sequence completion. Text prompts in our benchmark will be stored for reference but the model won't actually follow them.

---

## Known Issues (Pre-run)

### Issue 1: No text conditioning
- FlexCAD does not have a natural language encoder
- `mask_type=unconditional` generates random valid CAD sequences
- The generated geometry will be structurally valid but unrelated to the prompt
- **Impact:** Pass rate measures "valid geometry generation" not "prompt adherence"

### Issue 2: OCC dependency on Modal
- `pythonocc-core==7.7.2` is a complex build with OCCT system libraries
- Modal image includes apt packages (`libocct-*-dev`) — may have version mismatches
- Fallback: if pythonocc fails, parser.py can write OBJ; we can use trimesh to convert OBJ→STL

### Issue 3: argparse conflict with Modal CLI
- `modal_flexcad.py` currently uses argparse in `@app.local_entrypoint()` — **this will fail**
- Modal CLI intercepts `--` args before passing to the script
- **Must fix:** Convert to typed function parameters (same fix as modal_text2cadquery.py)
  ```python
  @app.local_entrypoint()
  def main(prompt: str = "", out: str = "results/flexcad"):
  ```

### Issue 4: Base model gating
- `meta-llama/Meta-Llama-3-8B` requires HuggingFace access token and Meta license acceptance
- Need `HF_TOKEN` secret set in Modal workspace
- `microsoft/FlexCAD` (the LoRA) is public but requires the base model

---

## Next Steps

1. **Fix argparse → typed params** in `modal_flexcad.py` local_entrypoint
2. **Add HF_TOKEN secret** to Modal: `modal secret create huggingface HF_TOKEN=<your_token>`
3. **Test image build**: `modal run eval/modal_flexcad.py --prompt "A cube 20mm"` — verify pythonocc installs
4. **Run quick test** with 1-2 prompts to verify the full pipeline (sample → parse → STL)
5. **Run full benchmark** — expect ~50-70% valid geometry (model generates valid DeepCAD sequences); dimension accuracy will be poor
6. **Add output label** in results.json: `"note": "unconditional — geometry valid but not conditioned on prompt"`
7. **Consider text-conditioned variant** — FlexCAD paper mentions a text-conditioned mode using CLIP/T5 encoder; check if the released weights include this
