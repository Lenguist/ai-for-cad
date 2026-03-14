# Model Notes: Text-to-CadQuery (Qwen 2.5 3B SFT)

**Type:** Academic (CadQuery Python, fine-tuned Qwen 2.5 3B)
**Weights:** `ricemonster/qwen2.5-3B-SFT` on HuggingFace
**Infrastructure:** Modal A10G GPU (16GB VRAM)
**Modal app:** `cad-arena-text2cadquery`
**Runner:** `eval/modal_text2cadquery.py`
**Eval run:** `eval/results/text2cadquery/qwen/`

---

## Score

| Tier | Score | Notes |
|------|-------|-------|
| T1 (Basic primitives) | 5/5 | Perfect |
| T2 (Multi-feature) | 3/5 | 1 empty code, 1 bad variable name |
| T3 (Assemblies) | 5/5 | Perfect |
| T4 (Complex geometry) | 1/5 | Variable naming + OCC crash |
| **Overall** | **70% (14/20)** | |
| Avg latency | ~7-18s on A10G | Model load: ~60s (cold start) |

---

## Failures

### t2_03 — L-shaped bracket
**Error:** No code / empty output
**Root cause:** Suspected early `<|endoftext|>` token — the model short-circuits on L-shaped geometry. May need a prompt adjustment.

### t2_04 — Square plate with 4 holes
**Error:** `No variable named 'result' found after exec()`
**Root cause:** Model uses non-standard output variable (training data used `part_1`, `plate`, etc.) — this specific output used a variable not in our fallback list.

### t4_02 — Hex bolt
**Error:** `No variable named 'result' found after exec()`
**Root cause:** Same — model output variable not in fallback list. Likely `bolt` with different casing or `hex_bolt`.

### t4_03 — 90-degree pipe elbow
**Error:** `GC_MakeArcOfCircle::Value() - no result`
**Root cause:** OpenCASCADE geometric construction error. The model attempts to create an arc for the elbow bend but the input geometry (radius/angle combination) is degenerate. Training data likely has normalized 0-1 unit geometry, so the 3D arc math breaks when applied to real mm dimensions.

### t4_04, t4_05 — Helical spring / Countersunk holes
**Error:** `No variable named 'result' found after exec()`
**Root cause:** Same variable naming issue on complex geometry.

---

## Known Limitations

### 1. Normalized units (0–1 scale) — PARTIALLY MITIGATED
The model was trained on DeepCAD dataset which uses normalized coordinates in [0, 1] space. It generates geometrically correct shapes but with wrong dimensions and inconsistent scales (e.g., a "20mm cube" becomes a 0.04×0.04×0.2 slab; a "50mm disk" is 0.005 units across).

**Post-processing applied (2026-03-09):** All 14 STL files in `public/eval/text2cadquery-qwen/` were rescaled so their longest bounding-box dimension = 50mm. This makes them visible in the 3D viewer. Scale factors ranged from 100× to 10000× — the model uses no consistent unit system.

**Remaining issues after post-processing:**
- `t1_02` (cylinder): zero-radius — model output a degenerate line mesh, renders as a vertical line
- `t2_02` (cylinder with hole): near-zero radius (0.2mm after scaling), same issue
- `t3_01`, `t3_02` (flanged cylinder, hollow box): very thin (1–4mm x/y span vs 50mm height) — needle-like appearance
- Internal proportions are wrong for most shapes (the "cube" renders as a 10×10×50 slab, not a cube)

**Impact:** Geometry passes execution but bounding box dimensions won't match the prompt. The 3D renders show the topology (holes, features) but not the correct shape. Functional pass rate overstates practical usefulness.

### 2. Non-standard variable names
Training data used diverse variable names (`assembly`, `part_1`, `plate`, `gear`, `bolt`). We added fallback resolution in execute.py but don't cover all cases.

### 3. Hardcoded export calls in generated code
Model sometimes emits `cq.exporters.export(result, './stlcq/filename.stl')` — this is a training artifact (training script injected export lines). We mock `cq.exporters.export` as a no-op in the executor to handle this.

### 4. Token truncation (pre-fix)
Original run used `max_new_tokens=512`. Three prompts were truncated. Fixed by bumping to `1024` in `eval/modal_text2cadquery.py`.

---

## Infrastructure Issues Found

### Issue: transformers 5.x vs torch 2.2 conflict
- **Problem:** `transformers>=4.45.0` resolved to 5.3.0 which requires `torch>=2.4`. Our Modal image had torch 2.2.
- **Fix:** Pinned `transformers>=4.45.0,<5.0.0` and `torch==2.4.1` in Modal image.

### Issue: Modal argparse conflict
- **Problem:** `modal run script.py --prompts "..."` fails because Modal CLI intercepts all `--` args.
- **Fix:** Used typed function parameters in `@app.local_entrypoint()` instead of `argparse`.

### Issue: Hardcoded export paths crash executor
- **Problem:** `cq.exporters.export(result, './stlcq/...')` — path doesn't exist in executor sandbox.
- **Fix:** Wrapped `cq.exporters` as a `types.SimpleNamespace` mock in execute.py.

---

## Observations

- Surprisingly competitive for a 3B model — 70% overall, same as Gemini 2.5 Flash
- Performance profile differs: Qwen fails on variable naming/OCC errors; Gemini fails on hallucinated API methods
- Model inference is fast once loaded (~7-18s/prompt) but cold start costs ~60s on Modal
- The Mistral-7B-lora variant has not been tested yet

---

## Next Steps

1. **Expand fallback variable name list** in execute.py — add `hex_bolt`, `part_3`, `spring_coil`, `countersunk_plate`, and any others seen in training artifacts
2. **Test Mistral-7B-lora** (`ricemonster/Mistral-7B-lora`) — same Modal app, `--model mistral` flag
3. **Add dimension scaling pass** — post-process generated code to rescale from normalized units to prompt dimensions (parse dimensions from prompt, compute scale factor)
4. **Re-run failures** with explicit variable name in system prompt: `"Assign your final result to a variable named 'result'."`
5. **Add bounding box validation** — compare generated shape BB against expected dimensions from prompt; flag mismatch as "dimensionally incorrect" vs "failed"
6. **Investigate t2_03 empty output** — may need more specific prompt formatting for L-shaped geometry
