# AI for CAD Benchmark: Strategy & Design
*Generated: 2026-03-03*

## 1. The Opportunity (Confirmed Gap)

The survey paper "LLMs for CAD" (2025) explicitly calls this out:
> "The field lacks comprehensive evaluation frameworks and limited standardization."

**No one has built this.** The closest analogue is:
- **3D Arena** (mesh generation, not parametric CAD)
- **Text2CAD** (academic benchmark, no live leaderboard, no commercial tools, no public submissions)

There is a direct opportunity for a paper + living website that:
1. Defines a standardized prompt set for text-to-CAD
2. Evaluates ALL existing models (academic + commercial) on the same prompts
3. Hosts an ongoing arena for model comparison with community participation

---

## 2. What the Website Should Be

### 2.1 Core Product: Text-to-CAD Arena

Inspired by **Chatbot Arena** (LMSYS) and **3D Arena** (dylanebert):

```
User enters: "A bracket with two M6 holes 30mm apart, 5mm thick, L-shaped"

Side by side comparison:
[ Text2CAD ]  [ Zoo ML-ephant ]  [ CAD-Coder ]  [ AdamCAD ]  [ GPT-4o ]
[  3D view  ]  [   3D view    ]  [  3D view  ]  [  3D view ]  [ 3D view]

Which result is best? [Vote] [Download STEP] [See code]
```

### 2.2 Leaderboard Page
- Elo scores from community votes
- Quantitative metrics on fixed benchmark set
- Filter by: model type, input modality, output format, year
- Link to paper for each model

### 2.3 Benchmark Page (Fixed Evaluation Set)
- Fixed set of ~200 prompts graded by difficulty (simple → complex)
- Any model can be submitted for evaluation
- Metrics computed automatically
- Persistent leaderboard with paper links

### 2.4 Blog / Publication Page
- Host the companion paper
- Blog posts on field updates
- Monthly leaderboard snapshots

---

## 3. Models to Include (Launch Set)

### Academic Models (Open-Source or Reproducible)

| Model | Year | Venue | Input | Output | Key Metric |
|-------|------|-------|-------|--------|-----------|
| DeepCAD | 2021 | ICCV | Unconditional | CAD sequences | Baseline |
| Text2CAD | 2024 | NeurIPS Spotlight | Text | CAD sequences | CD=0.370 |
| FlexCAD | 2025 | ICLR | Text/multi-cond | CAD sequences | Best ICLR 2025 |
| Text-to-CadQuery | 2025 | arXiv | Text | CadQuery Python | CD=0.191 |
| CAD-Coder | 2025 | arXiv | Text | CAD code | 91% vs SFT |
| CADFusion | 2025 | arXiv | Text+visual | CadQuery | LVM 8.96/10 |
| CAD-GPT | 2025 | arXiv | Text+image | CAD sequences | Latest |
| CAD-Recode | 2025 | ICCV | Point cloud | CadQuery | Best scan-to-CAD |
| GPT-4o (zero-shot) | 2024 | - | Text | OpenSCAD/SCAD | Baseline: 93% invalid |

### Commercial APIs (via API calls)

| Tool | API | Cost | Output |
|------|-----|------|--------|
| Zoo / KittyCAD | zoo.dev/machine-learning-api | $0.50/min | STEP, STL, OBJ |
| AdamCAD | adamcad.ai | TBD | STEP |
| CADGPT | cadgpt.ai | TBD | STEP |
| Tripo3D | tripo3d.ai/api | $0.02/gen | GLB mesh |

### LLM Baselines (Prompt Engineering)
- GPT-4o → OpenSCAD
- GPT-4o → CadQuery
- Claude Sonnet → CadQuery
- Gemini 2.0 → CadQuery

---

## 4. The Prompt Set (Benchmark Design)

### Difficulty Tiers

**Tier 1 — Simple Primitives** (expected success: 90%+)
- "A cube 20mm × 20mm × 20mm"
- "A cylinder 10mm diameter, 30mm tall"
- "A sphere of radius 15mm"

**Tier 2 — Single-Part with Features** (expected success: 60-80%)
- "A rectangular plate 50×30×5mm with a centered hole 8mm diameter"
- "An L-shaped bracket, 40mm wide arms, 5mm thick, 30mm tall"
- "A hex bolt head 10mm across flats, M6 thread, 20mm shaft"

**Tier 3 — Multi-Feature Parts** (expected success: 30-50%)
- "A flanged shaft with 3 equally-spaced M4 bolt holes on the flange"
- "A box with a lid that snaps on, 50×40×30mm"
- "A gear: 20 teeth, module 2, 10mm thick, 8mm center bore"

**Tier 4 — Complex Functional Parts** (expected success: 5-20%)
- "A parametric living hinge, 100mm span, 0.3mm flex zone"
- "An S-curve pipe fitting, 15mm inner diameter, 45° bend"
- "A 3-part snap-fit assembly: housing, PCB carrier, lid"

### Evaluation Metrics

**Automated Metrics (computed per submission):**
1. **Validity Rate** — does the code compile/execute to a valid solid?
2. **Chamfer Distance (CD)** — geometric similarity to ground truth mesh
3. **Volume Accuracy** — correct overall volume?
4. **Feature Completeness** — do requested features exist? (VLM judge)
5. **Manufacturability Score** — watertight, no self-intersections, correct topology

**Human/LLM Judge Metrics:**
6. **Prompt Adherence** — Gemini/GPT-4o as judge (0-10)
7. **Engineering Correctness** — does it look like a real part?

---

## 5. 3D Visualization Stack

