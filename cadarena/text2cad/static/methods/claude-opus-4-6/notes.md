# Model Notes: Claude Opus 4.6

**Type:** LLM Baseline (CadQuery Python via API)
**API:** Anthropic
**Eval run:** `eval/results/20260308_203415/`

---

## Score

| Tier | Score | Notes |
|------|-------|-------|
| T1 (Basic primitives) | 5/5 | Perfect |
| T2 (Multi-feature) | 5/5 | Perfect |
| T3 (Assemblies) | 5/5 | Perfect |
| T4 (Complex geometry) | 4/5 | 1 OCC crash |
| **Overall** | **95% (19/20)** | |
| Avg latency | 6.9s | Range: 1.7s–31.0s |

---

## Failures

### t4_05 — Countersunk screw hole pattern
**Error:** `gp_Vec::Normalize() - vector has zero norm`
**Root cause:** OpenCASCADE geometry error when computing the normal vector for a countersunk (conical) feature. This happens when the chamfer/countersink geometry produces a degenerate edge — usually because the countersink angle combined with the plate thickness creates a zero-length vector somewhere in the BREP kernel.
**Code produced:** Yes (code was generated and syntactically valid)
**STL:** Not produced

---

## Observations

- Most reliable model overall — handles all tier structures confidently
- Long latency on complex T4 prompts (t4_01 took 31s, t4_04 took 22s) — likely large token output for helical spring / gear code
- Produces idiomatic CadQuery with `result =` variable as expected by executor
- Does not hallucinate CadQuery API methods (unlike Gemini)
- Code style: parametric, well-structured, uses `.workplane()` properly

---

## Next Steps

1. **Investigate t4_05 fix** — Try alternate approach for countersink: use `.cskHole()` instead of manual chamfer geometry, which is the idiomatic CadQuery way and avoids raw OCC math
2. **Re-test t4_05** with a corrected prompt or post-processing fixup
3. **Consider adding Claude Sonnet 4.6** as a cheaper/faster baseline — expected slightly lower accuracy but much lower cost and latency
4. **Track cost per run** — Claude Opus is ~$15/MTok input; log token counts in eval runner
