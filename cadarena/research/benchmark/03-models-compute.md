# Text-to-CAD Models: Compute Requirements & Reproducibility
*Researched: 2026-03-03*

---

## Quick Reference Table

| Model | Params | Base LLM | VRAM | Weights? | Self-host? | Input | Output |
|-------|--------|----------|------|----------|------------|-------|--------|
| Text2CAD | ~363M | BERT-Large + custom decoder | 8–16GB | YES | YES | Text | CAD seq |
| FlexCAD | 8B | LLaMA-3-8B | 16–24GB | YES | YES | Text / masked CAD | CAD seq |
| CAD-Coder (NeurIPS, text) | 7B | Qwen2.5-7B-Instruct | 14–16GB | **NO** | NO | Text | CadQuery |
| CAD-Coder (VLM, image) | ~13B | LLaVA 1.5 / Vicuna-13B | 26–32GB | YES | YES | Image | CadQuery |
| Text-to-CadQuery (best) | 3B | Qwen2.5-3B | 8GB | YES | YES | Text | CadQuery |
| CADFusion | 8B | LLaMA-3-8B | 16–24GB | YES | YES | Text | CAD seq |
| CAD-GPT | ~7B | LLaVA-1.5 / Vicuna-7B | 14–16GB | **NO** | NO | Text + Image | CAD seq |
| DeepCAD | ~50–100M | None (custom) | 4–8GB | YES | YES | Unconditional | CAD seq |
| CAD-Llama | 8B | LLaMA-3-8B | 16–24GB | **NO** | NO | Text | SPCC code |
| CAD-Recode | ~1.5B | Qwen2-1.5B | 6–8GB | YES | YES | Point cloud | CadQuery |
| ReCAD | 7B | Qwen2.5-VL-7B | 14–18GB | **NO** | NO | Text + Image | CAD seq |
| CAD-MLLM | ~7B | Vicuna-7B | 16–20GB | **NO** | NO | Text/Image/PC | CAD seq |
| Zoo ML-ephant | — | Proprietary | API | NO | NO | Text | KCL + B-Rep |

**Immediately runnable (weights + code today): Text2CAD, FlexCAD, CAD-Coder (VLM), Text-to-CadQuery, CADFusion, DeepCAD, CAD-Recode — 7 models.**

**Blocked (no public weights): CAD-GPT, CAD-Coder (NeurIPS text), CAD-Llama, ReCAD, CAD-MLLM — 5 models.**

---

## Detailed Model Profiles

### 1. Text2CAD (NeurIPS 2024 Spotlight)
- **GitHub**: https://github.com/SadilKhan/Text2CAD
- **Architecture**: BERT-Large (340M) text encoder + 23M custom autoregressive decoder = ~363M total
- **Weights**: `SadilKhan/Text2CAD` on HuggingFace (`.pth` checkpoint in dataset repo)
- **VRAM**: Trained on 1× A100-80GB; inference fits in 8–16GB
- **Run**: `python test_user_input.py --prompt "..."`
- **Dependencies**: Python ≥3.9, conda env from `environment.yml`, HuggingFace datasets
- **Reproducibility**: Excellent. Dataset (170K models, 660K prompts), weights, inference script all available.

---

### 2. FlexCAD (ICLR 2025)
- **GitHub**: https://github.com/microsoft/FlexCAD
- **HuggingFace**: `microsoft/FlexCAD`
- **Architecture**: LLaMA-3-8B + LoRA (rank 8, alpha 32); 0.042% trainable params
- **VRAM**: 16–24GB; 8-bit quant → ~10GB
- **Inference speed**: **0.56 sec/sample** on A6000
- **Training hardware**: 4× NVIDIA A6000
- **Run**: `python sample.py --mask_type unconditional`
- **Dependencies**: `accelerate`, `transformers`, conda from `environments.yaml`
- **License**: Research-only (Microsoft)
- **Reproducibility**: Excellent. Note: must download LLaMA-3 base weights separately.

---

### 3a. CAD-Coder — NeurIPS 2025 text model (arXiv 2505.19713)
- **Architecture**: Qwen2.5-7B-Instruct fine-tuned with GRPO (geometric reward = Chamfer Distance)
- **Weights**: **NOT RELEASED** as of March 2026
- **Training**: 8× A800-80GB, SFT: 7h, GRPO: 146h
- **Dependencies**: vLLM, DeepSpeed ZeRO Stage 2
- **Status**: 🔴 Not reproducible — contact authors

---

