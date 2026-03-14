# CAD Arena — Next Steps
*Written: 2026-03-03, end of session*

---

## Where We Are

Pipeline is validated. We ran 20 prompts through 4 API models, got STL outputs,
committed results. Website is live on Vercel with a preliminary results table.

**What works:**
- eval/run.py — full benchmark pipeline end-to-end
- GPT-5, Claude Opus 4.6, Zoo ML-ephant all working
- CadQuery execution + STL export locally
- Landing page on Vercel with results table

**What's broken/incomplete:**
- Gemini hits rate limits (free tier quota) — need retry logic or paid key
- Self-hosted academic models not yet run (need cloud GPU)
- No Chamfer Distance metric yet (need ground truth STEP files)
- Website has no actual leaderboard page (just landing)

---

## Immediate Next Steps (do these first)

### 1. Fix Gemini rate limiting
File: `eval/models.py` → `GeminiModel.generate()`
Add exponential backoff retry on 429 errors:
```python
import time
for attempt in range(4):
    try:
        response = self.client.models.generate_content(...)
        break
    except Exception as e:
        if "429" in str(e) and attempt < 3:
            time.sleep(2 ** attempt * 5)  # 5s, 10s, 20s
        else:
            raise
```
Then re-run: `python run.py --models gemini-2.5-flash`

### 2. Get per-tier breakdown in analyze.py
Currently analyze.py shows per-model totals. Add per-tier rows so we can see
"Tier 1: Claude 5/5, GPT-5 5/5" etc.
File: `eval/analyze.py` — add `--breakdown` flag that groups by tier.

### 3. Register cadarena.dev domain
- Buy on Porkbun (~$10.98/yr): https://porkbun.com
- Point nameservers to Cloudflare (free account)
- Add domain to Vercel project (Settings → Domains)
- Set up Cloudflare Email Routing: contact@cadarena.dev → your Gmail (free)
- Update hardcoded `contact@cadarena.ai` in app/page.tsx to `contact@cadarena.dev`

---

## Phase 2: Self-Hosted Academic Models (needs cloud GPU)

### Models to run (weights are public, ranked by easiest first):

**1. Text-to-CadQuery (Qwen2.5-3B) — EASIEST**
- Weights: `ricemonster/*` on HuggingFace
- VRAM: ~8GB → fits on RTX 3090 or A10G
- Output: CadQuery Python (same pipeline as LLM models, no changes needed)
- Estimated cost: ~$1-2 on Lambda Labs for 20 prompts

**2. CAD-Recode (~1.5B) — point cloud input, different track**
- Weights: `filapro/cad-recode-v1.5` on HuggingFace
- VRAM: ~6-8GB
- Note: takes point cloud not text — needs different prompts
- Has a live HuggingFace ZeroGPU Space if you want to test manually first

**3. Text2CAD (363M) — most cited academic model**
- Weights: `SadilKhan/Text2CAD` on HuggingFace
- VRAM: 8-16GB
- Run: `python test_user_input.py --prompt "..."`
- GitHub: https://github.com/SadilKhan/Text2CAD

**4. FlexCAD (8B LLaMA-3) — Microsoft**
- Weights: `microsoft/FlexCAD` on HuggingFace
- VRAM: 16-24GB → needs A100 or 2×A6000
- License: research-only
- GitHub: https://github.com/microsoft/FlexCAD

**5. CADFusion (8B LLaMA-3) — Microsoft**
- Weights: `microsoft/CADFusion` on HuggingFace
- VRAM: 16-24GB
- GitHub: https://github.com/microsoft/CADFusion

### Cloud GPU options (cheapest first):
- **Lambda Labs**: A10G (24GB) $0.60/hr, A100-80GB $1.29/hr
- **RunPod**: similar pricing, good spot instances
- **HuggingFace ZeroGPU**: free for models with a Space (CAD-Recode has one)

### Setup script needed:
Create `eval/run_selfhosted.py` that:
1. Loads model locally (HuggingFace)
2. Runs same 20 prompts
3. Saves to same results.jsonl format
4. Uses same execute.py for CadQuery validation

