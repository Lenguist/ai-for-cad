# Assembly, Mechanism & Spatial Reasoning Papers
*Research sweep: 2020–2026. Compiled 2026-03-10.*

---

## Topic 1: LEGO Assembly, Design & Understanding

### 1.1 LEGO-Puzzles: How Good Are MLLMs at Multi-Step Spatial Reasoning?
- **Authors:** Kexian Tang, Junyao Gao, Yanhong Zeng, Haodong Duan, Yanan Sun, Zhening Xing, Wenran Liu, Kaifeng Lyu, Kai Chen
- **Year:** 2025
- **Venue:** arXiv:2503.19990 (cs.AI)
- **Summary:** Introduces a 1,100-sample visual QA benchmark across 11 LEGO-based spatial reasoning tasks. Tests 20 state-of-the-art MLLMs on sequential and spatial reasoning. Directly relevant as a benchmark exposing gaps in multi-step spatial intelligence.
- **Key findings:** Even the best models answer only ~50% of cases; human accuracy is >90%. Most models fail to transfer spatial reasoning to image generation tasks.

### 1.2 LEGO Co-builder: Exploring Fine-Grained Vision-Language Modeling for Multimodal LEGO Assembly Assistants
- **Authors:** Haochen Huang, Jiahuan Pei, Mohammad Aliannejadi, Xin Sun, Moonisa Ahsan, Chuang Yu, Zhaochun Ren, Pablo Cesar, Junxiao Wang
- **Year:** 2025
- **Venue:** arXiv:2507.05515
- **Summary:** Benchmark combining real LEGO assembly logic with programmatically generated multimodal scenes; evaluates GPT-4o, Gemini, and Qwen-VL on instruction-following and object detection in assembly contexts. Relevant as a direct VLM assembly evaluation.
- **Key findings:** Even GPT-4o achieves a maximum F1 of only 40.54% on state detection, revealing critical fine-grained assembly understanding gaps.

### 1.3 Translating a Visual LEGO Manual to a Machine-Executable Plan
- **Authors:** Ruocheng Wang, Yunzhi Zhang, Jiayuan Mao, Chin-Yi Cheng, Jiajun Wu
- **Year:** 2022
- **Venue:** ECCV 2022 — arXiv:2207.12572
- **Summary:** Presents MEPNet, which converts visual step-by-step LEGO assembly manuals into machine-executable 3D plans using neural keypoint detection and 2D-3D projection. Foundational work for instruction-to-assembly translation.
- **Key findings:** Outperforms baselines on three new LEGO datasets and a Minecraft house dataset; generalises to unseen components.

### 1.4 Budget-Aware Sequential Brick Assembly with Efficient Constraint Satisfaction
- **Authors:** Seokjun Ahn, Jungtaek Kim, Minsu Cho, Jaesik Park
- **Year:** 2022
- **Venue:** Transactions on Machine Learning Research (TMLR) — arXiv:2210.01021
- **Summary:** Develops a U-shaped sparse 3D CNN for predicting next brick positions during sequential LEGO assembly, with a constraint validation layer and support for budget-constrained scenarios. Relevant for automated LEGO structure generation.
- **Key findings:** Outperforms Bayesian optimisation, deep graph generative, and RL baselines on both constrained and unconstrained brick assembly.

### 1.5 Building LEGO Using Deep Generative Models of Graphs
- **Authors:** Rylee Thompson, Elahe Ghalebi, Terrance DeVries, Graham W. Taylor
- **Year:** 2020
- **Venue:** NeurIPS 2020 ML4eng Workshop — arXiv:2012.11543
- **Summary:** Proposes graph-structured generative neural networks trained on human LEGO designs to produce novel 3D LEGO structures. One of the earliest deep learning papers treating LEGO as a design generation testbed.
- **Key findings:** Model learns from human-built structures and produces novel designs with appealing visual qualities; open-sourced code.