### 3b. CAD-Coder — VLM image-to-CAD (arXiv 2505.14646)
- **GitHub**: https://github.com/anniedoris/CAD-Coder
- **HuggingFace**: `CADCODER/CAD-Coder` (13B, updated July 2025)
- **Architecture**: LLaVA 1.5 / Vicuna-13B + CLIP-ViT-L-336px
- **VRAM**: 26–32GB
- **Training hardware**: 4× H100-80GB; Stage 1: 4.5h, Stage 2: 5.7h
- **Input**: Image (not text) — takes CAD part photos
- **Dependencies**: `peft==0.10.0`, `flash-attention`, `datasets`, `tensorboard`
- **Note**: Different paper and different use case from 3a. Input is image not text.
- **Reproducibility**: Good (weights released).

---

### 4. Text-to-CadQuery (arXiv 2025)
- **GitHub**: https://github.com/Text-to-CadQuery/Text-to-CadQuery
- **HuggingFace**: `ricemonster/*` (fine-tuned model checkpoints)
- **Architecture**: Benchmark of 6 fine-tuned LLMs. Best model: **Qwen2.5-3B** (outperforms 7B Mistral)
- **Models evaluated**: CodeGPT-small (124M) · GPT-2-medium (355M) · GPT-2-large (774M) · Gemma3-1B · Qwen2.5-3B · Mistral-7B
- **VRAM**: 8GB for Qwen2.5-3B (recommended)
- **Training hardware**: 1–2× A100-80GB; Qwen2.5-3B trains in ~5h
- **Dependencies**: `cadquery` (Python), Blender (for rendering evaluation)
- **Reproducibility**: Good. 170K text-CadQuery pairs (extends Text2CAD dataset).

---

### 5. CADFusion (arXiv 2025)
- **GitHub**: https://github.com/microsoft/CADFusion
- **HuggingFace**: `microsoft/CADFusion` (v1.0 and v1.1)
- **Architecture**: LLaMA-3-8B + LoRA (rank 32, alpha 32); trained with Sequential Learning + DPO visual feedback
- **VRAM**: 16–24GB
- **v1.1** reportedly better than paper version (9 rounds vs 5)
- **Run**: `bash generate_samples.sh`
- **Dependencies**: `accelerate`, `transformers`, **`pythonocc-core==7.7.0`**, `chamfer_distance`
- **License**: MIT
- **Reproducibility**: Excellent. Two weight versions, full training code.

---

### 6. CAD-GPT (AAAI 2025)
- **GitHub**: https://github.com/SiyuWang0906/CAD-GPT (near-empty, 3 files)
- **HuggingFace**: `Ysjtu/CAD-GPT` (dataset only, no model weights)
- **Architecture**: LLaVA-1.5-7B + custom 3D Spatial Unfolding Mechanism
- **Weights**: **NOT RELEASED** — "will release code in the near future" (stated June 2025, still not out)
- **Training hardware**: 4× NVIDIA A800, 96h
- **Status**: 🔴 Not reproducible — blocked since AAAI 2025.

---

### 7. DeepCAD (ICCV 2021) — Baseline
- **GitHub**: https://github.com/ChrisWu1997/DeepCAD
- **Architecture**: Custom Transformer autoencoder + latent GAN (no LLM)
- **Weights**: `http://www.cs.columbia.edu/cg/deepcad/pretrained.tar`
- **VRAM**: ~4–8GB (2021-era model)
- **Dependencies**: Python 3.7, PyTorch ≥1.5, **`pythonocc-core==7.5.1`** (conda-forge), Linux+GPU
- **Note**: Unconditional/shape-conditioned, not text-to-CAD. Use as a quality baseline only.
- **Reproducibility**: Excellent (oldest, most battle-tested).

---

### 8. CAD-Llama (CVPR 2025)
- **Architecture**: LLaMA-3-8B fine-tuned in 2 stages (full FT pretraining → LoRA rank 256 instruction tuning)
- **Output format**: SPCC (Structured Parametric CAD Code) — Python-like pseudo-code
- **Weights**: **NOT RELEASED** — no GitHub repo, no HuggingFace
- **Training hardware**: 4× A100; 50h total
- **Status**: 🔴 Not reproducible.

---

