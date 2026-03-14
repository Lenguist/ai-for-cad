# Evaluation Criteria — CAD Arena Static Benchmark

Exhaustive extraction of every metric used across text-to-CAD papers, organized by category.

---

## Currently Implemented (v1)

| Metric | Type | Description | Papers |
|--------|------|-------------|--------|
| **Compiles** | Binary | Generated code executes without Python/syntax errors | All |
| **Valid STL** | Binary | Execution produces a non-empty STL file | All |
| **Generation time** | Numeric (s) | Wall-clock time from prompt to STL | All |

**Current leaderboard metric: % prompts producing a valid STL.**

---

## Validity & Executability

No ground truth required — purely code/mesh validation.

| Metric | Type | Description | Papers |
|--------|------|-------------|--------|
| **Invalid Ratio (IR)** | % | % of outputs that fail to produce valid geometry | Text2CAD, Text-to-CadQuery, CAD-Coder, CADFusion, CAD-GPT, CAD-Recode |
| **Validity Rate** | % | Inverse of IR: % producing a valid solid | FlexCAD |
| **Compile Rate** | % | % that pass syntax check only | CADPrompt, "Generating CAD Code with VLMs" |
| **Watertight** | Binary | Mesh is closed (no open edges) — via trimesh | Benchmark strategy |
| **Non-degenerate / No self-intersections** | Binary | Mesh has positive volume and no self-intersections | Benchmark strategy, CADCodeVerify |
| **Self-Intersection Ratio (SIR)** | Numeric | # self-intersecting faces / total faces | CAD-MLLM |
| **Dangling Edge Length (DangEL)** | Numeric (mm) | Total length of topologically invalid edges | CAD-MLLM |
| **Correct Topology** | Binary | # holes, # connected components matches spec | "Generating CAD Code with VLMs" |

---

## Geometric Similarity

Requires a reference/ground-truth mesh.

| Metric | Type | Description | Papers |
|--------|------|-------------|--------|
| **Chamfer Distance (CD)** | Numeric | Mean nearest-neighbor distance between generated and reference point clouds | DeepCAD, Text2CAD, Text-to-CadQuery, CAD-Coder, CAD-GPT, CAD-Recode |
| **Median CD** | Numeric | Median CD (more robust to outliers) | Text2CAD, CAD-GPT, CAD-Recode |
| **Hausdorff Distance (HD)** | Numeric | Max distance at worst-matching point — captures outlier misalignment | CADPrompt, "Generating CAD Code with VLMs" |
| **Coverage (COV)** | % | % of reference shapes well-approximated by generated shapes | DeepCAD, SkexGen, FlexCAD |
| **Minimum Matching Distance (MMD)** | Numeric | Fidelity: min distance to reference at best match | DeepCAD, SkexGen, FlexCAD |
| **Jensen-Shannon Divergence (JSD)** | Numeric | Distributional similarity between sets of generated vs reference shapes | DeepCAD, SkexGen, FlexCAD |
| **Intersection over Union (IoU)** | 0–1 | Volumetric overlap between generated and reference solid | CAD-Recode, CADPrompt, CAD-GPT |
| **IoGT (Intersection over Ground Truth)** | 0–1 | Like IoU but normalized by GT volume only | "Generating CAD Code with VLMs" (ICLR 2025) |
| **Point Cloud Distance (PCD)** | Numeric | L2 distance between generated and reference point clouds | CADPrompt, "Generating CAD Code with VLMs" |
| **Volume Accuracy** | % | |gen_volume − ref_volume| / ref_volume | Benchmark strategy |
| **Bounding Box Accuracy** | Numeric | Comparison of key dimensions (XYZ extents) to spec | Preliminary results benchmark |

---

## Command Sequence Accuracy

Only applicable to DeepCAD-style sequence models (Text2CAD, DeepCAD, CAD-GPT). Not applicable to CadQuery/OpenSCAD LLM baselines.

| Metric | Type | Description | Papers |
|--------|------|-------------|--------|
| **Command Accuracy (ACC_cmd)** | % | % of correctly predicted command types (line, arc, extrude, fillet…) | DeepCAD, Text2CAD, CAD-GPT |
| **Parameter Accuracy (ACC_param)** | % | % of parameters within tolerance (η=3 out of 256 quantization levels) | DeepCAD, CAD-GPT |
| **F1 for CAD Elements** | 0–1 | F1 score on predicted CAD elements (features, constraints, operations) | Text2CAD |
| **Segmentation Error (SegE)** | Numeric | Topological segmentation accuracy of predicted face/edge structure | CAD-MLLM |
| **Flux Edge Error (FluxEE)** | Numeric | Consistency of edge flux in B-rep; detects topological inconsistencies | CAD-MLLM |

---

## Semantic Alignment (VLM / Human)

| Metric | Type | Description | Papers / Source |
|--------|------|-------------|-----------------|
| **VLM Geometry Score** | 0–10 | LLaVA / Gemini / GPT-4V rates rendered shape vs prompt — shape quality, feature count, distribution | CADFusion, Benchmark strategy |
| **Prompt Adherence Score** | 0–10 | Does the generated CAD match the text prompt? LLM-as-judge | Benchmark strategy |
| **Engineering Correctness** | 0–10 | Does it look like a real, manufacturable part? VLM/human judge | Benchmark strategy |
| **Feature Completeness** | Binary/% | Are all requested features present in the output? VLM-judged per feature | Benchmark strategy |
| **Visual Adherence** | % | Does rendered output look like what was requested? Human/VLM assessment | General across papers |
| **Human Preference Rate** | % | % of humans who prefer this output in pairwise comparison | FlexCAD, pairwise frameworks |
| **Specification Match** | % | % of specified requirements satisfied | CADCodeVerify |

---

## Efficiency

| Metric | Type | Description |
|--------|------|-------------|
| **Average Latency (s)** | Numeric | Mean time to generate CAD for one prompt (already implemented) |
| **Inference Speed** | Samples/s | Throughput: samples per second |
| **Total Attempts** | Integer | # of generation attempts (for self-correcting models; already tracked) |

---

## Arena / Ranking

| Metric | Type | Description |
|--------|------|-------------|
| **Elo Score** | Numeric | Bradley-Terry pairwise ranking — from head-to-head comparisons |
| **Win Rate** | % | % of pairwise comparisons won vs baseline |

---

## Gaps Identified in the Literature

The field currently lacks:

1. **A consensus quality metric** — analogous to FID for images, CLIP score for text
2. **Manufacturability metrics** — real DFM (Design for Manufacturability) constraints
3. **Parametric editability** — can you change a dimension and have the model update correctly?
4. **Constraint satisfaction** — perpendicularity, symmetry, concentricity maintained?
5. **Engineering intent** — does the design reflect good engineering practice beyond geometry?

---

## Implementation Priority

### v2 (near-term, no ground truth needed)
- Watertight check (trimesh)
- Self-intersection / non-degenerate mesh
- VLM geometry score (Claude Sonnet renders → judges 0-10)

### v3 (requires reference meshes)
- Chamfer Distance (median)
- IoU volumetric
- Hausdorff Distance
- Bounding box accuracy for prompts with explicit dimensions

### v4 (arena)
- Elo / win rate from pairwise human/VLM voting
- Human preference in "Try It" dynamic benchmark