### 1.6 ManualVLA: A Unified VLA Model for Chain-of-Thought Manual Generation and Robotic Manipulation
- **Authors:** Chenyang Gu, Jiaming Liu, Hao Chen, Runzhong Huang, Qingpo Wuwu, Zhuoyang Liu, Xiaoqi Li, Ying Li, Renrui Zhang, Peng Jia, Pheng-Ann Heng, Shanghang Zhang
- **Year:** 2025
- **Venue:** arXiv:2512.02013
- **Summary:** Vision-Language-Action framework that generates intermediate "manuals" (images, text, position prompts) as chain-of-thought to bridge high-level planning and robot execution. Evaluated on LEGO assembly and object rearrangement.
- **Key findings:** 32% higher success rate than prior hierarchical SOTA on LEGO assembly tasks. Uses 3D Gaussian Splatting digital-twin toolkit for training data.

### 1.7 Autonomous Workflow for Multimodal Fine-Grained Training Assistants Towards Mixed Reality (LEGO-MRTA)
- **Authors:** Jiahuan Pei, Irene Viola, Haochen Huang, Junxiao Wang, Moonisa Ahsan, Fanghua Ye, Jiang Yiming, Yao Sai, Di Wang, Zhumin Chen, Pengjie Ren, Pablo Cesar
- **Year:** 2024
- **Venue:** ACL 2024 — arXiv:2405.13034
- **Summary:** Introduces LEGO-MRTA, a multimodal fine-grained assembly dialogue dataset auto-synthesised by an LLM agent integrated with XR tools. Creates a benchmark for instruction-following and assembly Q&A in mixed reality settings.
- **Key findings:** Pipeline successfully auto-generates instruction manuals, conversations, and VQA pairs; multiple open-source LLMs benchmarked with and without fine-tuning on the dataset.

### 1.8 Large-Scale Multi-Robot Assembly Planning for Autonomous Manufacturing
- **Authors:** Kyle Brown, Dylan M. Asmar, Mac Schwager, Mykel J. Kochenderfer
- **Year:** 2023 (published Robotics and Autonomous Systems 2025)
- **Venue:** Robotics and Autonomous Systems, Vol. 194 — arXiv:2311.00192
- **Summary:** Full algorithmic stack for multi-robot autonomous manufacturing: facility layout, mixed-integer task allocation, collaborative carrying, and collision-free motion planning. Uses a LEGO Saturn V (1,845 parts) as the benchmark structure.
- **Key findings:** Plans generated for 1,845-part assembly with 250 robots in under 3 minutes on laptop hardware. Open-sourced simulator in Julia.

### 1.9 Show, Don't Tell: Evaluating LLMs Beyond Textual Understanding with ChildPlay (LEGO Connect Language)
- **Authors:** Gonçalo Hora de Carvalho, Oscar Knap, Robert Pollice
- **Year:** 2024
- **Venue:** arXiv:2407.11068 (cs.AI)
- **Summary:** Benchmark using ASCII-encoded games including the novel LEGO Connect Language (LCL) task to probe spatial logic and generalisation in GPT-3.5, GPT-4, GPT-4o, and GPT-4o-mini.
- **Key findings:** Models consistently struggle with LCL alongside Battleship and molecular graph tasks; only 4 of 7 tasks show systematic improvement with model capability.

---

## Topic 2: AI/LLM for Mechanical Assembly Planning

### 2.1 AssemMate: Graph-Based LLM for Robotic Assembly Assistance
- **Authors:** Qi Zheng, Chaoran Zhang, Zijian Liang, EnTe Lin, Shubo Cui, Qinghongbing Xie, Zhaobo Xu, Long Zeng
- **Year:** 2025
- **Venue:** arXiv:2509.11617 (cs.RO)
- **Summary:** Combines graph convolutional networks with LLMs for assembly knowledge graph Q&A, enabling robots to process assembly instructions more efficiently than text-based approaches. Relevant for part-library-based assembly planning.
- **Key findings:** 6.4% higher accuracy, 3× faster inference, and 28× context length reduction vs. text-based baselines; validated on real-world robotic grasping.

