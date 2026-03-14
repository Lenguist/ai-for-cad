# LEGO Datasets Research

_Last updated: 2026-03-10_

---

## 1. LEGO Set & Parts Databases

### 1.1 Rebrickable Full Database Download

- **URL:** https://rebrickable.com/downloads/
- **What it is:** The canonical, continuously updated relational database of every official LEGO set, part, color, theme, and inventory. Widely used as the industry-standard reference.
- **Contents:**
  - `sets.csv` — all LEGO sets (set number, name, year, theme, num_parts)
  - `parts.csv` — all LEGO parts (part number, name, category)
  - `colors.csv` — all LEGO colors with RGB hex values
  - `inventories.csv` + `inventory_parts.csv` — which parts/quantities are in each set
  - `themes.csv` — hierarchical theme tree
  - `part_relationships.csv` — mold variants, alternates, print relationships
  - `minifigs.csv` + `inventory_minifigs.csv` — minifigure catalog and set inclusion
  - `elements.csv` — (part, color) combinations with LEGO element IDs
- **Format:** CSV
- **Size:** ~3–10 MB total (exact size changes as data is updated); ~20,000 sets, ~80,000 parts as of 2025
- **License:** CC BY (free to use with attribution)
- **How to download:** Directly from https://rebrickable.com/downloads/ — no login required. Also accessible via Rebrickable REST API v3 (https://rebrickable.com/api/v3/docs/).
- **Relevance:** Best starting point for set-level and part-level metadata. Does NOT include 3D geometry or instruction PDFs — just relational data.

---

### 1.2 Kaggle: LEGO Database (Rebrickable snapshot)

- **URL:** https://www.kaggle.com/datasets/rtatman/lego-database
- **What it is:** A July 2017 snapshot of the Rebrickable database packaged for Kaggle. Contains the same tables as above.
- **Format:** CSV (zipped)
- **Size:** ~3 MB
- **Downloads:** 41,500+ (very popular for data analysis courses)
- **License:** CC0 (Public Domain)
- **Note:** Stale (2017). Use direct Rebrickable downloads for current data.

---

### 1.3 LEGO Official Building Instructions

- **URL:** https://www.lego.com/en-us/service/buildinginstructions
- **What it is:** LEGO's official portal for set instruction PDFs. Covers thousands of current and past sets.
- **Format:** PDF (not structured/machine-readable)
- **Scale:** Thousands of instruction booklets — likely 5,000–15,000+ sets. LEGO has released ~20,000 official sets since 1949, though not all have digitized PDFs.
- **Access:** Free, browser-based search by set number or name. No bulk download API.
- **License:** LEGO Group copyright. Permitted for personal use; not licensed for redistribution or dataset creation.
- **AI relevance:** Raw PDFs — no structured step data. Would require CV parsing (see Section 3). Very useful as a source if you build a scraper + parser.

---

## 2. HuggingFace Datasets

### 2.1 AvaLovelace/StableText2Brick (BrickGPT training data)

- **URL:** https://huggingface.co/datasets/AvaLovelace/StableText2Brick
- **What it is:** The training/evaluation dataset for BrickGPT (aka LegoGPT). 47,389 LEGO-like brick structures paired with text captions, sourced from ShapeNet 3D objects voxelized and brick-fitted.
- **Format:** Parquet; each record is:
  - `structure_id` (string)
  - `object_id` — ShapeNet shape ID
  - `category_id` — ShapeNet category (21 categories: car, chair, table, etc.)
  - `captions` — list of 5 text descriptions per structure
  - `bricks` — custom text format: one line per brick, `HxW (x,y,z)`, all within a 20×20×20 grid
  - `stability_scores` — 20×20×20 array of float64 voxel stability values
- **Size:** 44.3 MB on disk; 47,389 rows (42,600 train / 4,789 test)
- **Unique 3D objects:** 28,000+
- **License:** MIT
- **How to download:** `datasets.load_dataset("AvaLovelace/StableText2Brick")`
- **Relevance:** High — first large-scale text-to-LEGO dataset with physical stability guarantees. NOT LDraw format (custom grid encoding). Only 21 object categories.

---

### 2.2 pvrancx/legobricks

