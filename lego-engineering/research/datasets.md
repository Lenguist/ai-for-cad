# LEGO Datasets Research

---

## 1. LEGO Set & Parts Databases

### Rebrickable
**URL:** https://rebrickable.com/downloads/
**License:** CC BY
**Format:** CSV, updated daily

The canonical open-source LEGO database. ~20,000 sets, ~80,000 parts, continuously updated. Direct bulk CSV download, no scraping needed.

- `sets.csv`, `parts.csv`, `inventory_parts.csv`, `colors.csv`, `part_relationships.csv`
- Also available via REST API (rate-limited — use CSVs for bulk work)

### Kaggle LEGO Database
**URL:** https://www.kaggle.com/datasets/rtatman/lego-database
**License:** CC0
**Size:** ~3 MB

Stale 2017 snapshot of Rebrickable data. Useful for offline work but outdated — use Rebrickable directly for current data.

### LEGO Official Instructions
**URL:** https://www.lego.com/service/buildinginstructions
**License:** Copyright LEGO Group — not freely redistributable

Individual PDFs accessible per set. No bulk download API. Content is copyright-restricted. Not usable as training data without licensing.

---

## 2. HuggingFace Datasets

| Dataset | Description | Size | License |
|---|---|---|---|
| **AvaLovelace/StableText2Brick** | 47,389 LEGO structures + 5 captions each — BrickGPT/LegoGPT training data | 44 MB | MIT |
| **pvrancx/legobricks** | 400k rendered part images, 1,000 part classes | 13.2 GB | Apache 2.0 |
| Norod78/lego-blip-captions-512 | 2,511 scraped LEGO photos + BLIP captions | 625 MB | unspecified |
| lukasHoel/lego_diffuse_1000 | 1,000 LEGO images for diffusion training | 451 MB | unspecified |

**Most important:** `AvaLovelace/StableText2Brick` — this is the training data behind BrickGPT/LegoGPT (CMU, 2025). 47k structures derived by voxelizing ShapeNet 3D meshes and applying brick layouts. Custom grid format (not LDraw), but outputs can be converted to `.ldr`.

---

## 3. 3D LEGO Structure Datasets

### LDraw Parts Library
**URL:** https://library.ldraw.org/library/updates/complete.zip
**License:** CC BY 2.0
**Size:** ~30 MB

~18,000+ part definitions in `.dat` format. Gold standard for LEGO part geometry. Not a dataset of *assemblies* — individual parts only.

### LDraw OMR (Official Model Repository)
**URL:** https://omr.ldraw.org
**License:** varies (community-built)

Several hundred official LEGO set models in `.mpd` format, community-reconstructed from real sets. Closest thing to a structured dataset of complete official set models in LDraw format.

### LTRON Dataset
**Paper:** arXiv:2207.13738 (ECCV 2022)
**Download:** `pip install ltron && ltron_asset_installer`
**Size:** ~3 GB (LDraw files)

~1,000 real fan-built LDraw models from various categories. Used in the LTRON interactive 3D LEGO simulation environment paper. Fully public and downloadable. **Best available dataset of complete LDraw assemblies.**

### POSTECH Combinatorial-3D-Shape-Generation
**GitHub:** https://github.com/POSTECH-CVLab/Combinatorial-3D-Shape-Generation
**License:** MIT

Voxel/graph brick structures across 11 object categories. Used by multiple academic papers on LEGO generation. Not LDraw format — voxel/graph representation.

---

## 4. Key Research Datasets (from Papers)

### StableText2Brick (BrickGPT/LegoGPT, CMU 2025)
**HuggingFace:** AvaLovelace/StableText2Brick
**Paper:** arXiv:2505.05469

47,389 structures derived from ShapeNet 3D meshes → voxelized → brick layouts applied → filtered for physical stability via physics sim. Each structure has 5 text captions. Custom grid format. This is the current state-of-the-art training set for text-to-LEGO.

### MEPNet Datasets (Stanford, ECCV 2022)
**Paper:** arXiv:2207.12572

Three LEGO instruction manual datasets collected to train MEPNet (translates manual images → executable assembly plans). Not yet confirmed as public release.

### LEGO-Puzzles Benchmark (2025)
**Paper:** arXiv:2503.19990

1,100 VQA samples across 11 spatial reasoning task types. Tests multi-step assembly reasoning from images. Evaluation benchmark, not training data.

---

## 5. Key Gap

**No publicly available large-scale dataset pairs complete official LEGO set LDraw files with structured step-by-step building instruction data.**

- Official instructions: copyright-restricted PDFs, no structured format
- LDraw OMR: has models but not step-by-step instruction sequences at scale
- LTRON: ~1,000 fan models in LDraw — best available but small
- StableText2Brick: 47k structures but synthetically generated (not real sets), no mechanism designs

For a Technic mechanism benchmark specifically, **no existing dataset** covers functional mechanism assemblies with ground truth motion/function labels.

---

## 6. Recommended Datasets for Benchmark

| Dataset | Use |
|---|---|
| AvaLovelace/StableText2Brick | Baseline comparison; understand prior work format |
| LTRON dataset (~1k LDraw) | Source of real assembly examples |
| Rebrickable CSV | Part/set inventory ground truth |
| LDraw OMR | Official set reconstructions for reference |
| LDraw Parts Library | Part geometry for all assembly validation |