### 2.2 Manual2Skill: Learning to Read Manuals and Acquire Robotic Skills for Furniture Assembly
- **Authors:** Chenrui Tie, Shengxiang Sun, Jinxuan Zhu, Yiwei Liu, Jingxuan Guo, Yue Hu, Haonan Chen, Junting Chen, Ruihai Wu, Lin Shao
- **Year:** 2025
- **Venue:** arXiv:2502.10090 (cs.RO)
- **Summary:** VLM-based system that reads IKEA instruction manuals, constructs hierarchical assembly graphs, and executes furniture assembly using a robot arm. Demonstrates end-to-end instruction-to-action for real-world multi-part assembly.
- **Key findings:** Successfully demonstrated on real IKEA furniture in physical experiments; VLM extracts structured connector and part information from images.

### 2.3 Manual2Skill++: Connector-Aware General Robotic Assembly from Instruction Manuals
- **Authors:** Chenrui Tie, Shengxiang Sun, Yudi Lin, Yanbo Wang, Zhongrui Li, Zhouhan Zhong, Jinxuan Zhu, Yiman Pang, Haonan Chen, Junting Chen, Ruihai Wu, Lin Shao
- **Year:** 2025
- **Venue:** arXiv:2510.16344 (cs.RO)
- **Summary:** Extends Manual2Skill by treating connectors (bolts, clips, etc.) as first-class assembly primitives, using VLMs to extract structured connection info from manuals. Covers furniture, toys, and manufacturing components.
- **Key findings:** Dataset with 20+ assembly tasks; validated across four complex scenarios in simulation; handles diverse connector types systematically.

### 2.4 Robot-Enabled Construction Assembly with Automated Sequence Planning based on ChatGPT: RoboGPT
- **Authors:** Hengxu You, Yang Ye, Tianyu Zhou, Qi Zhu, Jing Du
- **Year:** 2023
- **Venue:** IEEE Access — arXiv:2304.11018
- **Summary:** Uses ChatGPT's reasoning capabilities for automated sequence planning in robot-based construction assembly, overcoming limitations of traditional mathematical and heuristic methods. One of the earliest papers applying LLMs to physical assembly sequencing.
- **Key findings:** 80 real-robot trials across two case studies; ChatGPT-driven robots handle complex construction and adapt to on-the-fly changes.

### 2.5 Behavior Tree Generation using LLMs for Sequential Manipulation Planning (ICRA 2024 Workshop)
- **Authors:** Jicong Ao, Yansong Wu, Fan Wu, Sami Haddadin
- **Year:** 2024
- **Venue:** ICRA 2024 Workshop — arXiv:2409.09435
- **Summary:** LLM-based behavior tree generation framework for sequential robotic assembly, accepting human instructions and runtime feedback. Tested on the Siemens Robot Assembly Challenge gear set with a tool-changing robot.
- **Key findings:** Evaluated on success rate, logical coherence, executability, and token/time cost; first framework combining LLM-generated BTs with real-hardware assembly.

### 2.6 LLM-as-BT-Planner: Leveraging LLMs for Behavior Tree Generation in Robot Task Planning
- **Authors:** Jicong Ao, Fan Wu, Yansong Wu, Abdalla Swikir, Sami Haddadin
- **Year:** 2024
- **Venue:** ICRA 2025 — arXiv:2409.10444
- **Summary:** Four in-context learning methods enabling LLMs to produce behavior trees for robotic assembly task planning; also fine-tunes smaller models. Reduces manual BT authoring effort while maintaining robustness.
- **Key findings:** Validates in both simulation and real-world environments; fine-tuned smaller LLMs show strong performance on assembly tasks.

