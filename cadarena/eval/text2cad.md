# Model Notes: Text2CAD (SadilKhan/Text2CAD)

**Type:** Academic (text-to-CAD sequence generation, NeurIPS 2024)
**Weights:** Unverified — `SadilKhan/Text2CAD` on HuggingFace (may be dataset-only)
**Infrastructure:** Modal (not yet tested)
**Modal app:** `cad-arena-text2cad`
**Runner:** `eval/modal_text2cad.py`
**Status:** Scaffold written — HF slug UNVERIFIED — NOT YET RUN

---

## Architecture

Text2CAD (NeurIPS 2024) generates CAD construction sequences conditioned on natural language. Unlike FlexCAD, it was explicitly trained with text descriptions.

Pipeline:
```
Text → T5/CLIP encoder → Transformer decoder → CAD sequence (sketch + extrude commands)
                                              → Open-STEP or STL via pythonocc
```

---

## Known Issues (Pre-run)

### Issue 1: HuggingFace slug unverified
- We used `SadilKhan/Text2CAD` as the assumed slug
- This may be a **dataset repo** (with dataset cards) rather than model weights
- The paper authors may not have released inference weights publicly
- **Must verify:** Check HF repo contents before attempting to load

### Issue 2: Unknown model API
- The exact HF model class (AutoModelForCausalLM, T5ForConditionalGeneration, custom?) is unknown
- Need to read the model card and repo to determine correct loading code

### Issue 3: Output format to STL
- Text2CAD likely outputs a sketch-based CAD sequence, not CadQuery Python
- Need a custom decoder to convert sequences → geometry
- May require the authors' inference script from the GitHub repo

---

## Research Needed

1. **Verify HF repo:** Check `SadilKhan/Text2CAD` — is it model weights or just the dataset?
2. **Find GitHub repo:** Paper authors usually release code at `github.com/SadilKhan/Text2CAD` or similar
3. **Determine inference API:** How to load model, how to run inference, what output format
4. **Check compute requirements:** Paper reports model size and GPU requirements

---

## Next Steps

1. **Verify HF slug** — `from huggingface_hub import list_repo_files; list_repo_files("SadilKhan/Text2CAD")`
2. **Find official code repo** — look for Dockerfile, inference.py, or demo script
3. **Rewrite modal_text2cad.py** once inference API is confirmed
4. **Run quick test** on 1-2 prompts
5. If weights are not released: **contact authors** or check for a Colab demo that reveals the API
