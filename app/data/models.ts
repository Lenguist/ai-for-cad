export type ModelType = "academic" | "commercial" | "baseline";

export interface Model {
  slug: string;
  name: string;
  year: string;
  venue: string;
  type: ModelType;
  input: string;
  output: string;
  note: string;
  description?: string;
  links?: {
    paper?: string;
    github?: string;
    project?: string;
    website?: string;
  };
}

export const MODELS: Model[] = [
  {
    slug: "text2cad",
    name: "Text2CAD",
    year: "2024",
    venue: "NeurIPS Spotlight",
    type: "academic",
    input: "Text",
    output: "CAD sequences",
    note: "170K models, 4 abstraction levels",
    description:
      "Text2CAD generates parametric CAD models from natural language descriptions using a transformer trained on the DeepCAD dataset. The model maps text prompts at four abstraction levels (basic shape, part-level, feature-level, dimension-level) to sketch-extrude sequences. NeurIPS 2024 Spotlight.",
    links: {
      project: "https://sadilkhan.github.io/text2cad-project/",
      github: "https://github.com/SadilKhan/Text2CAD",
    },
  },
  {
    slug: "flexcad",
    name: "FlexCAD",
    year: "2025",
    venue: "ICLR",
    type: "academic",
    input: "Text / multi-cond",
    output: "CAD sequences",
    note: "Unified controllable generation",
    description:
      "FlexCAD introduces a unified framework for controllable CAD generation under multiple conditioning signals — text, partial geometry, sketch, and more. Accepted at ICLR 2025.",
  },
  {
    slug: "cad-coder",
    name: "CAD-Coder",
    year: "2025",
    venue: "arXiv",
    type: "academic",
    input: "Text",
    output: "CAD code",
    note: "Chain-of-thought + geometric reward RL",
    description:
      "CAD-Coder uses chain-of-thought prompting and reinforcement learning with geometric rewards to generate executable CAD code from text. The geometric reward signal directly penalizes invalid or non-manifold geometry.",
  },
  {
    slug: "text-to-cadquery",
    name: "Text-to-CadQuery",
    year: "2025",
    venue: "arXiv",
    type: "academic",
    input: "Text",
    output: "CadQuery Python",
    note: "Self-correction: 53% → 85% exec success",
    description:
      "Trains models (124M–7B parameters) to generate executable CadQuery Python from natural language. Introduces a self-correction loop that revises code when it fails to execute, raising success rate from 53% to 85%. Dataset of ~170K text-CadQuery pairs derived from DeepCAD.",
    links: {
      paper: "https://arxiv.org/html/2505.06507v1",
    },
  },
  {
    slug: "cadfusion",
    name: "CADFusion",
    year: "2025",
    venue: "arXiv",
    type: "academic",
    input: "Text + visual feedback",
    output: "CadQuery",
    note: "Iterative visual refinement loop",
    description:
      "CADFusion augments text-to-CAD generation with an iterative visual feedback loop. After each generation, the rendered output is evaluated against the prompt using a VLM, and the model refines the code. Shows significant improvement on complex multi-feature parts.",
  },
  {
    slug: "cad-gpt",
    name: "CAD-GPT",
    year: "2025",
    venue: "arXiv",
    type: "academic",
    input: "Text + image",
    output: "CAD sequences",
    note: "Spatial reasoning multimodal LLM",
    description:
      "CAD-GPT is a multimodal LLM fine-tuned to generate CAD construction sequences from both text and image inputs. Focuses on spatial reasoning — understanding 3D relationships from 2D projections.",
    links: {
      project: "https://openiwin.github.io/CAD-GPT/",
      paper: "https://arxiv.org/abs/2412.19663",
    },
  },
  {
    slug: "deepcad",
    name: "DeepCAD",
    year: "2021",
    venue: "ICCV",
    type: "academic",
    input: "Unconditional",
    output: "CAD sequences",
    note: "Foundational baseline — 178K models",
    description:
      "DeepCAD is the foundational generative model for parametric CAD sequences. Trained on 178K models from the ABC dataset, it established the sketch-extrude sequence representation that most subsequent work builds on. ICCV 2021.",
  },
  {
    slug: "zoo",
    name: "Zoo / ML-ephant",
    year: "2025",
    venue: "zoo.dev",
    type: "commercial",
    input: "Text",
    output: "STEP / STL / OBJ",
    note: "$30M+ funded, public API",
    description:
      "Zoo (formerly KittyCAD) provides the ML-ephant API for text-to-CAD generation. Returns STEP, STL, and OBJ files. The most polished commercial API with open-source tooling. $30M+ funded.",
    links: {
      website: "https://zoo.dev/machine-learning-api",
    },
  },
  {
    slug: "adamcad",
    name: "AdamCAD",
    year: "2025",
    venue: "YC W25",
    type: "commercial",
    input: "Text",
    output: "STEP",
    note: "$4.1M seed, mech. engineering focus",
    description:
      "AdamCAD is a YC W25 company building text-to-CAD specifically for mechanical engineering. $4.1M seed. Focuses on manufacturable, dimensionally accurate outputs rather than visual fidelity.",
    links: {
      website: "https://adamcad.ai",
    },
  },
  {
    slug: "cadgpt",
    name: "CADGPT",
    year: "2025",
    venue: "cadgpt.ai",
    type: "commercial",
    input: "Text",
    output: "STEP",
    note: "Commercial text-to-CAD API",
    description:
      "CADGPT is a commercial text-to-CAD service producing STEP files from natural language prompts.",
    links: {
      website: "https://cadgpt.ai",
    },
  },
  {
    slug: "gpt4o-zeroshot",
    name: "GPT-4o (zero-shot)",
    year: "2024",
    venue: "OpenAI",
    type: "baseline",
    input: "Text",
    output: "OpenSCAD / CadQuery",
    note: "93% invalid rate (Text2CAD eval)",
    description:
      "GPT-4o prompted zero-shot to generate CadQuery or OpenSCAD code. The Text2CAD paper reports a 93% invalidity rate, establishing it as a weak baseline. Used here as a reference point for general-purpose LLM capability without CAD-specific training.",
  },
  {
    slug: "claude-zeroshot",
    name: "Claude Sonnet (zero-shot)",
    year: "2025",
    venue: "Anthropic",
    type: "baseline",
    input: "Text",
    output: "CadQuery",
    note: "Strong code model — untested on CAD",
    description:
      "Claude Sonnet prompted zero-shot to generate CadQuery. Strong general code generation capability but no CAD-specific training. Included as a baseline to assess how far general coding ability transfers to parametric CAD.",
  },
  {
    slug: "gemini-zeroshot",
    name: "Gemini 2.0 (zero-shot)",
    year: "2025",
    venue: "Google",
    type: "baseline",
    input: "Text",
    output: "CadQuery",
    note: "85% compile rate on CADPrompt",
    description:
      "Gemini 2.0 prompted zero-shot on the CADPrompt benchmark achieves 85% compile rate. Included as a second general-purpose LLM baseline alongside GPT-4o and Claude.",
  },
];

export const TYPE_STYLES = {
  academic: {
    bg: "rgba(255,255,255,0.12)",
    color: "rgba(255,255,255,0.9)",
    label: "Academic",
  },
  commercial: {
    bg: "rgba(255,255,255,0.12)",
    color: "rgba(255,255,255,0.9)",
    label: "Commercial",
  },
  baseline: {
    bg: "rgba(255,255,255,0.12)",
    color: "rgba(255,255,255,0.9)",
    label: "LLM Baseline",
  },
};