### 2.7 From Perception to Symbolic Task Planning: VLM-Guided Human-Robot Collaborative Structured Assembly
- **Authors:** Yanyi Chen, Min Deng
- **Year:** 2026
- **Venue:** arXiv:2601.00978 (cs.RO)
- **Summary:** Two-module framework: Perception-to-Symbolic State (PSS) using VLMs to convert visual data to verifiable assembly states, plus Human-Aware Planning and Replanning (HPR) for adaptive multi-robot task allocation. Validated on a 27-component timber-frame task.
- **Key findings:** PSS achieves 97% state synthesis accuracy; HPR maintains feasible task progression across diverse human-robot collaboration scenarios.

### 2.8 IDfRA: Self-Verification for Iterative Design in Robotic Assembly
- **Authors:** Nishka Khendry, Christos Margadji, Sebastian W. Pattinson
- **Year:** 2025
- **Venue:** arXiv:2509.16998 (cs.RO)
- **Summary:** Iterative plan-execute-verify-replan cycle that uses the real world as feedback (no physics simulation) to progressively refine assembly designs for balance between semantic accuracy and physical feasibility.
- **Key findings:** 73.3% top-1 semantic accuracy, 86.9% construction success rate; design quality improves across iterations.

### 2.9 Blox-Net: Generative Design-for-Robot-Assembly Using VLM Supervision, Physics Simulation, and a Robot with Reset
- **Authors:** Andrew Goldberg, Kavish Kondap, Tianshuang Qiu, Zehan Ma, Letian Fu, Justin Kerr, Huang Huang, Kaiyuan Chen, Kuan Fang, Ken Goldberg
- **Year:** 2024
- **Venue:** arXiv:2409.17126 (cs.RO)
- **Summary:** Introduces Generative Design-for-Robot-Assembly (GDfRA): given a natural-language prompt and images of physical components, VLM generates an assembly design plus robotic instructions that must be physically assemblable by a 6-DOF arm.
- **Key findings:** 63.5% Top-1 recognisability; near-perfect consecutive assembly success after automated perturbation redesign; full prompt-to-physical-assembly pipeline without human intervention.

---

## Topic 3: AI for Mechanism Design (Linkages, Gears, Motion Conversion)

### 3.1 LInK: Learning Joint Representations of Design and Performance Spaces through Contrastive Learning for Mechanism Synthesis
- **Authors:** Amin Heyrani Nobari, Akash Srivastava, Dan Gutfreund, Kai Xu, Faez Ahmed
- **Year:** 2024
- **Venue:** Transactions on Machine Learning Research — arXiv:2405.20592
- **Summary:** Contrastive learning framework over a dataset of 10M+ planar linkage mechanisms that learns joint design/performance representations, enabling rapid candidate retrieval and hierarchical optimisation for path synthesis. Also introduces the LINK ABC benchmark (trajectory synthesis for capital letters).
- **Key findings:** 28× less error and 20× less time vs. SOTA on existing benchmarks; existing methods fail almost entirely on the new LINK ABC benchmark.

### 3.2 Deep Generative Model-based Synthesis of Four-bar Linkage Mechanisms with Target Conditions
- **Authors:** Sumin Lee, Jihoon Kim, Namwoo Kang
- **Year:** 2024
- **Venue:** Journal of Computational Design and Engineering, Vol. 11, Issue 5, pp. 318–332 — arXiv:2402.14882
- **Summary:** Conditional GAN for synthesising four-bar crank-rocker linkages that simultaneously satisfy kinematic workspace and quasi-static torque transmission requirements. Enables designers to explore large mechanism design spaces.
- **Key findings:** Outperforms cVAE and NSGA-II baselines on generating diverse, feasible, and constraint-satisfying mechanism candidates.

