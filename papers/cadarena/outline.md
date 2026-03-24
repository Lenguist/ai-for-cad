# CAD Arena: A Living Benchmark for Text-to-CAD Generation

## Status: outline / pre-draft
## Target: workshop paper (~4-6 pages)

---

## Core Argument

Existing text-to-CAD benchmarks are static, closed, and disconnected from real user intent.
CAD Arena is a *living* benchmark: prompts come from real users, outputs are compared side-by-side,
and the leaderboard updates continuously. This surfaces what people actually want to build,
not what researchers assumed they want.

---

## Novelty / Contribution Checklist

- [ ] First live, user-driven benchmark for text-to-CAD
- [ ] Side-by-side comparison of academic models (CadQuery-based) vs. commercial (Zoo ML-ephant)
- [ ] Dataset of real user CAD prompts (collected from cadarena.dev)
- [ ] Human preference votes as evaluation signal (not just geometric metrics)
- [ ] Open platform — others can submit models

---

## Outline

### 1. Introduction (~0.5 pages)
- CAD generation is increasingly important (engineering automation, co-pilots, etc.)
- Existing benchmarks: static prompt sets, closed evaluation, researcher-designed prompts
- Gap: no benchmark reflects real user intent or allows continuous model comparison
- We introduce CAD Arena: live, user-driven, preference-based

### 2. Related Work (~0.5 pages)
- Text2CAD (NeurIPS 2024) — closest academic benchmark, static
- ShapeNet/ABC dataset-based evals — geometry-focused, not text-driven
- LLM coding benchmarks (HumanEval, etc.) — inspiration for living benchmarks
- Commercial tools (Zoo, AdamCAD) — never benchmarked against academic models

### 3. The CAD Arena Platform (~1 page)
- Architecture: user submits prompt → 4 models run in parallel → STL rendered → user votes
- Models currently supported: Claude Sonnet 4.6, GPT-5, Gemini 2.5 Flash, Zoo ML-ephant
- Two output formats: CadQuery Python (LLMs) and KCL (Zoo), both rendered to STL via Modal
- Rate limiting, email collection, vote tracking (Upstash Redis)
- Open API for model submission

### 4. Benchmark Design (~0.5 pages)
- Prompt taxonomy: what kinds of parts do users actually ask for?
  (initial analysis from collected prompts)
- Evaluation: geometric validity (does it render?), human preference votes, latency
- Limitations of geometric metrics alone — argument for preference-based eval

### 5. Results (~1 page)
- Static benchmark: 4 models × 20 prompts
  - Claude Sonnet: ~95%, Zoo: ~95%, Gemini: ~70%, GPT-5: ~60%
- Live results: [to be filled as platform accumulates data]
- Win rate by model from user votes
- Prompt complexity vs. success rate

### 6. Discussion (~0.5 pages)
- What the prompt distribution reveals about user intent
- Where all models fail (complex geometry, mechanisms, assemblies)
- Argument: geometric accuracy metrics are insufficient — need functional + preference eval
- Roadmap: more models, geometric metrics, open submissions

### 7. Conclusion
- CAD Arena fills a real gap
- Living benchmark as a model for other engineering domains
- Platform open at cadarena.dev

---

## What's Missing Before Submission

- [ ] Enough accumulated user prompts to say something interesting about distribution
- [ ] Win rate data from votes (need platform live + some traffic)
- [ ] Related work section written out
- [ ] At least one figure: architecture diagram or example outputs grid
- [ ] Someone to co-author / sanity check (ideally a faculty collaborator)

---

## Possible Submission Targets

See `../venues.md` for full analysis.

**Best fit (workshop papers):**
- NeurIPS 2026 workshops: ML4Engineering, AI4Science, or dataset/benchmark track
- ICLR 2027 workshop on ML for physical sciences
- ICML 2026 workshop track
- CAD-specific: Computer-Aided Design journal (longer, more formal)
- arXiv first — get it out, then shop to workshops

**Stretch (full papers):**
- EMNLP / ACL (if framed as structured generation evaluation)
- NeurIPS Datasets & Benchmarks track (competitive but this fits the format)

---

## Timeline (rough)

- Platform live + collecting data: NOW (pending deploy)
- Enough data for analysis: ~1 month post-launch
- Draft: ~6 weeks post-launch
- arXiv submission: ~2 months post-launch
- Workshop submission: depends on deadlines