- **URL:** https://huggingface.co/datasets/pvrancx/legobricks
- **What it is:** 400,000 rendered images of LEGO parts for image classification. The 1,000 most common LEGO part IDs from Rebrickable, rendered at multiple angles and colors using the LDraw rendering engine.
- **Format:** Parquet (images as ImageObjects)
- **Size:** 13.2 GB
- **Scale:** 400 images × 1,000 part classes = 400,000 images
- **Images per class:** 400 (varied rotations, weighted colors from Rebrickable frequency data)
- **Resolution:** 1200×1200 px
- **License:** Apache 2.0
- **How to download:** `datasets.load_dataset("pvrancx/legobricks")`
- **Relevance:** Part recognition / classification. Not useful for set-level or assembly-level tasks.

---

### 2.3 Norod78/lego-blip-captions-512

- **URL:** https://huggingface.co/datasets/Norod78/lego-blip-captions-512
- **What it is:** 2,511 LEGO images scraped from the web, auto-captioned with BLIP. Used for fine-tuning diffusion models.
- **Format:** Parquet (image + text)
- **Size:** 625 MB; 2,511 rows
- **Resolution:** 512×512 px
- **License:** Not specified
- **Relevance:** Low — no structure data, just image-caption pairs.

---

### 2.4 lukasHoel/lego_diffuse_1000

- **URL:** https://huggingface.co/datasets/lukasHoel/lego_diffuse_1000
- **What it is:** 1,000 LEGO images for diffusion model training. Minimal documentation.
- **Format:** Parquet
- **Size:** 451 MB
- **License:** Not specified
- **Relevance:** Low.

---

### 2.5 merve/lego_sets_latest

- **URL:** https://huggingface.co/datasets/merve/lego_sets_latest
- **What it is:** 61 images of LEGO sets with BLIP-2 generated captions. Used for DreamBooth fine-tuning of SDXL.
- **Format:** imagefolder → Parquet (119 MB)
- **License:** Apache 2.0
- **Relevance:** Negligible — 61 samples.

---

### 2.6 lerobot/koch_pick_place_1_lego_raph

- **URL:** https://huggingface.co/datasets/lerobot/koch_pick_place_1_lego_raph
- **What it is:** A robotics demonstration dataset (33,000 frames) of a robot arm picking and placing LEGO bricks. Part of the LeRobot robotics imitation learning ecosystem.
- **Format:** Parquet + video frames
- **Size:** 33k rows
- **Relevance:** Robotics manipulation, not LEGO structure/design.

---

## 3. Research Papers on LEGO Instruction Parsing

### 3.1 "Translating a Visual LEGO Manual to a Machine-Executable Plan" (MEPNet)

- **Paper:** arXiv:2207.12572 — ECCV 2022
- **Authors:** Ruocheng Wang, Yunzhi Zhang, Jiayuan Mao, Chin-Yi Cheng, Jiajun Wu (Stanford)
- **Project page:** https://cs.stanford.edu/~rcwang/projects/lego_manual
- **What it does:** Converts step-by-step LEGO assembly manual images into machine-executable instruction sequences. Uses neural 2D keypoint detection + 2D-3D projection.
- **Dataset:** "Three newly collected LEGO manual datasets and a Minecraft house dataset." Paper claims datasets were newly collected for the work.
- **Format:** Images of instruction pages + paired structural annotations
- **Size:** Not specified in abstract; appears to be relatively small (dozens to hundreds of models)
- **Public availability:** Unclear — project page may have data. Authors at Stanford.
- **Relevance:** High for instruction parsing research. This is one of the first papers to tackle LEGO manual → executable plan conversion end-to-end.

---

### 3.2 "Break and Make: Interactive Structural Understanding Using LEGO Bricks" + LTRON

- **Paper:** arXiv:2207.13738 — ECCV 2022
- **Authors:** Walsman, Zhang, Kotar, Desingh, Farhadi, Fox
- **GitHub (LTRON):** https://github.com/aaronwalsman/ltron
- **What it is:** LTRON is a fully interactive 3D LEGO simulator. The accompanying LEGO dataset consists of fan-made LDraw models sourced from the LDraw Open Model Repository (OMR) and community-contributed designs.
- **Dataset scale:** "Over a thousand unique brick shapes" — several hundred to ~1,000 distinct LEGO models
- **Format:** LDraw (.ldr / .mpd / .dat files). LTRON converts to OBJ for rendering.
- **How to download:** `pip install ltron` then `ltron_asset_installer` (downloads ~3 GB to `~/.cache/ltron`)
- **License:** Community LDraw files (open licensing); LTRON code is research code
- **Relevance:** High — first simulator for interactive assembly AI. Dataset is real LDraw fan models, not synthetic.

