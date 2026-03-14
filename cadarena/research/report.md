# AI for CAD: State of the Field Report

**Compiled: February 2026**
**Sources: 173 research papers, 60 companies, 2 comprehensive surveys, and individual paper analysis**

---

## Executive Summary

Artificial intelligence is rapidly transforming Computer-Aided Design. What began in 2021 with DeepCAD — the first deep generative model for CAD sequences — has exploded into a field with 170+ papers, $7B+ in startup funding, and every major CAD vendor racing to ship AI features. The core research question has evolved from "can we generate CAD at all?" to "can we generate engineering-grade, editable, parametric CAD from natural language or images?" The answer, as of early 2026, is: partially — simple to moderate parts yes, complex constrained assemblies not yet.

This report synthesizes the full landscape: the research approaches, key benchmarks, datasets, open problems, the startup ecosystem, and what the incumbents are doing.

---

## Table of Contents

1. [How the Field is Structured](#1-how-the-field-is-structured)
2. [CAD Representations: The Core Technical Challenge](#2-cad-representations-the-core-technical-challenge)
3. [Generation Approaches](#3-generation-approaches)
4. [Key Benchmarks and Datasets](#4-key-benchmarks-and-datasets)
5. [Quantitative Results: Where Models Stand](#5-quantitative-results-where-models-stand)
6. [Reconstruction: From the Real World Back to CAD](#6-reconstruction-from-the-real-world-back-to-cad)
7. [CAD Analysis and Understanding](#7-cad-analysis-and-understanding)
8. [The LLM Revolution in CAD](#8-the-llm-revolution-in-cad)
9. [Industry Landscape](#9-industry-landscape)
10. [Open Problems and Research Gaps](#10-open-problems-and-research-gaps)
11. [Key Takeaways](#11-key-takeaways)
12. [Paper Reference Index](#12-paper-reference-index)

---

## 1. How the Field is Structured

The "Geometric Deep Learning for CAD" survey (Heidari & Iosifidis, 2025, arXiv:2402.17695) provides the clearest taxonomy. The field breaks into two major branches:

**CAD Analysis with GDL (understanding existing CAD):**
- Classification and retrieval (finding similar parts)
- Segmentation (identifying machining features, faces, operations)
- Assembly prediction (how parts fit together)

**CAD Construction with Generative Deep Learning (creating new CAD):**
- 2D sketch generation (engineering sketches with constraints)
- 3D CAD command generation (sketch-and-extrude sequences)
- Direct B-rep synthesis (generating boundary representations directly)
- 3D CAD from point clouds (scan-to-CAD)
- 3D CAD from images (photo/sketch to CAD)

The "LLMs for CAD" survey (Zhang et al., 2025, arXiv:2505.08137) adds a parallel taxonomy for the LLM-specific work:
- Data generation (using LLMs to create CAD training datasets)
- CAD code generation (17 papers — the largest category)
- Parametric CAD generation (9 papers)
- Model evaluation (using VLMs to judge CAD quality)
- Text generation (descriptions, comments on CAD programs)

**Paper counts from our database by category:**

| Category | Papers |
|----------|--------|
| Generation (text/image/sketch to CAD) | 68 |
| Reconstruction (point cloud/scan/image to CAD) | 35 |
| Analysis (understanding, retrieval, segmentation) | 20 |
| Survey papers | 16 |
| Datasets | 10 |
| Optimization (topology, generative design) | 10 |
| Adjacent (general 3D generation, sim-to-real) | 14 |
| **Total** | **173** |

---

## 2. CAD Representations: The Core Technical Challenge

The single most important technical question in the field is: **how do you represent a CAD model in a way that neural networks can learn?**

CAD models are fundamentally different from images, text, or even meshes. A CAD model is:
- **Sequential**: built through a series of operations (sketch, extrude, fillet, boolean)
- **Parametric**: every dimension is a parameter that can be changed
- **Constrained**: geometric relationships (parallel, perpendicular, coincident) must hold
- **Topologically structured**: represented as B-rep (boundary representation) with faces, edges, vertices, and their relationships

The field has converged on several representation strategies:

### 2.1 CAD Command Sequences
Pioneered by **DeepCAD** (Wu et al., 2021, ICCV, arXiv:2105.09492). Represents a CAD model as a sequence of commands: sketch primitives (line, arc, circle) interleaved with extrusion commands. Each command is a fixed-size vector of quantized parameters. The sequence is padded to a fixed length (N_c = 60 commands in DeepCAD).

Key insight from DeepCAD: "Our specification of a CAD model is akin to natural language. The vocabulary consists of individual CAD commands expressed sequentially to form sentences." This analogy — CAD as language — has driven most subsequent work.

Used by: DeepCAD, SkexGen, Text2CAD (Khan et al., NeurIPS 2024), FlexCAD (ICLR 2025), CAD-GPT, Diffusion-CAD, and many others.

**Strengths:** Human-interpretable, editable in CAD software, large datasets available (DeepCAD: 178,238 models, Fusion 360: 8,625).
**Weaknesses:** Limited to sketch-and-extrude operations; fillets, chamfers, sweeps, lofts are not represented. Fixed sequence length limits complexity.

### 2.2 Direct B-rep Generation
Rather than generating the sequence of operations, generate the boundary representation directly — the actual surfaces, edges, and vertices.

Key papers:
- **BrepGen** (Xu et al., SIGGRAPH 2024, arXiv:2401.15563) — diffusion model generating structured latent geometry for B-rep
- **SolidGen** (Jayaraman et al., 2022, arXiv:2203.13944) — autoregressive B-rep generation
- **BrepGPT** (2025, SIGGRAPH Asia, arXiv:2511.22171) — autoregressive with Voronoi half-patch representation
- **AutoBrep** (2025, SIGGRAPH Asia, arXiv:2512.03018) — unified topology and geometry
- **DTGBrepGen** (2025, CVPR, arXiv:2503.13110) — decoupled topology and geometry
- **HoLa** (2025, SIGGRAPH, arXiv:2504.14257) — holistic latent representation
- **BrepDiff** (2025, SIGGRAPH) — single-stage B-rep diffusion

**Strengths:** Can produce more complex shapes than command sequences. Output is directly a solid model.
**Weaknesses:** Harder to edit. No construction history. Datasets with clean B-rep annotations are scarce.

### 2.3 CAD Code Generation
Instead of learning a neural representation, use LLMs to generate executable code in CAD scripting languages: OpenSCAD, CadQuery (Python), FreeCAD Python, or proprietary macro languages.

Key papers:
- **Text-to-CadQuery** (2025, arXiv:2505.06507) — generates CadQuery Python code from text
- **CAD-Recode** (2025, ICCV, arXiv:2412.14042) — reverse-engineers CadQuery code from point clouds using Qwen2-1.5B with a point cloud projector
- **Generating CAD Code with VLMs** (ICLR 2025, arXiv:2410.05340) — uses vision-language models to generate executable CAD code
- **EvoCAD** (2025, arXiv:2510.11631) — evolutionary approach with VLMs
- **Generative AI for CAD Automation** (Kumar et al., 2026, arXiv:2508.00843) — LLM + FreeCAD with iterative error refinement
- **ScadLM**, **CQAsk** — open source projects

**Strengths:** Output is fully parametric and editable. Leverages the massive code training of foundation LLMs. Can produce complex shapes with booleans, fillets, etc. Human-readable.
**Weaknesses:** Code execution can fail (syntax errors, geometric inconsistencies). Requires a CAD kernel to execute. Quality is highly dependent on the LLM's code generation ability.

### 2.4 Hybrid Approaches
Several 2025 papers combine LLMs with learned geometric representations:
- **CADFusion** (Wang et al., 2025, arXiv:2501.19054) — LLaMA-3 8B backbone with visual feedback training stage
- **CAD-Llama** (CVPR 2025, arXiv:2505.04481) — leverages LLMs for parametric CAD generation
- **FlexCAD** (ICLR 2025, arXiv:2411.05823) — fine-tuned LLMs for controllable CAD with multiple input conditions
- **ReCAD** (2025, arXiv:2512.06328) — reinforcement learning enhanced VLM for parametric CAD
- **CAD-Coder** (2025, arXiv:2505.19713) — chain-of-thought reasoning with geometric reward functions

---

## 3. Generation Approaches

### 3.1 The DeepCAD Lineage (Autoencoder + GAN/Diffusion)
**DeepCAD** (Wu et al., 2021) established the template: train a Transformer autoencoder on command sequences, then use latent-GAN or diffusion to sample new designs from the latent space.

The DeepCAD dataset contains **178,238 CAD models** from Onshape, each represented as a sequence of sketch-and-extrude operations. This is ~20x larger than the prior Fusion 360 Gallery dataset (~8,000 models).

DeepCAD's autoencoder achieves **99.50% command accuracy** and **97.98% parameter accuracy** on reconstruction (with augmentation). For generation, it achieves Coverage (COV) of 78.13 and JSD of 3.76, comparable to point-cloud generative models while producing sharp, editable CAD models.

**SkexGen** (Xu et al., ICML 2022, arXiv:2207.04632) improved on DeepCAD with disentangled codebooks for topology, geometry, and extrusion — giving users finer control over generation.

**Diffusion-CAD** (2024) formulated CAD generation as continuous denoising diffusion over command sequences, adding multiple control mechanisms: command-type control, dimension control, partial sketch completion, structural control (symmetry, perpendicularity), and class-conditional generation.

### 3.2 Text-to-CAD
The most commercially relevant direction. Key approaches:

**Text2CAD** (Khan et al., NeurIPS 2024, arXiv:2409.17106) — generates sequential CAD designs from beginner-to-expert level text prompts. Uses the DeepCAD dataset augmented with text descriptions generated by VLMs. Four levels of text complexity: abstract, simplified, generalized geometric, and detailed geometric.

**CAD-GPT** (2025, arXiv:2412.19663) — multimodal LLM enhanced with spatial reasoning to synthesize CAD construction sequences from text and image inputs. Uses LLaVA-1.5 7B as backbone, maps 3D space to 1D tokens for spatial reasoning.

**NURBGen** (2025, arXiv:2511.06194) — LLM-driven NURBS modeling for high-fidelity text-to-CAD with precise surface control.

**Text-to-CadQuery** (2025, arXiv:2505.06507) — a code-generation approach that produces CadQuery Python scripts from text, yielding real STEP/BREP geometry.

### 3.3 Image-to-CAD
Bridging vision to engineering models:

**CADCrafter** (CVPR 2025, arXiv:2504.04753) — generates editable CAD models from unconstrained real-world images.

**CADDreamer** (CVPR 2025, arXiv:2502.20732) — single-view image to parametric CAD.

**Img2CAD** (2024, arXiv:2407.15886) — VLM-assisted decomposition of images into CAD primitives.

**From 2D CAD Drawings to 3D Parametric Models** (AAAI 2025, arXiv:2412.11892) — vision-language approach for converting engineering drawings to 3D.

### 3.4 Direct B-rep Generation
The 2024-2025 period saw a burst of B-rep generation papers, many at top graphics venues:

**BrepGen** (SIGGRAPH 2024) pioneered structured latent diffusion for B-rep. The 2025 SIGGRAPH/SIGGRAPH Asia cycle brought **BrepDiff**, **Stitch-A-Shape**, **HoLa**, **CLR-Wire** (SIGGRAPH 2025) and **BrepGPT**, **AutoBrep** (SIGGRAPH Asia 2025) — collectively representing a major push toward generating B-rep directly.

**DTGBrepGen** (CVPR 2025, arXiv:2503.13110) decouples topology and geometry prediction, improving structural validity.

---

## 4. Key Benchmarks and Datasets

### 4.1 Datasets

From the GDL survey (Heidari & Iosifidis, 2025), here are the critical CAD datasets:

| Dataset | Size | Has B-Rep | Has Mesh | Has Sketch | Categories | Primary Use |
|---------|------|-----------|----------|------------|------------|-------------|
| **ABC** | 1M+ | Yes | Yes | No | -- | Reconstruction |
| **Fusion 360 Gallery** | 8,625 | Yes | Yes | No | -- | Reconstruction |
| **SketchGraphs** | 15M+ | No | No | Yes | -- | Sketch generation |
| **DeepCAD** | 178,238 | Yes | No | No | -- | Command generation |
| **CAD as Language** | 4.7M+ | No | No | Yes | -- | Sketch generation |
| **ShapeNet** | 3M+ | No | Yes | No | 3,135 | Classification |
| **Fusion 360 Assembly** | 154,468 | Yes | Yes | No | -- | Joint prediction |
| **AutoMate** | 3M+ | Yes | Yes | No | -- | Joint prediction |
| **MFCAD** | 15,488 | Yes | No | No | 16 | Segmentation |
| **MFCAD++** | 59,655 | Yes | No | No | 25 | Segmentation |
| **Fusion 360 Segmentation** | 35,680 | Yes | Yes | No | 8 | Segmentation |
| **SolidLetters** | 96,000 | Yes | No | No | 26 | Classification |
| **FabWave** | 5,373 | Yes | Yes | No | 52 | Classification |
| **CC3D-Ops** | 37,000 | Yes | No | Yes | -- | Segmentation |

**Key observation from the survey:** "The scarcity of annotated CAD data available in the B-Rep format" is the single biggest bottleneck. Most large-scale public databases (ABC) are predominantly unlabeled. Manually annotating B-Rep data requires engineering expertise and is extremely costly.

The three foundational datasets are:
1. **ABC** (Koch et al., CVPR 2019, arXiv:1812.06216) — 1M+ hand-designed CAD models from Onshape. First large-scale, real-world B-rep dataset.
2. **SketchGraphs** (Seff et al., ICML 2020 Workshop, arXiv:2007.08506) — 15M+ real-world 2D CAD sketches from Onshape, represented as geometric constraint graphs. ~40% of new CAD designs are built from existing designs in repositories.
3. **DeepCAD dataset** (Wu et al., ICCV 2021, arXiv:2105.09492) — 178,238 models with full CAD construction sequences. The standard benchmark for command-sequence generation.

### 4.2 Evaluation Metrics

The field uses several metrics, none fully satisfactory:

**For command sequence reconstruction:**
- **Command Accuracy (ACC_cmd):** % of correctly predicted command types
- **Parameter Accuracy (ACC_param):** % of parameters within tolerance threshold (eta=3 out of 256 levels)
- **Invalid Ratio:** % of generated sequences that fail to produce valid geometry

**For shape quality (point-cloud based):**
- **Chamfer Distance (CD):** geometric distance between generated and reference shapes
- **Coverage (COV):** % of reference shapes well-approximated by generated shapes
- **Minimum Matching Distance (MMD):** fidelity of generated shapes
- **Jensen-Shannon Divergence (JSD):** distributional similarity between sets

**For code generation:**
- **Parsing Rate:** % of generated code that executes without error
- **Intersection over Union (IoU):** geometric overlap with ground truth
- **Visual fidelity scores:** using VLMs to compare rendered output to specification

---

## 5. Quantitative Results: Where Models Stand

### 5.1 DeepCAD Benchmark Results (Autoencoding)

From DeepCAD (Wu et al., 2021):

| Method | ACC_cmd | ACC_param | Median CD (x10^3) | Invalid Ratio |
|--------|---------|-----------|-------------------|---------------|
| DeepCAD+Aug | **99.50** | **97.98** | **0.752** | **2.72** |
| DeepCAD | 99.36 | 97.47 | 0.787 | 3.30 |
| Alt-Regression | -- | -- | 2.142 | 4.32 |

### 5.2 Text-to-CAD Benchmark Comparison

The most comprehensive comparison comes from combining results across recent papers. All numbers are Chamfer Distance (CD) ×10^3 unless noted:

| Method | Params | Median CD | Mean CD | IR (%) | Visual Eval |
|--------|--------|-----------|---------|--------|-------------|
| Text2CAD (NeurIPS 2024) | 363M | 0.370 | 26.42 | 3.5% | 58.80% (Gemini) |
| **Text-to-CadQuery** (Qwen2.5-3B) | 3B | **0.191** | 10.23 | 6.5% | **69.30%** (Gemini) |
| Text-to-CadQuery (CodeGPT-small) | 124M | 0.234 | 13.52 | -- | 60.28% (Gemini) |
| **CAD-Coder** (Qwen2.5-7B + GRPO) | 7B | 0.17 | **6.54** | **1.45%** | -- |
| CAD-Coder (SFT only) | 7B | -- | 74.55 | -- | -- |
| **CADFusion** (LLaMA-3-8B + DPO) | 8B | -- | 19.89 | 6.20 | **8.96/10** (LVM) |
| GPT-4o (zero-shot) | -- | -- | 133.52 | 93.00% | 5.13/10 (LVM) |
| Claude-3.7-Sonnet (zero-shot) | -- | -- | 186.53 | 47.03% | -- |
| DeepSeek-V3 (zero-shot) | -- | -- | 186.69 | 51.96% | -- |

**Key findings:**
- **Text-to-CadQuery** shows that generating CadQuery code outperforms command sequences: 48.6% reduction in median CD over Text2CAD, with a model 10x smaller (124M vs 363M).
- **CAD-Coder** demonstrates that RL (GRPO) with geometric reward is transformative: SFT alone gives Mean CD=74.55, adding GRPO reduces it to 6.54 — a 91% improvement. Training cost: 146 hours on 8× A800 GPUs.
- **CADFusion** shows visual feedback (DPO with VLM scoring) works: LVM Score improves from 7.69 (SL-only) to 8.96 (5 SL+VF iterations).
- **Zero-shot LLMs fail catastrophically** at CAD: GPT-4o has 93% Invalid Ratio, Claude-3.7 has 47%.

### 5.3 Image-to-CAD Benchmark (CAD-GPT)

From CAD-GPT (AAAI 2025, arXiv:2412.19663), which adds spatial localization tokens to LLaVA-1.5 7B:

| Method | Input | IR (%) | Median CD | ACC_cmd | ACC_param |
|--------|-------|--------|-----------|---------|-----------|
| **CAD-GPT** | Image | **1.61** | **9.77** | 99.21 | 98.87 |
| HNC-CAD (prior best) | Image | 18.64 | 18.64 | -- | -- |
| GPT-4 (few-shot) | Image | 64.37 | 62.64 | -- | -- |
| **CAD-GPT** | Text | **7.43** | **28.33** | 98.73 | 98.12 |
| GPT-4 (few-shot) | Text | 76.97 | 187.52 | -- | -- |
| LLaMA-3.1 (few-shot) | Text | 98.68 | -- | -- | -- |

**Key insight:** Image-to-CAD (median CD=9.77) is significantly easier than text-to-CAD (median CD=28.33) — images provide more precise geometric specification than language.

### 5.4 Point-Cloud-to-CAD (CAD-Recode)

From CAD-Recode (ICCV 2025, arXiv:2412.14042), using Qwen2-1.5B with point cloud projector:

| Dataset | Mean CD | Median CD | IoU (%) | IR (%) |
|---------|---------|-----------|---------|--------|
| DeepCAD test | 0.30 | 0.16 | 92.0 | 0.4 |
| Fusion360 test | 0.35 | 0.15 | 87.8 | 0.5 |
| CC3D (real scans) | 0.76 | 0.31 | 74.2 | 0.3 |
| Prior best (CAD-SIGNet) | 3.33 | 2.36 | 81.5 | -- |

**Key insight:** CAD-Recode achieves ~10× improvement over prior methods, trained on 1M procedurally generated CadQuery scripts (12 hours on one H100). Demonstrates that synthetic data at scale can substitute for expensive human-annotated datasets.

### 5.5 Controllable Generation (FlexCAD)

From FlexCAD (ICLR 2025, arXiv:2411.05823), using LLaMA-3-8B with LoRA:

| Method | COV (%) | MMD | JSD | PV (%) | Realism (human) |
|--------|---------|-----|-----|--------|-----------------|
| FlexCAD (sketch-level) | 65.6 | 1.19 | 0.82 | 93.4 | 39.6% |
| FlexCAD (extrusion-level) | 68.5 | 1.19 | 1.32 | 93.3 | 42.1% |
| SkexGen | 55.2 | -- | -- | 72.6 | 21.3% |
| GPT-4o (no fine-tune) | 40.1 | -- | -- | 48.9 | 12.8% |

FlexCAD's hierarchy-aware masking enables controllable editing at any level of the CAD hierarchy: sketch, extrusion, face, loop, or curve.

### 5.6 CAD Code Verification (CADCodeVerify)

From "Generating CAD Code with VLMs" (ICLR 2025, arXiv:2410.05340):

| Method | Compile Rate | IoGT | Point Cloud Dist | Hausdorff Dist |
|--------|-------------|------|-------------------|----------------|
| GPT-4 + CADCodeVerify | **96.5%** | **0.944** | **0.127** | **0.419** |
| GPT-4 + 3D-Premise | 91.0% | 0.921 | 0.137 | 0.452 |
| GPT-4 (no refinement) | 91.0% | 0.912 | 0.142 | -- |
| Human-in-the-loop | -- | -- | 0.120 | -- |

Uses automated VLM-based verification: renders the CAD object, generates Yes/No questions about it, answers via chain-of-thought, and provides feedback. Human-in-the-loop only marginally outperforms the automated approach.

### 5.7 LLM-based FreeCAD Generation (Kumar et al., 2026)

From "Generative AI for CAD Automation" (arXiv:2508.00843), testing GPT-4 with FreeCAD across 10 complexity levels:

| Complexity | Task | Result |
|------------|------|--------|
| 1 (Basic cube) | Simple shape creation | Success, 1st attempt, 19s |
| 2 (Cylinder) | Defined radius/height | Success, 1st attempt, 20s |
| 3 (Filleted cuboid) | Edge fillets | Converged after 1 refinement, 42s |
| 4 (Boolean union) | Box + cylinder merge | Success, 1st attempt, 22s |
| 5 (Boolean subtraction) | Hole through solid | Success, 1st attempt, 23s |
| 6 (Parametric plate + 4 holes) | Fully constrained model | Success, 1st attempt, 28s |
| 7 (Parametric hinge) | Multiple segments, constraints | Converged after 2 refinements, 54s |
| 8 (Involute gear) | Specialized geometry | **Failed** (50 iterations, 836s) |
| 9 (Plate with cutouts) | Complex feature constraints | Converged after 2 refinements, 81s |
| 10 (Constrained frame) | Reinforcement ribs, multiple constraints | **Failed** (50 iterations, 909s) |

**Key finding:** LLMs handle simple-to-moderate complexity (levels 1-7) well, but fail on highly specialized geometry (gears) and fully constrained parametric models.

### 5.8 LLM Usage in CAD Research

From the LLM survey (Zhang et al., 2025), the most frequently used LLMs in CAD research:
1. GPT-4o — 11 papers
2. GPT-4 — 8 papers
3. GPT-4V — 4 papers
4. LLaVA variants — 3 papers
5. ChatGPT — 2 papers

The OpenAI GPT family dominates despite being closed-source, due to superior code generation and spatial reasoning capabilities.

---

## 6. Reconstruction: From the Real World Back to CAD

Reverse engineering — recovering editable CAD models from physical scans or images — is a critical practical problem. Key papers:

**Point Cloud to CAD:**
- **Point2CAD** (Liu et al., 3DV 2024, arXiv:2312.04962) — detects geometric primitives and relationships from point clouds
- **CAD-Recode** (Rukhovich et al., ICCV 2025, arXiv:2412.14042) — reverse-engineers CadQuery code from point clouds using Qwen2-1.5B with a lightweight point cloud projector. GPT-4o refactors code for interactive editing.
- **ComplexGen** (Guo et al., SIGGRAPH 2022, arXiv:2205.14573) — reconstructs B-rep from point clouds via chain complexes
- **Point2Cyl** (Uy et al., CVPR 2022, arXiv:2112.09329) — decomposes point clouds into extrusion cylinders
- **SECAD-Net** (Li et al., CVPR 2023, arXiv:2303.12084) — self-supervised sketch-extrude reconstruction
- **CAD-SIGNet** (Agarwal et al., CVPR 2024, arXiv:2305.02278) — infers sketch-and-extrude sequences from point clouds

**Scan/Image to CAD:**
- **Scan2CAD** (Avetisyan et al., CVPR 2019, arXiv:1811.11187) — aligns CAD models to RGB-D scans
- **InverseCSG** (Du et al., SIGGRAPH Asia 2018, arXiv:1811.10719) — converts meshes to CSG trees
- **CSGNet** (Sharma et al., CVPR 2018, arXiv:1712.08290) — parses shapes into CSG programs
- **ExtrudeNet** (Ren et al., ECCV 2022, arXiv:2209.15632) — unsupervised sketch-and-extrude decomposition

**Sketch to CAD:**
- **Free2CAD** (Li et al., SIGGRAPH 2022, arXiv:2205.01762) — converts freehand drawings to CAD commands
- **Sketch2CAD** (Li et al., SIGGRAPH Asia 2020) — interactive sequential sketching to CAD
- **PICASSO** (WACV 2025, arXiv:2407.13394) — feed-forward parametric sketch inference

---

## 7. CAD Analysis and Understanding

### 7.1 B-Rep Learning
The foundational works for learning on B-rep:
- **UV-Net** (Jayaraman et al., CVPR 2021, arXiv:2006.10211) — learns features from B-rep via UV-grid sampling. The UV-Net encoder is the standard backbone for B-rep representation learning.
- **BRepNet** (Lambourne et al., CVPR 2021, arXiv:2104.00706) — first GNN specifically for B-rep segmentation, operating on coedge topology.

### 7.2 CAD Segmentation
Identifying machining features (chamfer, pocket, hole, slot, etc.) from B-rep geometry:
- **CADNet / Hierarchical CADNet** — GNN encoding face geometry and topology for machining feature classification. Released the **MFCAD++** dataset (59,655 models, 25 features).
- **SB-GCN** (Colligan et al., 2022) — structured B-rep graph convolutional network for machining feature recognition.

### 7.3 Assembly
- **AutoMate** (Jones et al., SIGGRAPH Asia 2021/2024, arXiv:2305.09174) — 92,529 assemblies from Onshape with 541,635 mate annotations
- **JoinABLe** (Willis et al., CVPR 2022, arXiv:2111.12772) — bottom-up joint prediction between B-rep parts using GAT v2

### 7.4 Semantic Understanding
- **CADTalk** (Yuan et al., SIGGRAPH 2024, arXiv:2311.16703) — adds semantic comments to CAD programs
- **CAD-Assistant** (ICCV 2025, arXiv:2412.13810) — tool-augmented VLLMs as generic CAD task solvers

---

## 8. The LLM Revolution in CAD

The LLM-for-CAD survey (Zhang et al., 2025) identifies this as a nascent but rapidly growing area. Key findings:

### 8.1 Two Paradigms

**Paradigm 1: CAD Code Generation (dominant, 17 papers)**
LLMs generate executable code (Python, OpenSCAD, CadQuery, FreeCAD scripts) that is then run through a CAD kernel. Almost all approaches use an iterative refinement loop: generate code, execute, if errors feed them back to the LLM and retry.

The survey notes: "Nearly all approaches utilize LLMs to generate intermediate representations rather than directly outputting 3D CAD models or 2D CAD drawings. Directly generating accurate 3D or 2D CAD outputs remains a significant challenge for current models."

**Paradigm 2: Parametric Sequence Generation (9 papers)**
LLMs are fine-tuned to generate parametric data (JSON-like sequences of sketch/extrude commands) rather than executable code. This avoids code execution issues but requires custom parsers.

### 8.2 The Visual Feedback Loop
A critical 2025 innovation: training LLMs with visual feedback. **CADFusion** (Wang et al., ICML 2025, arXiv:2501.19054) uses LLaMA-3-8B-Instruct with two alternating training stages:
1. **Sequential Learning (SL):** Fine-tune on 20K text-parametric pairs with human-annotated captions (human annotation boosts LVM score from 6.56 to 7.69)
2. **Visual Feedback (VF):** Direct Preference Optimization (DPO) where LLaVA-OneVision-Qwen2-7B scores rendered objects on shape quality/quantity/distribution. Generates ~1,500 preference pairs per iteration from 1,000 text prompts.

The two stages alternate for 5 iterations, preventing skill degradation. Result: LVM Score improves 8.28→8.76→8.89→8.96 across iterations.

**CADCodeVerify** (ICLR 2025, arXiv:2410.05340) takes a different approach: fully automated VLM-based verification at inference time. Renders CAD output, generates Yes/No verification questions, answers them with chain-of-thought, and feeds corrective feedback back to the code generator. Achieves within 5% of human-in-the-loop performance.

Both approaches are directly relevant to this project's pipeline (render → VLM describe → compare → iterate).

### 8.3 Multi-Agent Systems
**From Idea to CAD** (2025, arXiv:2503.04417) — multi-agent LLM system for collaborative CAD design. Multiple LLM agents with different roles (conceptual designer, detailer, verifier) collaborate to go from idea to finished model.

**CADDesigner** (2025, arXiv:2508.01031) — general-purpose agent for conceptual CAD from high-level specifications.

### 8.4 CAD Editing with Language
- **CAD-Editor** (2025, arXiv:2502.03997) — locate-then-infill framework for text-based CAD editing
- **B-repLer** (2025, arXiv:2508.10201) — language-guided editing of B-rep CAD models

---

## 9. Industry Landscape

### 9.1 Funding Overview

The AI-for-CAD startup ecosystem has attracted massive investment:

| Company | Total Funding | Stage | Focus |
|---------|--------------|-------|-------|
| Project Prometheus | **$6.2B** | Mega-round | Physical AI for engineering (Bezos-backed) |
| Divergent Technologies | $400M+ | Late | AI generative design + additive manufacturing |
| nTop | $95M+ | Series D | Computational design for advanced manufacturing |
| Machina Labs | $72M+ | Series B | AI-powered robotic manufacturing |
| Luma AI | $70M+ | Series B | 3D capture/generation |
| Zoo (formerly KittyCAD) | $30M+ | Series A | Text-to-CAD, open-source CAD kernel |
| Vizcom | $20M+ | Series A | AI sketch-to-rendering |
| Kaedim | $15M+ | Series A | Image to 3D |
| Hyperganic | $13M+ | Series A | AI voxel-based design for AM |
| Adam AI | $4.1M | Seed (YC W25) | Text-to-CAD for mechanical engineering |

### 9.2 Pure-Play AI-for-CAD Startups

**Zoo (formerly KittyCAD)** — The most prominent text-to-CAD startup. API-first approach with an open-source CAD kernel in Rust. ML models generate STEP/BREP from natural language. Freemium pricing: 40 free min/month, then $0.50/min. Backed by Sequoia Capital.

**Adam AI** (YC W25) — $4.1M seed. Open-source CADAM project. Plans Onshape integration. Focused specifically on mechanical engineering.

**Katalyst Labs** — Open-source AI copilot for hardware design. Acquired by Rubix LS in 2025-2026, indicating strategic value in the design-to-manufacturing chain.

**Tripo AI** — Text-to-CAD API for programmatic access. Multi-vertical (gaming, architecture, product design).

**Open source projects:**
- **ScadLM** (github.com/KrishKrosh/ScadLM) — agentic AI for OpenSCAD generation
- **CQAsk** (github.com/OpenOrion/CQAsk) — LLM-powered CadQuery generation
- **CADAM** (github.com/Adam-CAD/CADAM) — Adam AI's open-source text-to-CAD

### 9.3 Incumbent Moves

**Autodesk — Neural CAD (announced AU 2025):** Dedicated foundation models for geometry generation. Two models: one for product geometry (Fusion integration), one for buildings (Forma). Accepts text, sketch, and image inputs. Claims it can automate "80-90% of routine design tasks."

**Siemens — Altair acquisition ($10B, 2024) + Industrial Copilot:** Now owns the deepest AI simulation portfolio (HyperWorks, SimSolid, Inspire). Partnership with Microsoft on generative AI for engineering workflows. Altair ranked #1 by ABI Research for AI in engineering.

**Synopsys acquired Ansys ($35B, 2024):** Creates combined electronic + mechanical AI simulation. Ansys SimAI predicts simulation results in near real-time using ML.

**PTC/Onshape:** Cloud-native, API-first architecture makes Onshape the most AI-ready among major CAD platforms. Natural integration target for startups (Adam AI plans Onshape integration).

### 9.4 M&A Activity (2024-2026)

| Acquirer | Target | Value | Significance |
|----------|--------|-------|-------------|
| Synopsys | Ansys | $35B | Electronic + mechanical AI simulation |
| Siemens | Altair | ~$10B | AI simulation/optimization powerhouse |
| Rubix LS | Katalyst Labs | Undisclosed | Open-source AI CAD copilot |
| Altair/Siemens | Gen3D | Undisclosed | Generative design technology |
| nTop | Cloudfluid | Undisclosed | GPU-native CFD solver |

---

## 10. Open Problems and Research Gaps

### 10.1 Data Scarcity
The biggest bottleneck. From the GDL survey: "The scarcity of annotated CAD data available in the B-Rep format" limits the field. Most large-scale CAD databases are unlabeled, and manual annotation requires engineering expertise. There is no ImageNet-scale labeled B-rep dataset.

### 10.2 Complexity Ceiling
Current models excel at simple mechanical parts (brackets, flanges, basic enclosures) but struggle with:
- Complex constrained assemblies
- Involute gears, splines, and specialized geometry
- Parts with 10+ features and hierarchical dependencies
- Real engineering parts with tolerances and manufacturing constraints

The FreeCAD generation benchmark (Kumar et al., 2026) shows clear failure at complexity levels 8-10 (gears, fully constrained parametric frames).

### 10.3 The Representation Gap
Command sequences (DeepCAD-style) only handle sketch-and-extrude. Real CAD models use fillets, chamfers, sweeps, lofts, patterns, mirrors, shells, drafts, and more. No current representation captures the full range of CAD operations.

### 10.4 Evaluation
There is no agreed-upon benchmark for text-to-CAD. Chamfer Distance measures geometric similarity but not parametric editability, manufacturing feasibility, or constraint satisfaction. The field needs standardized benchmarks that evaluate:
- Geometric accuracy
- Parametric editability (can you change a dimension and have the model update correctly?)
- Constraint satisfaction (are perpendicularity, symmetry, etc. maintained?)
- Manufacturing feasibility

### 10.5 Assembly-Level Generation
Almost all work focuses on single parts. Generating multi-part assemblies with correct joint relationships is barely explored (AutoMate and JoinABLe are analysis, not generation).

### 10.6 Engineering Intent
No model captures "why" — the functional purpose, load paths, material choices, or manufacturing process that drove a design. Current models mimic form without understanding function.

### 10.7 Bridging Research and Industry
The LLM survey notes that the most common model used in research (GPT-4o) is closed-source and expensive. Deploying LLM-based CAD generation at scale with acceptable latency and cost remains unsolved. The "3D CAD software market is projected to grow from USD 13.40 billion in 2025 to USD 24.23 billion by 2034" — the commercial opportunity is clear but the technology isn't production-ready for complex parts.

---

## 11. Key Takeaways

1. **The field is in a "Cambrian explosion" phase.** 173 papers, 68 on generation alone, with publication velocity accelerating sharply in 2024-2025 (42 papers in 2024, 37 in 2025).

2. **Three generation paradigms are competing:** (a) learned command sequences (DeepCAD lineage), (b) direct B-rep synthesis (BrepGen lineage), and (c) LLM code generation (the newest and most commercially practical approach). None yet produces engineering-grade output for complex parts.

3. **LLMs are transforming the field.** The code generation approach — generating CadQuery/FreeCAD code — is emerging as the most practical path. Text-to-CadQuery shows even a 124M parameter model generating CadQuery code outperforms a 363M model generating command sequences. But zero-shot LLMs fail catastrophically: GPT-4o has 93% Invalid Ratio, Claude-3.7 has 47%. Fine-tuning or RL is essential.

4. **RL with geometric reward is the biggest performance lever.** CAD-Coder shows GRPO training reduces Mean CD from 74.55 (SFT-only) to 6.54 — a 91% improvement. CADFusion shows visual DPO improves LVM scores from 7.69 to 8.96. These are the most impactful techniques to emerge in 2025.

5. **The visual feedback loop works.** Both CADFusion (training-time DPO with VLM scoring) and CADCodeVerify (inference-time VLM verification) demonstrate that visual feedback is effective. CADCodeVerify achieves within 5% of human-in-the-loop performance. This directly validates this project's pipeline architecture.

6. **Data is the bottleneck, not architecture.** The DeepCAD dataset (178K models) is the standard, but it's limited to simple sketch-and-extrude shapes. CAD-Recode's key insight: 1M procedurally generated CadQuery scripts can substitute for expensive human-annotated data (achieving 92% IoU, 10× better than prior methods). Synthetic data generation is a viable path forward.

7. **The industry is betting big.** $6.2B (Project Prometheus) + $35B (Ansys acquisition) + $10B (Altair acquisition) = the largest players believe AI will fundamentally transform engineering design. But no one has a production-quality text-to-CAD system for real engineering parts yet.

8. **Onshape's architecture is the natural AI integration target.** Cloud-native, API-first, data-rich — multiple startups (Adam AI, etc.) are building on it.

9. **The open-source ecosystem is emerging.** ScadLM, CQAsk, CADAM, Zoo's CAD kernel — all open source. CadQuery is converging as the standard output format: 6 of the 10 most recent papers use it, citing executability, interpretability, and compatibility with pre-trained LLMs.

10. **Image-to-CAD is easier than text-to-CAD.** CAD-GPT shows median CD of 9.77 from images vs 28.33 from text. Images provide more precise geometric specification — relevant for this project's search pipeline which retrieves images.

11. **Key unsolved problems:** assembly-level generation, complex constrained geometry (gears, splines), engineering intent capture, standardized benchmarks, and the data scarcity problem for B-rep annotations.

12. **The most promising near-term recipe** for practical text-to-CAD (like this project) based on the evidence: fine-tuned open LLM (Qwen/LLaMA 3-8B) → CadQuery code generation → iterative error correction → RL with geometric reward (GRPO/DPO) → visual feedback via VLM comparison. This matches the pipeline architecture in this project.

---

## 12. Paper Reference Index

### Seminal / Must-Read Papers

| # | Paper | Year | Venue | Why It Matters |
|---|-------|------|-------|---------------|
| 100 | **DeepCAD** (Wu et al.) | 2021 | ICCV | First generative model for CAD; established the field; 178K model dataset |
| 34 | **Geometric DL for CAD Survey** (Heidari & Iosifidis) | 2025 | arXiv | Most comprehensive technical survey; dataset overview; taxonomy |
| 20 | **LLMs for CAD Survey** (Zhang et al.) | 2025 | ACM Computing Surveys | First systematic LLM+CAD survey; covers all code gen and parametric gen work |
| 44 | **BrepGen** (Xu et al.) | 2024 | SIGGRAPH | First diffusion model for direct B-rep generation |
| 42 | **Text2CAD** (Khan et al.) | 2024 | NeurIPS | Key text-to-CAD benchmark with multi-level text prompts |
| 79 | **SkexGen** (Xu et al.) | 2022 | ICML | Disentangled codebooks for controlled CAD generation |
| 102 | **BRepNet** (Lambourne et al.) | 2021 | CVPR | First GNN for B-rep; foundational for B-rep learning |
| 103 | **UV-Net** (Jayaraman et al.) | 2021 | CVPR | Standard B-rep encoder backbone |
| 113 | **SketchGraphs** (Seff et al.) | 2020 | ICML WS | 15M sketch dataset; enables sketch generation research |
| 123 | **ABC** (Koch et al.) | 2019 | CVPR | 1M+ CAD model dataset; standard for geometric DL |

### 2025 Highlights (Most Important Recent Papers)

| # | Paper | Venue | Approach |
|---|-------|-------|----------|
| 15 | **FlexCAD** | ICLR 2025 | Unified controllable CAD gen with fine-tuned LLMs |
| 16 | **CAD Code with VLMs** | ICLR 2025 | Vision-language models generating executable CAD code |
| 26 | **CAD-Recode** | ICCV 2025 | Reverse-engineering CadQuery code from point clouds |
| 17 | **CAD-Llama** | CVPR 2025 | LLM for parametric CAD model generation |
| 11 | **CADCrafter** | CVPR 2025 | CAD from unconstrained images |
| 10 | **DTGBrepGen** | CVPR 2025 | Decoupled topology/geometry B-rep generation |
| 6 | **Stitch-A-Shape** | SIGGRAPH 2025 | Bottom-up B-rep generation from local patches |
| 7 | **BrepDiff** | SIGGRAPH 2025 | Single-stage B-rep diffusion |
| 2 | **BrepGPT** | SIGGRAPH Asia 2025 | Autoregressive B-rep with Voronoi half-patch |
| 3 | **AutoBrep** | SIGGRAPH Asia 2025 | Unified topology/geometry autoregressive B-rep |
| 14 | **CADFusion** | arXiv | Text-to-CAD with LLM visual feedback |
| 21 | **Text-to-CadQuery** | arXiv | CadQuery code from text — practical for real engineering |
| 5 | **CAD-Coder** | arXiv | Chain-of-thought + geometric reward for text-to-CAD |

### By Category — Selected Key Papers

**Text/Language to CAD:** #42, #43, #21, #5, #14, #15, #17, #22
**Image to CAD:** #11, #12, #47, #29
**Point Cloud to CAD:** #26, #50, #63, #68, #82, #83
**B-Rep Generation:** #44, #2, #3, #6, #7, #8, #10, #87
**2D Sketch Generation:** #99, #104, #81
**CAD Analysis:** #45, #78, #94, #102, #103
**Assembly:** #53, #84, #106
**Datasets:** #46, #101, #113, #123, #154
**Surveys:** #20, #34, #35, #38, #62
**Topology Optimization + AI:** #60, #39, #109

*Paper numbers refer to the papers-database.md index.*

---

**End of Report**

*This report is based on 173 cataloged papers (116 with PDFs downloaded), 60 companies, and deep reading of key survey papers and individual research contributions. For the full structured database of all papers, see papers-database.md. For the complete companies analysis, see companies.md.*