### 9. CAD-Recode (ICCV 2025) ⭐ Most accessible
- **GitHub**: https://github.com/filaPro/cad-recode
- **HuggingFace weights v1**: `filapro/cad-recode`
- **HuggingFace weights v1.5**: `filapro/cad-recode-v1.5`
- **HuggingFace Space (live demo)**: https://huggingface.co/spaces/filapro/cad-recode (ZeroGPU)
- **Architecture**: Qwen2-1.5B + single linear layer for point cloud projection
- **VRAM**: ~6–8GB — **lowest VRAM in this list**
- **Input**: Point cloud (not text) — relevant for scan-to-CAD track
- **License**: CC-BY-NC-4.0
- **Reproducibility**: Excellent. Live demo, two weight versions, `demo.ipynb`.

---

### 10. ReCAD (AAAI 2026 Oral)
- **Architecture**: Qwen2.5-VL-7B-Instruct + GRPO reinforcement learning (veRL framework)
- **Weights**: **NOT RELEASED**
- **Training hardware**: 8× NVIDIA A800-80GB
- **Status**: 🔴 Not reproducible — AAAI 2026 oral, no code/weights release.

---

### 11. CAD-MLLM (arXiv 2024)
- **GitHub**: https://github.com/CAD-MLLM/CAD-MLLM
- **Architecture**: Vicuna-7B + DINOv2 vision encoder + Michelangelo point cloud encoder
- **VRAM**: 16–20GB; Training: 16× H800-80GB, 47h
- **Status**: 🟡 Dataset + eval code released (Omni-CAD on HuggingFace). **Model weights NOT released.** Repo README lists inference code as "TODO".
- **Most flexible input**: text, single/multi-view images, point clouds, or any combination.

---

### 12. Zoo / ML-ephant (Commercial API)
- **API**: https://zoo.dev/machine-learning-api
- **Web demo**: https://zoo.dev/text-to-cad
- **Pricing**: $0.0083/sec (~$0.08–$0.25/call); first $10 free (~20 min of generation)
- **Output**: KCL (KittyCAD Language) code + B-Rep CAD model; exports to STEP, STL, OBJ
- **Speed**: "Large majority of calls last 10–30 seconds"
- **Architecture**: Proprietary (closed source, internal fine-tune)
- **Self-hostable**: NO — geometry engine is proprietary
- **Reproducibility**: API-only, non-reproducible in research sense

---

## Key Observations

### Output format divergence — major evaluation challenge
| Format | Models |
|--------|--------|
| DeepCAD command sequences | Text2CAD, FlexCAD, CADFusion, DeepCAD, CAD-GPT, ReCAD, CAD-MLLM |
| CadQuery Python | CAD-Recode, Text-to-CadQuery, CAD-Coder (NeurIPS), CAD-Coder (VLM) |
| SPCC pseudo-code | CAD-Llama |
| KCL (proprietary) | Zoo ML-ephant |

You need a separate evaluation pipeline per output format. CadQuery is the easiest to evaluate (execute and measure with `cadquery` Python library).

### Minimum hardware for full self-hosted evaluation
- All 7 runnable models fit on a single **A100-80GB** or **2× A6000** (48GB total)
- CAD-Recode + Text-to-CadQuery (3B) fit on a **single 16GB GPU** (RTX 3090/4080)
- Cloud cost estimate for one full benchmark run (7 models × ~200 prompts):
  - A100-80GB on Lambda Labs: ~$1.29/hr
  - Estimated 4–6 hours per model = ~$5–8 per model = **~$35–55 total** for the 7 runnable models

### LLM baselines (zero-shot, API cost)
- GPT-4o: ~$0.005/1K input tokens; ~200 prompts × ~200 tokens = **~$0.20 total** — negligible
- Claude Sonnet: similar pricing
- Gemini 2.0 Flash: cheapest, ~$0.00015/1K tokens

---

## HuggingFace Weights Summary

| Model | HF ID | Available |
|-------|-------|-----------|
| Text2CAD | `SadilKhan/Text2CAD` (dataset repo) | ✅ |
| FlexCAD | `microsoft/FlexCAD` | ✅ |
| CAD-Coder VLM | `CADCODER/CAD-Coder` | ✅ |
| Text-to-CadQuery | `ricemonster/*` | ✅ |
| CADFusion | `microsoft/CADFusion` | ✅ |
| CAD-Recode v1 | `filapro/cad-recode` | ✅ |
| CAD-Recode v1.5 | `filapro/cad-recode-v1.5` | ✅ |
| CAD-GPT | `Ysjtu/CAD-GPT` (dataset only) | ❌ |
| CAD-MLLM | — | ❌ |
| CAD-Llama | — | ❌ |
| ReCAD | — | ❌ |
| CAD-Coder NeurIPS | — | ❌ |