### 3.3 Data-Driven Dimensional Synthesis of Diverse Planar Four-bar Function Generation Mechanisms via Direct Parameterization
- **Authors:** Woon Ryong Kim, Jaeheun Jung, Jeong Un Ha, Donghun Lee, Jae Kyung Shim
- **Year:** 2025
- **Venue:** arXiv:2507.08269 (cs.LG)
- **Summary:** LSTM + Mixture-of-Experts neural network for solving inverse kinematics of planar four-bar mechanisms from desired motion specs; handles both single-type and multi-type linkage synthesis. Makes mechanism design accessible to non-experts.
- **Key findings:** Produces accurate, defect-free linkages across diverse configurations; novel simulation metric for evaluating predicted vs. desired motions.

### 3.4 INGRID: Intelligent Generative Robotic Design Using Large Language Models
- **Authors:** Guanglu Jia, Ceng Zhang, Gregory S. Chirikjian
- **Year:** 2025 (withdrawn for revision Oct 2025)
- **Venue:** arXiv:2509.03842 (cs.RO)
- **Summary:** Integrates LLMs with reciprocal screw theory and kinematic synthesis to automate parallel robotic mechanism design through four progressive subtasks (constraint analysis → joint generation → chain construction → mechanism design). Bridges formal mechanism theory with ML.
- **Key findings:** Generated novel parallel mechanisms including previously undocumented kinematic configurations; demonstrated across three case studies for task-specific parallel robots.

---

## Topic 4: Robot Assembly Planning with Part Libraries

### 4.1 Assembler: Scalable 3D Part Assembly via Anchor Point Diffusion
- **Authors:** Wang Zhao, Yan-Pei Cao, Jiale Xu, Yuejiang Dong, Ying Shan
- **Year:** 2025
- **Venue:** arXiv:2506.17074 (cs.CV)
- **Summary:** Diffusion-based generative framework for assembling 3D objects from individual part meshes and reference images, using sparse anchor point clouds rather than pose estimation. Built on a 320K+ part-object dataset.
- **Key findings:** SOTA on PartNet benchmark; first system demonstrated effectively on complex real-world objects; enables interactive compositional 3D modelling.

### 4.2 CRAG: Can 3D Generative Models Help 3D Assembly?
- **Authors:** Zeyu Jiang, Sihang Li, Siqi Tan, Chenyang Xu, Juexiao Zhang, Julia Galway-Witham, Xue Wang, Scott A. Williams, Radu Iovita, Chen Feng, Jing Zhang
- **Year:** 2026
- **Venue:** arXiv:2602.22629 (cs.CV)
- **Summary:** Reformulates 3D assembly as a joint assembly-and-generation problem: assembly provides part-level structural priors for generation, while generation resolves assembly ambiguities. Can synthesise missing geometry while predicting part poses.
- **Key findings:** SOTA results on diverse objects including those with missing parts; demonstrates that generation and assembly mutually reinforce each other.

### 4.3 From CAD to POMDP: Probabilistic Planning for Robotic Disassembly of End-of-Life Products
- **Authors:** Jan Baumgärtner, Malte Hansjosten, David Hald, Adrian Hauptmann, Alexander Puchta, Jürgen Fleischer
- **Year:** 2025
- **Venue:** arXiv:2511.23407 (cs.RO)
- **Summary:** Automatically generates POMDP models from CAD data and robot specs to handle uncertainty in disassembly of aged products; uses RL on stochastic action outcomes with Bayesian belief filtering over latent product conditions.
- **Key findings:** Outperforms deterministic baselines in speed, consistency, and adaptability across three products and two robotic systems.

### 4.4 The Shape Part Slot Machine: Contact-based Reasoning for Generating 3D Shapes from Parts
- **Authors:** Kai Wang, Paul Guerrero, Vladimir Kim, Siddhartha Chaudhuri, Minhyuk Sung, Daniel Ritchie
- **Year:** 2022
- **Venue:** ECCV 2022 — arXiv:2112.00584
- **Summary:** Represents shapes as "graphs of slots" (contact regions between parts) and assembles novel 3D shapes through contact-based reasoning without requiring semantic part labels. Relevant to general part-library assembly.
- **Key findings:** Generates diverse novel shapes by composing parts via learned contact slot compatibility.

