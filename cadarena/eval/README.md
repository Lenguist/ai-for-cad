# Model Notes

Per-model investigation files documenting eval results, issues, and next steps.

## Evaluated (in results.json)

| Model | Status | Score | Notes file |
|-------|--------|-------|-----------|
| Claude Opus 4.6 | ✓ Evaluated | 95% (19/20) | [claude-opus-4-6.md](claude-opus-4-6.md) |
| Zoo ML-ephant | ✓ Evaluated | 95% (19/20) | [zoo-ml-ephant.md](zoo-ml-ephant.md) |
| Gemini 2.5 Flash | ✓ Evaluated | 70% (14/20) | [gemini-2.5-flash.md](gemini-2.5-flash.md) |
| GPT-5 | ✓ Evaluated | 60% (12/20) | [gpt-5.md](gpt-5.md) |
| Text2CadQuery (Qwen 3B) | ✓ Evaluated | 70% (14/20) | [text2cadquery-qwen.md](text2cadquery-qwen.md) |

## Pending

| Model | Status | Notes file |
|-------|--------|-----------|
| FlexCAD (microsoft) | Runner written, not run | [flexcad.md](flexcad.md) |
| Text2CAD (SadilKhan) | Scaffold written, HF slug unverified | [text2cad.md](text2cad.md) |
| CAD-Coder (13B) | Not started | [cad-coder.md](cad-coder.md) |

## Immediate Action Items

1. **GPT-5**: Increase `max_tokens` to 4096+ in `eval/models.py` → re-run T2_03, T3_01, T3_03, T4_all (expected: +8 passes)
2. **FlexCAD**: Fix argparse conflict in `modal_flexcad.py`, add HF_TOKEN secret, test build
3. **Text2CadQuery Qwen**: Re-run with explicit `"Assign result to variable named 'result'"` in system prompt
4. **Text2CAD**: Verify HuggingFace slug before building Modal runner
5. **CAD-Coder**: Write Modal runner (needs A100 or 4-bit quantized A10G)
