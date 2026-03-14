# Model Notes: Zoo ML-ephant

**Type:** Commercial (KittyCAD Language via Zoo API)
**API:** `https://api.zoo.dev/ai/text-to-cad/stl` (POST) + job polling
**Eval run:** `eval/results/20260309_zoo_kcl/` (re-run to capture KCL source)
**Original run:** `eval/results/20260308_zoo/`

---

## Score

| Tier | Score | Notes |
|------|-------|-------|
| T1 (Basic primitives) | 5/5 | Perfect |
| T2 (Multi-feature) | 5/5 | Perfect |
| T3 (Assemblies) | 5/5 | Perfect |
| T4 (Complex geometry) | 4/5 | 1 timeout |
| **Overall** | **95% (19/20)** | |
| Avg latency | ~5s (KCL re-run) | First run was ~11s — may vary with API load |

---

## Failures

### t4_04 — Helical compression spring
**Error:** `Timeout after 120s` (`job_id=f131e1bc-3dc3-4b77-8430-b0b8abb97a41`)
**Root cause:** Helix-based geometry (lofting along a helical path) is computationally expensive in KCL/Zoo's backend. The job was submitted successfully but never completed within the 120s timeout window.
**KCL produced:** Unknown (job never completed, no status with code field)
**STL:** Not produced

---

## Infrastructure Issues Found

### Issue 1: KCL source not captured initially
- **Problem:** First eval (`20260308_zoo/`) called `/ai/text-to-cad/stl` and discarded the `code` field in the job status response.
- **Fix:** Updated `eval/models.py` to read `status_data.get("code")` from the job polling loop. Re-ran as `eval/results/20260309_zoo_kcl/`.
- **Result:** 19/20 prompts now have KCL source code (t4_04 excluded due to timeout)

### Issue 2: Base64 decoding
- **Problem:** Early runs had issues decoding STL bytes from the API response.
- **Fix:** Applied in `eval/execute.py` → `validate_zoo_stl()` with explicit `base64.b64decode()`.

---

## Observations

- KCL is a functional, declarative language — very different from CadQuery's imperative Python
- Example KCL output for a cube:
  ```kcl
  @settings(defaultLengthUnit = mm)
  cube = startSketchOn(XY)
    |> rectangle(center = [0, 0], width = size, height = size)
    |> extrude(length = size)
  ```
- Zoo's internal model does not appear to struggle with basic/intermediate geometry
- The helical spring timeout may be a known hard case — even professional CAD tools struggle to parameterize helices efficiently

---

## Next Steps

1. **Retry t4_04 (helical spring)** — increase timeout to 300s and retry, or simplify the prompt (fewer coils)
2. **Display KCL with syntax highlighting** on the website — add `language-kcl` class and a simple highlighter
3. **Investigate Zoo API rate limits** — check if there's a per-minute cap causing the slower ~11s first-run latencies
4. **Try STEP export endpoint** — Zoo also returns STEP in the job response; STEP preserves B-rep topology (better for analysis than STL mesh)
5. **Add quality scoring** — Zoo produces metrically accurate geometry; worth verifying bounding box dimensions match the prompt spec
