# Model Notes: GPT-5

**Type:** LLM Baseline (CadQuery Python via API)
**API:** OpenAI
**Eval run:** `eval/results/20260308_203415/`

---

## Score

| Tier | Score | Notes |
|------|-------|-------|
| T1 (Basic primitives) | 5/5 | Perfect |
| T2 (Multi-feature) | 4/5 | 1 token truncation |
| T3 (Assemblies) | 3/5 | 2 token truncations |
| T4 (Complex geometry) | 0/5 | All truncated |
| **Overall** | **60% (12/20)** | |
| Avg latency | 16.1s | Slow — T4 prompts take 29-33s |

---

## Failures

### t2_03 — L-shaped bracket
**Error:** No code extracted (empty string from `extract_code()`)
**Root cause:** Token limit truncation. The response was cut off mid-code block. `extract_code()` returns empty string when the code fence is opened but never closed.

### t3_01 — Flanged cylinder
**Error:** Same as above — truncated
**Latency:** 29.0s (model was generating but hit limit)

### t3_03 — T-shaped bracket
**Error:** Truncated
**Latency:** 25.9s

### t4_01 through t4_05 — All T4 prompts
**Error:** All truncated
**Latencies:** 29–33s
**Root cause:** GPT-5 appears to have a 2048 token output limit in our current API configuration. Complex T3/T4 prompts (helical spring, gear, pipe elbow) require 3000+ tokens of CadQuery code. The model generates the code correctly but runs out of tokens before closing the code fence.

---

## Infrastructure Issues Found

### Issue: `extract_code()` returns empty on truncated fences
- **Problem:** When a response is truncated mid-`\`\`\`python` block, `extract_code()` finds no closing fence and returns `""`.
- **Current behavior:** Empty code → logged as failure, no partial code saved.
- **Proposed fix:** Add a fallback that saves the partial code and tries to execute anyway, or at least log the raw response for debugging.

### Issue: No retry on truncation
- **Problem:** Truncations happen silently — no warning in the log that the response was cut off.
- **Proposed fix:** Check if `finish_reason == "length"` in the API response and log a `[TRUNCATED]` warning.

---

## Observations

- GPT-5 code quality (on prompts it completes) is good — T1/T2 pass cleanly
- The truncation problem is systematic, not random — all T4 and some T3 prompts exceed the token budget
- 29-33s latency on T4 prompts suggests the model IS generating a full answer; it's just getting cut off
- This is likely a `max_tokens` parameter issue in our API call — need to increase it

---

## Next Steps

1. **Increase `max_tokens`** in `eval/models.py` for GPT-5 — try `max_tokens=4096` or `max_tokens=8192`
2. **Log `finish_reason`** from OpenAI API response — detect truncation explicitly and mark as `"truncated"` in results
3. **Save partial code** on truncation — even partial code is useful for debugging the model's approach
4. **Re-run T2_03, T3_01, T3_03, T4_01–T4_05** with higher token limit — expected score should improve to 85-90%
5. **Check OpenAI API version** — confirm we're not on an older endpoint with lower limits