### 4.5 Score-PA: Score-based 3D Part Assembly
- **Authors:** Junfeng Cheng, Mingdong Wu, Ruiyuan Zhang, Guanqi Zhan, Chao Wu, Hao Dong
- **Year:** 2023
- **Venue:** arXiv:2309.04220 (cs.CV)
- **Summary:** Score-based generative approach for assembling 3D parts into complete shapes; introduces Fast Predictor-Corrector Sampler to accelerate inference while maintaining assembly quality.
- **Key findings:** Demonstrates that generative score-based models are effective for the combinatorial 3D part assembly problem.

---

## Topic 5: Spatial Reasoning Benchmarks Involving Physical Assembly

### 5.1 PhyBlock: A Progressive Benchmark for Physical Understanding and Planning via 3D Block Assembly
- **Authors:** Liang Ma, Jiajun Wen, Min Lin, Rongtao Xu, Xiwen Liang, Bingqian Lin, Jun Ma, Yongxin Wang, Ziming Wei, Haokun Lin, Mingfei Han, Meng Cao, Bokui Chen, Ivan Laptev, Xiaodan Liang
- **Year:** 2025
- **Venue:** arXiv:2506.08708 (cs.RO)
- **Summary:** 2,600-task benchmark (400 assembly + 2,200 VQA) assessing VLMs on physical understanding through robotic 3D block assembly; evaluates partial completion, failure diagnosis, and planning robustness across 21 SOTA models.
- **Key findings:** All models show pronounced limitations in high-level planning; chain-of-thought prompting barely helps; persistent failures in spatial orientation and part dependency reasoning.

### 5.2 BuildArena: A Physics-Aligned Interactive Benchmark of LLMs for Engineering Construction
- **Authors:** Tian Xia, Tianrun Gao, Wenhao Deng, Long Wei, Xiaowei Qian, Chenglei Yu, Tailin Wu
- **Year:** 2025
- **Venue:** arXiv:2510.16559 (cs.AI) — project: build-arena.github.io
- **Summary:** First physics-aligned interactive benchmark evaluating 8 frontier LLMs on language-driven engineering construction under strict physical constraints; spans static and dynamic mechanics at multiple difficulty levels.
- **Key findings:** Establishes first systematic assessment of LLMs for physics-grounded construction automation; reveals significant gaps in constraint reasoning and spatial planning.

### 5.3 MineAnyBuild: Benchmarking Spatial Planning for Open-world AI Agents
- **Authors:** Ziming Wei, Bingqian Lin, Zijian Jiao, Yunshuang Nie, Liang Ma, Yuecheng Liu, Yuzheng Zhuang, Xiaodan Liang
- **Year:** 2025
- **Venue:** NeurIPS 2025 Datasets & Benchmarks Track — arXiv:2505.20148
- **Summary:** 4,000 Minecraft-based tasks requiring agents to generate executable building plans from multimodal instructions; evaluates spatial understanding, reasoning, creativity, and commonsense across MLLM agents.
- **Key findings:** Current MLLM agents show significant spatial planning limitations; benchmark uses player-generated content for extensibility.

### 5.4 Agentic Design of Compositional Machines (BesiegeField)
- **Authors:** Wenqian Zhang, Weiyang Liu, Zhen Liu
- **Year:** 2025
- **Venue:** arXiv:2510.14980 (cs.AI) — project: besiegefield.github.io
- **Summary:** Tests whether LLMs can design machines by assembling standardised components in the Besiege game simulation (physics-based). Benchmarks SOTA LLMs with agentic workflows on spatial reasoning, strategic assembly, and instruction-following.
- **Key findings:** Open-source models struggle significantly; RL fine-tuning shows promise. Identifies spatial reasoning and strategic planning as key bottlenecks.

