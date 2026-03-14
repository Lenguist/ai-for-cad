# Model Notes: Gemini 2.5 Flash

**Type:** LLM Baseline (CadQuery Python via API)
**API:** Google Generative AI
**Eval run:** `eval/results/20260308_203415/`

---

## Score

| Tier | Score | Notes |
|------|-------|-------|
| T1 (Basic primitives) | 5/5 | Perfect |
| T2 (Multi-feature) | 4/5 | 1 bad variable name |
| T3 (Assemblies) | 4/5 | 1 hallucinated method |
| T4 (Complex geometry) | 1/5 | Multiple hallucinations |
| **Overall** | **70% (14/20)** | |
| Avg latency | 3.1s | Very fast — streaming response |

---

## Failures

### t2_03 — L-shaped bracket
**Error:** `No variable named 'result' found after exec()`
**Root cause:** Model assigned output to a different variable name (not `result`, `assembly`, or any of the fallback names in execute.py). Likely used `bracket` or similar but with a different capitalization or compound name.

### t3_05 — Rectangular plate with pocket
**Error:** `'Workplane' object has no attribute 'cutExtrude'`
**Root cause:** Hallucinated method. `cutExtrude()` is not a CadQuery method. The correct method is `.cut()` or `.cutBlind()`. Gemini appears to have confused CadQuery with another CAD API (possibly FreeCAD's Python scripting or SolidWorks API terminology).

### t4_01 — Spur gear
**Error:** `'Workplane' object has no attribute 'gear'`
**Root cause:** Hallucinated method. CadQuery has no `.gear()` method — gear generation requires manual involute curve math or a library like `cq-gears`. Gemini invented a convenience method that doesn't exist.

### t4_03 — 90-degree pipe elbow
**Error:** `No variable named 'result' found after exec()`
**Root cause:** Complex sweep geometry (pipe along curved path) — model may have assigned to a different variable name or produced incomplete code.

### t4_04 — Helical spring
**Error:** `No variable named 'result' found after exec()`
**Root cause:** Same as above — helix path sweeps require precise variable naming.

### t4_05 — Countersunk screw hole pattern
**Error:** `Workplane.rarray() got an unexpected keyword argument 'centered'`
**Root cause:** API version mismatch or hallucination. In some CadQuery versions, `rarray()` accepts `center=True`; in the version we're running it doesn't accept `centered`. Gemini used a parameter name that doesn't exist in our installed version.

---

## Observations

- Fast response time (3.1s avg) — streaming helps
- Fails hard on T4 due to hallucinated API methods (gear, cutExtrude)
- Variable naming inconsistency on complex prompts
- Does well on T1-T3 where the CadQuery API surface is straightforward
- The `centered` keyword on `rarray()` is a real CadQuery issue — different API versions accept different params; worth pinning our CadQuery version and updating the prompt to use canonical modern syntax
- Rate limit retry was necessary in `eval/models.py` (added exponential backoff)

---

## Next Steps

1. **Fix `rarray()` centered kwarg** — pin `cadquery==2.4.0` in executor environment and check which params are accepted; or strip `centered=` from generated code as a post-processing step
2. **Add CadQuery version to system prompt** — tell Gemini explicitly which version of CadQuery to use: `"Use CadQuery 2.4.0 API. Do not use .gear(), .cutExtrude(), or any method not in the official CadQuery 2.x docs."`
3. **Improve variable name fallback** — add more variable names to the fallback list in execute.py (e.g. `l_bracket`, `l_shape`, `elbow_pipe`)
4. **Re-run T4 with constrained system prompt** — prohibit inventing API methods; require `result = ...` assignment
5. **Test Gemini 2.5 Pro** — Pro variant may have better code reliability at the cost of speed