---

### 3.3 "Learning to Build by Building Your Own Instructions" (Break-and-Make v2)

- **Paper:** arXiv:2410.01111 — Oct 2024
- **Authors:** Aaron Walsman, Muru Zhang, Adam Fishman, Ali Farhadi, Dieter Fox
- **What it does:** Agent learns to reconstruct LEGO assemblies by disassembling them and capturing step-by-step instruction images.
- **Dataset:** Procedurally generated LEGO vehicles; average 31 bricks; >100 assembly/disassembly steps each.
- **Public availability:** Not confirmed in abstract.
- **Relevance:** Useful framing for instruction generation rather than parsing.

---

### 3.4 "LEGO-Puzzles: How Good Are MLLMs at Multi-Step Spatial Reasoning?"

- **Paper:** arXiv:2503.19990 — Mar 2025
- **Authors:** Kexian Tang, Junyao Gao, Yanhong Zeng et al.
- **What it is:** Benchmark of 1,100 VQA samples testing spatial + sequential reasoning in multimodal LLMs using LEGO-based visual puzzles.
- **Dataset:** 1,100 samples across 11 tasks (basic spatial understanding → complex multi-step reasoning)
- **Key finding:** SOTA MLLMs ~50% accuracy; humans >90%
- **Public availability:** Paper not confirmed released; contact authors.
- **Relevance:** Evaluation benchmark for spatial reasoning, not a training dataset.

---

### 3.5 "LEGO Co-builder: Exploring Fine-Grained Vision-Language Modeling for Multimodal LEGO Assembly Assistants"

- **Paper:** arXiv:2507.05515 — 2025
- **Authors:** Haochen Huang, Jiahuan Pei, Mohammad Aliannejadi et al.
- **What it does:** Hybrid benchmark combining real-world LEGO assembly logic with programmatically generated multimodal scenes. Evaluates instruction following, object detection, state detection.
- **Dataset:** Benchmark with stepwise visual states + procedural instructions (exact count not in abstract)
- **Code/data:** Authors say released; check paper page.
- **Relevance:** Most complete multimodal LEGO assembly benchmark as of 2025.

---

### 3.6 "Building LEGO Using Deep Generative Models of Graphs"

- **Paper:** arXiv:2012.11543 — Dec 2020
- **GitHub:** https://github.com/uoguelph-mlrg/GenerativeLEGO
- **What it does:** Graph-based generative model trained on human-built LEGO structures.
- **Dataset:** Uses data from Kim et al. "Combinatorial 3D Shape Generation via Sequential Assembly" (POSTECH). Auto-downloaded by `python extract_dataset.py` from https://github.com/POSTECH-CVLab/Combinatorial-3D-Shape-Generation
- **Format:** 3D voxel / graph representations of LEGO structures (converted from their original format)
- **License:** MIT (code); dataset license unclear
- **Relevance:** Moderate — graph-level generation, earlier work.

---

### 3.7 "Budget-Aware Sequential Brick Assembly with Efficient Constraint Satisfaction"

- **Paper:** arXiv:2210.01021 — 2022
- **Authors:** Seokjun Ahn, Jungtaek Kim, Minsu Cho, Jaesik Park (POSTECH)
- **What it does:** Generates LEGO-like 3D structures sequentially under budget constraints using sparse 3D CNNs.
- **Dataset:** POSTECH Combinatorial 3D Shape Generation dataset (same as above)
- **Format:** 3D voxel grids
- **Relevance:** Sequential assembly generation.

---

### 3.8 "Image2Lego: Customized LEGO Set Generation from Images"

- **Paper:** arXiv:2108.08477 — Aug 2021
- **Authors:** Lennon, Fransen, O'Brien et al. (Drori lab)
- **What it does:** Generates LEGO brick models from 2D photos using an octree-structured autoencoder trained on 3D voxelized models. Produces step-by-step building instructions.
- **Dataset:** 3D voxelized models (likely from ShapeNet or similar) converted to LEGO representation. Specific dataset name not stated in abstract.
- **Relevance:** Image-to-LEGO generation.