### 5.5 Jigsaw++: Imagining Complete Shape Priors for Object Reassembly
- **Authors:** Jiaxin Lu, Gang Hua, Qixing Huang
- **Year:** 2025
- **Venue:** arXiv:2410.11816 (cs.CV)
- **Summary:** Generative method for 3D object reassembly that learns complete-shape priors to resolve ambiguities during part reassembly; uses a retargeting strategy to leverage outputs from existing assembly methods.
- **Key findings:** Improves reassembly accuracy by providing holistic shape context, complementing pose-based methods.

---

## Topic 6: LLMs on Engineering Design & Mechanism Reasoning

### 6.1 Toward Engineering AGI: Benchmarking the Engineering Design Capabilities of LLMs (EngDesign)
- **Authors:** Xingang Guo et al. (64 co-authors)
- **Year:** 2025
- **Venue:** NeurIPS 2025 Datasets & Benchmarks Track — arXiv:2509.16204
- **Summary:** Introduces EngDesign, a benchmark evaluating LLMs across 9 engineering disciplines (electrical, mechanical, aerospace, civil, computer, etc.) with simulation-based evaluation of functional design correctness — not just static answer checking.
- **Key findings:** Engineering design poses fundamentally different challenges than textbook problems; shifts evaluation paradigm from static answers to dynamic functional verification.

### 6.2 Engineering Reasoning and Instruction (ERI) Benchmark
- **Authors:** MZ Naser, Ahmad Bani Awwad, Zoie McCreery, Radwa Eissa, Ahmad Naser, Gianluca Cusatis, Andrew Metcalf, Kapil Madathil, Jamal Abdalla, Venkatesh Kodur, Mohammad Reza Saeb
- **Year:** 2026
- **Venue:** arXiv:2603.02239 (cs.AI)
- **Summary:** Taxonomy-driven instruction dataset of 57,750 records spanning 9 engineering fields and 55 subdomains across 7 intent types and 3 difficulty levels, designed for training and evaluating engineering-capable LLMs.
- **Key findings:** Frontier models (GPT-5, Claude Sonnet 4, DeepSeek V3.1) score >4.30/5.0; smaller and mid-tier models show high failure rates. Hallucination constrained to 1.7% via convergent validation.

### 6.3 A Multidisciplinary Design and Optimization (MDO) Agent Driven by Large Language Models
- **Authors:** Bingkun Guo, Wentian Li, Xiaojian Liu, Jiaqi Luo, Zibin Yu, Dalong Dong, Shuyou Zhang, Yiming Zhang
- **Year:** 2025
- **Venue:** arXiv:2511.17511 (cs.AI)
- **Summary:** LLM agent orchestrating natural-language-driven parametric modelling with RAG and engineering software integration for design verification and multidisciplinary optimisation workflows. Shows LLMs acting as design orchestrators.
- **Key findings:** Demonstrated feasibility of LLM-driven MDO; RAG bridges LLM general knowledge with domain-specific engineering software tools.

### 6.4 A Domain Adaptation of Large Language Models for Classifying Mechanical Assembly Components
- **Authors:** Fatemeh Elhambakhsh, Daniele Grandi, Hyunwoong Ko
- **Year:** 2025
- **Venue:** arXiv:2505.01627 (cs.CL)
- **Summary:** Fine-tunes LLMs for automated functional classification of mechanical assembly components, improving accuracy and consistency of part annotation in early-phase engineering design exploration.
- **Key findings:** Domain-adapted LLMs provide meaningful accuracy gains over general-purpose models for component classification in assembly contexts.

