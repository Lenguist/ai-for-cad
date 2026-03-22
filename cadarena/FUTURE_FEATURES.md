# Future Features

Features deliberately deferred — not prioritized until the core arena is live and has traffic.

---

## /explore — Community Prompt Browser

**What:** Grid of user-submitted prompts (consent=true only). Filter by tier/model/success. Click any prompt to see results same as static detail view.

**Why deferred:** Network effects feature — useless at launch, valuable once /try has 50+ user submissions. Building it requires the full Supabase stack (auth + DB + storage) which blocks shipping the core demo.

**When to build:** Once /try is live and generating real traffic.

**Dependencies to build first:**
- Supabase project (auth + postgres + storage)
- Schema: results table, quota table
- Storage bucket for STL files
- Consent UI in /try ("Save this prompt to the public dataset?")
- /api/generate updated to save to Supabase on consent

---

## Auth + Rate Limiting (full)

**What:** Email + Google sign-in via Supabase Auth. Free accounts get 20 prompts/day vs 3/day anonymous.

**Why deferred:** Upstash Redis IP-based rate limiting covers abuse prevention at launch without needing accounts.

**When to build:** When there's a reason for users to have accounts (saved history, /explore submissions).

---

## Geometric Accuracy Metrics

**What:** Beyond valid STL — score whether the output actually matches the prompt. Chamfer distance, VLM scoring, dimension extraction.

**Why deferred:** Hard problem, needs a VLM judge or manual review pipeline. Validity rate is honest and sufficient for v1.