---

## 4. 3D LEGO Structure Datasets

### 4.1 StableText2Brick (BrickGPT / "LegoGPT")

_(See Section 2.1 for full detail)_

- **GitHub:** https://github.com/AvaLovelace1/BrickGPT (1,600+ stars as of May 2025)
- **Paper:** arXiv:2505.05469 — May 2025
- **Model:** BrickGPT (autoregressive LLM with physics-aware rollback)
- **Dataset:** 47,389 structures, 28,000+ unique ShapeNet objects, 21 categories
- **Outputs LDraw files:** Yes — `.ldr` format compatible with LDraw viewers
- **Note:** Despite being called "LegoGPT" on the project page, the system is officially named BrickGPT in the paper.

---

### 4.2 LDraw Parts Library + Official Model Repository (OMR)

- **URL:** https://www.ldraw.org / https://omr.ldraw.org
- **What it is:** The de facto open standard for digital LEGO models since 1995. Two components:
  1. **Parts Library:** ~18,000+ individual LEGO part definitions as `.dat` files (geometric primitives)
  2. **Official Model Repository (OMR):** Community-built complete set models in `.ldr` / `.mpd` format — several hundred official LEGO set recreations
- **Format:** LDraw text format — human-readable ASCII describing triangles, primitives, subfile references
- **License:** Creative Commons Attribution 2.0 (parts library); individual model files may vary
- **How to download:**
  - Parts library: Available from LDraw.org download page as a zip (~30 MB)
  - OMR: https://omr.ldraw.org — browse and download individual set `.mpd` files
- **Used by:** LTRON (arXiv:2207.13738), BrickGPT (for visualization), LeoCAD, BrickLink Studio
- **Relevance:** Gold standard for 3D LEGO structure representation. Any serious LEGO AI work uses or references LDraw.

---

### 4.3 POSTECH Combinatorial 3D Shape Generation Dataset

- **GitHub:** https://github.com/POSTECH-CVLab/Combinatorial-3D-Shape-Generation
- **Paper:** "Combinatorial 3D Shape Generation via Sequential Assembly" (Kim et al., Apr 2020)
- **What it is:** Dataset of 3D structures built from LEGO-like unit bricks. Includes 11 object categories (bars, lines, plates, walls, cuboids, pyramids, chairs, sofas, cups, hollow structures, tables, cars).
- **Format:** Stored in the repository as part of the code; voxel/graph structure (not LDraw)
- **License:** MIT (code)
- **Used by:** GenerativeLEGO (arXiv:2012.11543), Budget-Aware Assembly (arXiv:2210.01021)
- **Relevance:** Foundational dataset for generative LEGO-brick assembly research.

---

### 4.4 Rebrickable MOC Database

- **URL:** https://rebrickable.com/mocs/
- **What it is:** Crowd-sourced database of user-designed LEGO MOCs (My Own Creations). Primarily part lists + building instructions.
- **Scale:** Tens of thousands of MOC designs
- **Format:** Part lists (CSV via API); some include LDraw files or PDF instructions as designer uploads
- **Access:** Rebrickable API v3 (`/api/v3/lego/mocs/`) returns metadata; downloadable files are per-design
- **License:** Varies by designer; most are shared for personal use
- **Relevance:** Large crowdsourced design corpus but not in a unified downloadable 3D format.

---

### 4.5 BrickLink Catalog

- **URL:** https://www.bricklink.com/catalogList.asp
- **What it is:** The most comprehensive LEGO parts and sets marketplace database. Includes set inventories, part images, color names, and secondary market prices.
- **Format:** Web-accessible only (BrickLink XML format for shopping lists; no bulk CSV download officially)
- **Scale:** ~20,000+ sets, 85,000+ parts/molds
- **API:** BrickLink API available but requires OAuth; rate-limited
- **License:** Terms prohibit scraping/bulk redistribution
- **Relevance:** Best for part images and set metadata. Not an open bulk dataset.

---

## 5. Visual LEGO Part Recognition Datasets (Kaggle)

### 5.1 Kaggle: Images of LEGO Bricks (Hazelzet)

- **URL:** https://www.kaggle.com/datasets/joosthazelzet/lego-brick-images
- **What it is:** 40,000 rendered images of 50 LEGO brick types (800 angles each). Created with Autodesk Maya 2020.
- **Format:** ZIP (~1.07 GB); RGB images
- **License:** GPL 2.0
- **Classes:** 50 part types
- **Relevance:** Part classification. Small part selection.