### 6.5 On the Evaluation of Engineering Artificial General Intelligence
- **Authors:** Sandeep Neema, Susmit Jha, Adam Nagel, Ethan Lew, Chandrasekar Sureshkumar, Aleksa Gordic, Chase Shimmin, Hieu Nguyen, Paul Eremenko
- **Year:** 2025
- **Venue:** arXiv:2505.10653
- **Summary:** Proposes an extensible evaluation framework grounding Bloom's taxonomy in engineering design, supporting evaluation of structured design artifacts including CAD models and SysML models. Directly relevant to benchmarking LLMs on engineering design tasks.
- **Key findings:** Taxonomy-grounded evaluation framework; covers both reasoning (recall/comprehension) and design synthesis (application/creation) levels.

### 6.6 BikeBench: A Bicycle Design Benchmark for Generative Models with Objectives and Constraints
- **Authors:** Lyle Regenwetter, Yazan Abu Obaideh, Fabien Chiotti, Ioanna Lykourentzou, Faez Ahmed
- **Year:** 2025
- **Venue:** arXiv:2508.00830
- **Summary:** Engineering design benchmark evaluating generative models on multi-physics bicycle design with quantified human-centred and physics performance characteristics. Tests models on objective/constraint satisfaction in a constrained mechanical design domain.
- **Key findings:** Diverse input representations evaluated; establishes multi-objective design benchmark for engineering generative models.

### 6.7 Human-in-the-Loop: Quantitative Evaluation of 3D Models Generated by Large Language Models
- **Authors:** Ahmed R. Sadik, Mariusz Bujny
- **Year:** 2025
- **Venue:** arXiv:2509.07010
- **Summary:** Evaluation framework for LLM-generated CAD/3D models using volumetric accuracy, surface alignment, and complexity metrics with human-in-the-loop validation. Provides methodology for benchmarking LLM-generated engineering geometry.
- **Key findings:** Introduces a comprehensive similarity and complexity metric suite; highlights gap between LLM textual competence and 3D geometric accuracy.

---

## Additional Cross-Cutting Papers

### A.1 NovaPlan: Zero-Shot Long-Horizon Manipulation via Closed-Loop Video Language Planning
- **Authors:** Jiahui Fu, Junyu Nan, Lingfeng Sun, Hongyu Li, Jianing Qian, Jennifer L. Barry, Kris Kitani, George Konidaris
- **Year:** 2026
- **Venue:** arXiv:2602.20119 (cs.RO)
- **Summary:** Combines VLM planning with video generation and geometric grounding for zero-shot robotic assembly without demonstrations; relevant to long-horizon assembly planning.
- **Key findings:** Demonstrates closed-loop feedback between video generation and physical execution for zero-shot assembly task completion.

### A.2 Replanning Human-Robot Collaborative Tasks with Vision-Language Models via Semantic and Physical Dual-Correction
- **Authors:** Taichi Kato, Takuya Kiyokawa, Namiko Saito, Kensuke Harada
- **Year:** 2026
- **Venue:** arXiv:2602.14551 (cs.RO)
- **Summary:** Internal correction model for logical consistency plus external correction for physical failures in HRC assembly tasks; addresses dynamic replanning when assembly states deviate from plan.
- **Key findings:** Dual-correction architecture improves robustness of human-robot collaborative assembly tasks.

### A.3 COALESCE: Component Assembly by Learning to Synthesize Connections
- **Authors:** Kangxue Yin, Zhiqin Chen, Siddhartha Chaudhuri, Matthew Fisher, Vladimir G. Kim, Hao Zhang
- **Year:** 2020
- **Venue:** ECCV 2020 — arXiv:2008.01936
- **Summary:** First data-driven deep learning framework for component-based 3D shape assembly that handles geometric and topological mismatches by learning to synthesise connecting geometry (joints). Foundational for part-library-based assembly.
- **Key findings:** Successfully assembles diverse shape parts including those with geometric mismatch; learned joint synthesis enables novel shape creation.

---

*Notes: Papers marked withdrawn (INGRID) were included for their conceptual contribution. Rate limits on arXiv prevented exhaustive follow-up searches on topics like gear synthesis, disassembly planning, and construction sequence optimisation — further targeted searches are recommended.*