### Option A: Server-side STEP → mesh, serve GLB (Recommended)
```
STEP/STL/CadQuery code → Open CASCADE (pythonocc) → GLB/OBJ → Three.js viewer
```
- Server converts CAD output to GLB
- Frontend: Three.js or `<model-viewer>` web component (Google)
- Pro: Works for all output formats, consistent quality
- Packages: `cadquery`, `pythonocc-core`, `trimesh`, `gltflib`

### Option B: In-browser OCCT via WebAssembly
- `occt-import-js` — JS library parsing STEP files in browser
- `pythonocc-js` — WebAssembly port (heavier, ~20MB WASM blob)
- Pro: No server conversion needed
- Con: Slow load, large bundle

### Option C: Three.js + STL loader (Simplest)
- Convert to STL server-side, load in Three.js STLLoader
- Pro: Very simple, well-supported
- Con: Loses color/material info

**Recommended viewer controls:**
- Orbit / zoom / pan (Three.js OrbitControls)
- Wireframe toggle
- Section cut plane
- Dimension measurement overlay
- Download button (STEP, STL, OBJ)

---

## 6. Tech Stack Recommendation

### Frontend
```
Next.js 15 (App Router)
TypeScript
Tailwind CSS
Three.js + @react-three/fiber + @react-three/drei
Framer Motion (animations)
Recharts (metrics visualization)
```

### Backend
```
FastAPI (Python) — model API calls, file conversion
Redis — queue for model generation jobs
PostgreSQL — prompt/result/vote storage
S3/R2 — generated file storage (STEP, GLB, STL)
```

### CAD Processing
```
CadQuery — execute generated CadQuery code
pythonocc-core — STEP import/export, mesh conversion
trimesh — mesh validation, watertight checks
Open3D — point cloud processing
```

### Infrastructure
```
Modal or RunPod — GPU compute for model inference
Vercel — frontend hosting
Railway or Render — FastAPI backend
Cloudflare R2 — file storage
```

### Arena Voting System
```
Elo rating (same as Chatbot Arena / 3D Arena)
Bradley-Terry model for statistical ranking
Store: (prompt_id, model_a, model_b, winner, voter_id, timestamp)
```

---

## 7. Publication Strategy

### Paper Type: Benchmark/Dataset Paper
Similar to: SWE-bench (NeurIPS), GLUE (EMNLP), 3DGen-Bench (arXiv), DesignQA (ASME)

### Paper Title Ideas
- "CAD-Arena: An Open Platform for Evaluating Text-to-CAD Generation"
- "TextCAD-Bench: A Comprehensive Benchmark for Text-to-Parametric-CAD Generation"
- "Open CAD: A Living Benchmark for AI-Generated Parametric Models"

### Paper Structure
1. Introduction — why no unified benchmark exists
2. Related Work — existing benchmarks, their limitations (Table 1 = our landscape research)
3. Benchmark Design — prompt set, difficulty tiers, metrics
4. Experimental Evaluation — all models on our benchmark (Table 2 = big results table)
5. Arena System — description of pairwise evaluation + crowd voting
6. Analysis — where models succeed/fail, capability radar charts
7. Platform Description — website, submission process, ongoing updates
8. Conclusion + call for submissions

### Target Venues
- **NeurIPS 2026 Datasets & Benchmarks Track** (deadline ~June 2026) — ideal, same venue as Text2CAD
- **ICCV 2026** (deadline ~March 2026) — very tight but possible
- **SIGGRAPH 2026** (CAD papers strong presence) — deadline ~Jan 2026 (missed)
- **arXiv preprint first** — immediate visibility

### Differentiation from Existing Work
1. **First cross-model evaluation** covering academic + commercial simultaneously
2. **First living leaderboard** (not just paper-time snapshot)
3. **First arena-style pairwise voting** for parametric CAD
4. **Broader metrics** including manufacturability (watertight, valid topology)
5. **Difficulty tiers** enabling fine-grained capability analysis

---

## 8. Phased Build Plan

### Phase 1: Static Benchmark (2-4 weeks)
- [ ] Finalize 200-prompt benchmark set with ground truth STEPs
- [ ] Run all available models on the benchmark
- [ ] Compute metrics (Validity, CD, VLM judge)
- [ ] Build simple results table website
- [ ] Write arXiv preprint

### Phase 2: Arena MVP (4-6 weeks)
- [ ] Build Next.js frontend with Three.js viewer
- [ ] Connect Zoo API + GPT-4o → CadQuery baseline
- [ ] Implement pairwise voting + Elo scoring
- [ ] Add 3D visualization for comparison

### Phase 3: Full Platform (6-10 weeks)
- [ ] Add more model integrations (Text2CAD, FlexCAD, etc.)
- [ ] Public model submission portal
- [ ] Automated metrics pipeline
- [ ] Blog + paper hosting
- [ ] Community features (prompt sharing, leaderboard)

---

## 9. Key Risks

1. **Model access**: Many academic models have no hosted API; need to run inference ourselves
2. **Ground truth generation**: Who generates the "correct" STEP for each prompt? Need expert review
3. **Metric validity**: Chamfer Distance doesn't capture engineering correctness; need better metrics
4. **Commercial API costs**: Zoo at $0.50/min, AdamCAD TBD — need budget for evaluation runs
5. **Junk votes in arena**: Need CAPTCHA + IP deduplication for meaningful Elo

---

## 10. Competitive Moat

If built well, this becomes the **reference benchmark** cited by every new text-to-CAD paper. The network effect means:
- Papers submit to the leaderboard for visibility
- More models → more visitors → more community votes → better signal
- Platform becomes "SWE-bench for CAD" — mandatory citation

This is a common pattern: Chatbot Arena (LMSYS → 1M+ votes), SWE-bench (mandatory citation for code agents), GLUE/SuperGLUE (NLP standard). The CAD version doesn't exist. Being first matters.