---

## 6. Key Resources Not Directly Accessible

### 6.1 LEGO's Official Instruction PDFs (Bulk)

LEGO provides individual PDF instruction downloads at lego.com but there is no official bulk dataset. The full collection spans thousands of sets dating back decades. Several community efforts have partially scraped this:
- **Brickset** (https://brickset.com) tracks which sets have instructions and links them
- Community archivists have assembled partial mirrors but no public unified dataset exists
- LEGO's legal terms restrict redistribution

### 6.2 LEGO MRTA Dataset (2024)

- **Paper:** Pei, Viola, Huang et al. (2024) — "Multimodal fine-grained assembly dialogue dataset with instruction manuals, conversations, and VQA"
- Exact arXiv ID not confirmed; contact authors for access.

---

## 7. Summary Table

| Dataset | Type | Scale | Format | License | Download |
|---|---|---|---|---|---|
| **Rebrickable DB** | Sets/parts metadata | ~20k sets, ~80k parts | CSV | CC BY | https://rebrickable.com/downloads/ |
| **Kaggle LEGO DB** | Sets/parts metadata (2017) | ~11k sets | CSV | CC0 | Kaggle |
| **StableText2Brick** | 3D brick structures + captions | 47,389 structures | Custom text + Parquet | MIT | HuggingFace: AvaLovelace/StableText2Brick |
| **pvrancx/legobricks** | Part images (rendered) | 400k images, 1000 classes | Parquet | Apache 2.0 | HuggingFace: pvrancx/legobricks |
| **LTRON dataset** | 3D LDraw models (community) | ~1,000+ models | LDraw (.ldr/.mpd) | Open (fan content) | `pip install ltron && ltron_asset_installer` (~3 GB) |
| **LDraw Parts Library** | 3D part geometry | ~18,000+ parts | LDraw (.dat) | CC BY 2.0 | ldraw.org downloads (~30 MB) |
| **LDraw OMR** | 3D set models | Several hundred sets | LDraw (.mpd) | Mixed CC | omr.ldraw.org |
| **POSTECH Assembly** | 3D brick structures | 11 categories | Voxel/graph | MIT | github.com/POSTECH-CVLab/Combinatorial-3D-Shape-Generation |
| **Norod78 BLIP Captions** | LEGO images + captions | 2,511 images | Parquet | Unspecified | HuggingFace: Norod78/lego-blip-captions-512 |
| **Kaggle Brick Images** | Part images (rendered) | 40k images, 50 classes | ZIP/JPG | GPL 2.0 | Kaggle: joosthazelzet/lego-brick-images |
| **LEGO Official PDFs** | Instruction manuals | Thousands of sets | PDF | LEGO copyright | lego.com/service/buildinginstructions |
| **MEPNet datasets** | Instruction manual images | Small (dozens of sets?) | Images + annotations | Research | cs.stanford.edu/~rcwang (check paper) |
| **LEGO-Puzzles** | VQA benchmark | 1,100 samples | Images + Q&A | Research | arXiv:2503.19990 (check paper) |
| **LEGO Co-builder** | Assembly VQA benchmark | Not specified | Multimodal | Released by authors | arXiv:2507.05515 (check paper) |
| **Rebrickable MOC DB** | Crowdsourced designs | Tens of thousands | Part lists (API) | Varies | Rebrickable API |

---

## 8. Relevance to AI Benchmark for LEGO

**Most directly relevant for a text-to-LEGO benchmark:**
1. **StableText2Brick** — only dataset directly pairing text descriptions with LEGO structures; MIT license; downloadable
2. **LTRON + LDraw OMR** — real LDraw models for evaluation; ~1,000 diverse structures
3. **Rebrickable DB** — set metadata for context/prompts; completely open

**For instruction-following / manual parsing:**
- MEPNet (arXiv:2207.12572) is the most serious attempt at LEGO instruction → plan translation
- LEGO Co-builder (2025) is the most recent benchmark

**Key gap:** No large-scale publicly available dataset of complete LEGO set LDraw files paired with their official building instructions as structured step data. The LTRON dataset is the closest (1,000 fan models in LDraw format) but not from official sets.
