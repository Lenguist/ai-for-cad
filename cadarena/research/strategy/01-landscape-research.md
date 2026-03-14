# AI for CAD Benchmark Landscape Research
*Generated: 2026-03-03*

## TL;DR

**No arena-style text-to-CAD benchmark exists.** This is a clear gap. 3D mesh arenas exist (3D Arena, 3DGen-Bench) but none cover parametric CAD. Academic benchmarks exist as paper-specific one-shots; no living leaderboard with public submissions. Commercial tools are never compared against academic models.

---

## 1. Arena-Style Platforms (No CAD Coverage)

### Chatbot Arena (LMSYS) — The gold standard to emulate
- URL: https://chat.lmsys.org
- Model: Crowdsourced pairwise battles, Elo-based ranking
- Covers: LLM text quality
- **Gap**: No CAD generation track

### 3D Arena
- URL: https://huggingface.co/spaces/dylanebert/3d-arena
- Paper: https://arxiv.org/abs/2506.18787
- Model: Pairwise battles, 123K+ votes, 8K users, 19 models
- Covers: Image-to-3D mesh generation (Tripo, Meshy, HunyuanD, TRELLIS)
- Output formats: OBJ, GLB, PLY, SPLAT
- **Gap**: Visual/game-art meshes only. Zero parametric CAD.

### GenAI Arena (NeurIPS 2024)
- URL/Paper: https://arxiv.org/html/2406.04485v4
- GitHub: https://github.com/TIGER-AI-Lab/GenAI-Bench
- Covers: Text-to-image, image editing, text-to-video
- **Gap**: No 3D or CAD track

### Artificial Analysis Arena
- URL: https://artificialanalysis.ai
- Covers: Image and video generation
- **Gap**: No CAD track

---

## 2. 3D Generation Leaderboards (Close But Not CAD)

### 3DGen-Bench / 3DGen-Arena
- Leaderboard: https://huggingface.co/spaces/3DTopia/3DGen-Leaderboard
- Paper: https://arxiv.org/abs/2503.21745
- GitHub: https://github.com/3DTopia/3DGen-Bench
- Stats: 11,200 generated models, 19 methods, 68K+ preference votes
- Covers: Text-to-3D and image-to-3D mesh generation
- **Gap**: No parametric CAD / STEP / sketch-extrude / B-rep

---

## 3. Academic Text-to-CAD Benchmarks (Paper-Only, No Live Leaderboard)

### Text2CAD (NeurIPS 2024 Spotlight) — Best-known benchmark
- Project: https://sadilkhan.github.io/text2cad-project/
- GitHub: https://github.com/SadilKhan/Text2CAD
- Dataset: DeepCAD (~170K models, 600K+ text prompts, 4 abstraction levels)
- Metrics: F1 for CAD elements, Chamfer Distance, Invalidity Ratio
- **Gap**: No public submission leaderboard. Static paper results only.

### CADPrompt / Query2CAD (2024-2025)
- Papers: https://arxiv.org/html/2406.00144v1 and https://arxiv.org/html/2410.05340v2
- First benchmark for CAD code generation
- Stats: 200 NL prompts + expert CadQuery/OpenSCAD annotations
- Models tested: GPT-4 (96.5% compile), Gemini 1.5 (85%), CodeLlama (73.5%)
- Metrics: Compile rate, PCD, Hausdorff, DSC, IoU
- **Gap**: Only 200 prompts. No live leaderboard. Static results.

### Text-to-CadQuery (arXiv 2025)
- Paper: https://arxiv.org/html/2505.06507v1
- Dataset: ~170K text-CadQuery pairs (extends Text2CAD/DeepCAD)
- Models tested: 124M to 7B parameters
- Key finding: Self-correction raised execution success from 53% → 85%
- **Gap**: Paper-only evaluation.

### CAD-MLLM
- Project: https://cad-mllm.github.io/
- Paper: https://arxiv.org/html/2411.04954v1
- First multimodal conditioning (text + image + point cloud)
- Dataset: Omni-CAD (~450K instances)
- New metrics: SegE, DangEL, SIR, FluxEE for topological quality
- **Gap**: Research project only, no ongoing leaderboard.

### CAD-GPT
- Project: https://openiwin.github.io/CAD-GPT/
- Paper: https://arxiv.org/abs/2412.19663
- Multimodal LLM for CAD construction sequences
- **Gap**: Research project only.

### DesignQA (MIT/Autodesk, ASME 2025)
- Project: https://design-qa.github.io/
- Paper: https://arxiv.org/abs/2404.07917
- 1,449 questions on engineering documentation (Formula SAE)
- Tests rule comprehension from CAD images + engineering drawings
- Tested: GPT-4o, Claude-Opus, Gemini-1.0
- **Angle**: CAD *understanding*, not *generation*
- **Gap**: Narrow domain, no live leaderboard.

---

## 4. Editorial/Journalistic Comparisons (Not Scientific)

### Xometry Pro: "We Tested 7 Text-to-CAD Tools"
- URL: https://xometry.pro/en/articles/text-to-cad-tools-test/
- Tools: Zoo, AdamCAD, CADGPT, Vondy, CADScribe, OpenArt, Leo AI
- Method: 6 standardized prompts (simple to complex functional parts)
- **Best existing editorial comparison**: Uses consistent prompts, engineer perspective
- **Gap**: Qualitative only. Not reproducible. Not updated continuously.

### The CAD Hub Blog
- URL: https://thecadhub.com/blog/ai-cad-software-in-2025-adamcad-cadgpt-draftaid/
- Tools: AdamCAD, CADGPT, DraftAid, Zoo, Leo AI
- **Gap**: Opinion-based.

---

## 5. Curated Lists (Not Benchmarks)

### Awesome-CAD
- URL: https://github.com/bertjiazheng/Awesome-CAD
- Community-maintained paper list
- **Gap**: No rankings or benchmark results.

---

## 6. Commercial Tools with No Public Benchmark

| Tool | URL | Notes |
|------|-----|-------|
| Zoo / KittyCAD | https://zoo.dev/machine-learning-api | ML-ephant API, STEP/STL/GLB output, open-source UI. Most polished. |
| Autodesk CAD-LLM | https://www.research.autodesk.com/publications/ai-lab-cad-llm/ | Internal research, not public. |
| OnShape AI | onshape.com | AI co-pilot, 15M model library. No generation benchmark. |
| AdamCAD | adamcad.ai | YC W25, commercial product, no public benchmark. |
| Tripo AI | tripo3d.ai | Text-to-3D API, mostly meshes. |

---

## 7. Key Gaps — The Opportunity

1. **No arena-style pairwise comparison**: Chatbot Arena / 3D Arena model doesn't exist for parametric CAD.
2. **No standardized prompt set with public submissions**: No SWE-bench equivalent for CAD.
3. **No cross-methodology comparison**: Sequence-based (Text2CAD), code-based (Text-to-CadQuery), B-rep direct (BrepGen) are never compared on the same benchmark.
4. **No academic-vs-commercial comparison**: Zoo, AdamCAD never in academic tables; academic models never in commercial comparisons.
5. **No consensus quality metric**: No agreed-upon metric like FID/CLIP for CAD quality.
6. **No manufacturability metric**: Nothing tests if generated parts are actually manufacturable.

---

## 8. Key Survey Confirming the Gap

### LLMs for CAD Survey (arXiv 2025)
- URL: https://arxiv.org/html/2505.08137v1
- Explicitly identifies "lack of comprehensive evaluation frameworks" and "limited standardization" as critical gaps
- Directly calls for unified benchmarking platforms