---

## Phase 3: Ground Truth + Chamfer Distance

Currently we only measure "did it produce valid geometry" (binary).
To publish a real benchmark paper we need Chamfer Distance against ground truth.

### What's needed:
1. Create ground truth STEP files for all 20 prompts
   - Option A: manually model them in FreeCAD/OnShape (accurate but slow)
   - Option B: use Claude/GPT-5 to generate CadQuery, review + fix manually
   - Option C: hire a CAD engineer on Upwork for ~$50-100 for 20 parts

2. Add `metrics.py` that:
   - Loads ground truth STL
   - Loads model-generated STL
   - Computes Chamfer Distance using `point_cloud_utils` or `open3d`
   - Returns CD score per prompt

3. Add CD column to results table and website

---

## Phase 4: Website — Leaderboard Page

Currently we have one page (landing). Need:

### New page: app/leaderboard/page.tsx
- Full results table with all models
- Filter by: tier, input type, output format
- Sort by: STL%, Chamfer Distance, latency
- Each model card links to paper/GitHub
- Updated automatically from results JSON

### New page: app/arena/page.tsx (stretch goal)
- Text input → send to all models simultaneously
- Show outputs side by side in 3D viewer
- Three.js viewer: convert STL to buffer, render with OrbitControls
- Vote buttons → store in Upstash Redis (same as the no-russia project)
- Elo scoring

---

## Phase 5: Paper

Target: NeurIPS 2026 Datasets & Benchmarks Track
Deadline: ~June 2026 (check exact date at neurips.cc)

### Paper outline:
1. Introduction — the gap (no unified benchmark)
2. Related work — Text2CAD, 3D Arena, SWE-bench as analogues
3. Benchmark design — 200 prompts, 4 tiers, selection methodology
4. Metrics — validity rate, Chamfer Distance, VLM judge score
5. Experimental results — all models on fixed set (big table)
6. Arena system — description of pairwise voting platform
7. Analysis — per-tier failure modes, which models struggle where
8. Conclusion + call for submissions

### To start the paper:
- Use the report.md in feb8/ as background section source
- Use benchmark/04-preliminary-results.md as preliminary results
- LaTeX template: NeurIPS 2026 official template

---

## How to Resume This Work (for Claude)

When you start a new session, say:
> "I'm continuing work on CAD Arena, the AI-for-CAD benchmark.
>  Read NEXT-STEPS.md and mar3-chat.txt in the repo root, and
>  benchmark/04-preliminary-results.md for context on where we are."

Claude will have memory from this session stored in:
~/.claude/projects/-Users-mbondarenko-Desktop-ai-for-cad/memory/MEMORY.md

The repo is: https://github.com/Lenguist/ai-for-cad

---

## File Map (key files to know)

```
ai-for-cad/
├── app/page.tsx                     ← landing page (Next.js)
├── eval/
│   ├── .env                         ← API keys (gitignored)
│   ├── prompts.py                   ← 20 benchmark prompts
│   ├── models.py                    ← GPT-5, Claude, Gemini, Zoo clients
│   ├── execute.py                   ← CadQuery subprocess execution
│   ├── run.py                       ← main runner
│   ├── analyze.py                   ← print results table
│   └── results/20260303_210402/     ← first run results
│       ├── summary.json             ← per-model aggregate stats
│       └── results.jsonl            ← per-(model,prompt) raw results
├── benchmark/
│   ├── 01-landscape-research.md    ← what exists in the field
│   ├── 02-benchmark-strategy.md    ← full build plan
│   ├── 03-models-compute.md        ← model weights + VRAM guide
│   └── 04-preliminary-results.md   ← first run analysis
├── feb8/
│   ├── papers-database.md          ← 173 papers cataloged
│   ├── report.md                   ← deep field analysis
│   └── companies.md                ← 60 companies
├── mar3-chat.txt                   ← today's session log
└── NEXT-STEPS.md                   ← this file
```
