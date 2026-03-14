# AI for CAD / AI for Mechanical Engineering -- Companies & Startups

**Compiled: February 8, 2026**
**Last Updated with Live Web Search Data: February 8, 2026**

> This document catalogs companies and startups working at the intersection of AI and computer-aided design (CAD) / mechanical engineering. It merges researcher knowledge with confirmed findings from live web searches covering 2024-2026 data.

---

## Summary Statistics

| Category | Count | Combined Funding (Est.) |
|---|---|---|
| Pure-play AI-for-CAD startups | 18 | ~$300M+ |
| Established CAD/engineering companies with AI | 12 | Public companies; combined market cap $300B+ |
| Adjacent companies (manufacturing, simulation, 3D generation) | 30 | ~$5B+ |
| **Total unique companies cataloged** | **60** | -- |

| Notable Trends (2025-2026) | |
|---|---|
| Largest single new investment | Project Prometheus -- $6.2B (Bezos/Bajaj, 2025) |
| Biggest incumbent move | Autodesk Neural CAD -- foundation models for geometry (AU 2025) |
| Most notable YC entrant | Adam AI (YC W25) -- text-to-CAD for mechanical engineering |
| Key acquisition activity | Katalyst Labs acquired by Rubix LS; Altair acquired Gen3D; nTop acquired Cloudfluid |
| Open source momentum | CADAM (Adam AI), ScadLM, CQAsk -- open source text-to-CAD tools emerging |
| Pricing innovation | Zoo freemium model: 40 free min/month, then $0.50/min |

---

## 1. Pure-Play AI-for-CAD Startups

Companies whose primary product is AI + CAD generation, modeling, or design automation.

---

### Project Prometheus
- **Website:** Not yet public
- **Founded:** 2025
- **Founders:** Jeff Bezos and Vik Bajaj
- **Funding:** $6.2B (2025) -- the largest investment in AI-for-engineering to date
- **Employees:** 100+ recruited from Meta, OpenAI, DeepMind
- **Product/Service:** "Physical AI" platform for engineering and manufacturing. Aims to build AI systems that can design and optimize physical products across computers, automotive, and aerospace sectors.
- **AI + CAD Relevance:** Directly targets the application of AI foundation models to physical product engineering and manufacturing. The scale of funding and talent signals a major bet that AI will transform how physical products are designed.
- **Key Differentiator:** Unprecedented funding scale ($6.2B), world-class AI talent pool from leading labs, and backing by Jeff Bezos. Positioned to be the most well-resourced entrant in AI-for-engineering.

---

### Zoo (formerly KittyCAD)
- **Website:** https://zoo.dev
- **Founded:** 2021
- **Funding:** $28M Series A (2023, Okta Ventures, Fuel Capital). Total raised ~$30M+. Backed by Sequoia Capital, Venrex, and GitHub co-founders. *(Updated 2025-2026)*
- **Pricing:** Freemium model -- 40 free minutes/month, then $0.50/min. *(Confirmed 2025-2026)*
- **Product/Service:** Text-to-CAD engine and API-first CAD platform. Offers "Zoo Modeling App" (a full CAD environment built from scratch in Rust) plus API endpoints that allow developers to generate 3D CAD geometry from text prompts, convert between CAD formats, and programmatically manipulate models. Open-source CAD kernel.
- **AI + CAD Relevance:** The most prominent pure-play "text-to-CAD" startup. Their ML models generate STEP/BREP geometry from natural language descriptions. Also building a full infrastructure layer (CAD engine, file conversion APIs) for the next generation of AI-native CAD tools.
- **Key Differentiator:** API-first approach, open-source CAD kernel written in Rust, purpose-built for AI integration rather than retrofitting AI onto legacy CAD. Now backed by top-tier investors including Sequoia Capital.

---

### Adam AI
- **Website:** https://adam.new
- **Founded:** 2025
- **Founders:** Zach Dive and Aaron Li (San Francisco)
- **Funding:** $4.1M seed (October 2025)
- **Accelerator:** Y Combinator W25 batch
- **Open Source:** CADAM -- open source text-to-CAD. GitHub: https://github.com/Adam-CAD/CADAM
- **Product/Service:** AI-powered CAD platform with text-to-3D generation, focused specifically on mechanical engineering applications. Plans to integrate with Onshape for seamless workflow with existing CAD tools.
- **AI + CAD Relevance:** Direct text-to-CAD generation for mechanical engineering parts. One of the first YC-backed startups explicitly targeting AI + mechanical CAD. Open-source CADAM project lowers the barrier to entry for AI-CAD experimentation.
- **Key Differentiator:** YC W25 pedigree, mechanical engineering focus (not general 3D), planned Onshape integration, and open-source CADAM project for community development.

---

### Vizcom
- **Website:** https://www.vizcom.ai
- **Founded:** 2021
- **Funding:** $20M+ total (Series A in 2023 led by a16z, seed from Y Combinator)
- **Product/Service:** AI-powered industrial design rendering tool. Transforms rough sketches and concepts into photorealistic product renderings in real time. Used by industrial designers and product designers.
- **AI + CAD Relevance:** Sketch-to-rendering for product/industrial design. Bridges the concept design phase to downstream CAD. Accelerates the front end of the mechanical design workflow.
- **Key Differentiator:** Real-time sketch-to-render AI specifically for industrial/product design (not general art). YC-backed, a16z Series A.

---

### Katalyst Labs
- **Website:** https://katalyst-labs.com
- **Founded:** ~2024
- **Funding:** Acquired by Rubix LS *(Confirmed 2025-2026)*
- **Product/Service:** Open-source AI copilot for hardware design. Generates parametric, context-aware designs from text prompts. Focuses on producing editable, parametric CAD output rather than static meshes.
- **AI + CAD Relevance:** Directly generates parametric CAD from text with context awareness. Open-source approach enables community contribution and adoption.
- **Key Differentiator:** Open-source AI copilot specifically for hardware design with parametric output. Acquired by Rubix LS, indicating strategic value in the design-to-manufacturing chain.

---

### Tripo AI
- **Website:** https://tripo3d.ai
- **Founded:** 2024
- **Funding:** Undisclosed
- **Product/Service:** AI platform for text-to-CAD generation. Launched a Text-to-CAD API for programmatic access. Targets gaming, animation, architecture, and product design verticals.
- **AI + CAD Relevance:** Text-to-CAD generation platform with API access, enabling integration into existing workflows and tools. Broad vertical targeting across multiple design disciplines.
- **Key Differentiator:** Dedicated Text-to-CAD API for developers and integrators. Multi-vertical approach spanning gaming, animation, architecture, and product design.

---

### Leo AI
- **Website:** https://getleo.ai
- **Founded:** ~2024
- **Funding:** Undisclosed
- **Product/Service:** Engineering-grade AI for leading engineering firms. AI CAD copilot that integrates into professional engineering workflows.
- **AI + CAD Relevance:** AI copilot specifically designed for professional engineering CAD workflows, targeting established engineering firms rather than individual users.
- **Key Differentiator:** "Engineering-grade" positioning targeting large engineering firms, suggesting enterprise-quality output and integration.

---

### MecAgent
- **Website:** https://mecagent.com
- **Founded:** ~2024
- **Funding:** Undisclosed
- **Product/Service:** AI CAD software copilot focused specifically on mechanical design workflows. Provides intelligent assistance for mechanical engineers using CAD tools.
- **AI + CAD Relevance:** Directly targets mechanical CAD workflows with AI copilot functionality. Narrow focus on mechanical engineering rather than general CAD.
- **Key Differentiator:** Exclusive focus on mechanical design workflows, as opposed to broader CAD or 3D generation.

---

### Hyperganic
- **Website:** https://www.hyperganic.com
- **Founded:** 2016 (Munich, Germany)
- **Funding:** $13M+ (Series A, 2021)
- **Product/Service:** AI-driven engineering design platform. Algorithmic engineering that uses AI to generate complex 3D geometries optimized for manufacturing (especially additive manufacturing). Targets aerospace, automotive, and industrial applications.
- **AI + CAD Relevance:** Core AI-for-engineering-design company. Generates manufacturable 3D parts using AI/algorithmic methods. Strong focus on lattice structures, heat exchangers, and other complex geometries.
- **Key Differentiator:** Voxel-based AI design kernel purpose-built for additive manufacturing. Deep engineering focus rather than general 3D.

---

### Physna (now Thangs)
- **Website:** https://thangs.com / https://physna.com
- **Founded:** 2016
- **Funding:** $30M+ total (Series A in 2021). Investors include Drive Capital, Sequoia Scout.
- **Product/Service:** Geometric deep learning platform for 3D models. Core technology analyzes 3D geometry at the geometric/topological level. Consumer-facing product "Thangs" is a 3D model search engine. Enterprise product provides 3D model search, comparison, and analysis for engineering teams.
- **AI + CAD Relevance:** AI-powered geometric search and analysis of CAD models. Enables finding similar parts, detecting IP infringement in 3D models, and analyzing CAD libraries.
- **Key Differentiator:** Geometric deep learning that understands 3D shape at a fundamental level (not just visual similarity). Massive 3D model database.

---

### Transcad AI
- **Website:** https://transcad.ai (unverified)
- **Founded:** ~2024
- **Funding:** Pre-seed / early stage
- **Product/Service:** AI copilot for CAD engineers. Integrates with existing CAD tools to provide intelligent suggestions, automate repetitive modeling tasks, and generate geometry from specifications.
- **AI + CAD Relevance:** Direct CAD workflow integration with AI assistance.
- **Key Differentiator:** Copilot model that augments existing CAD tools rather than replacing them.

---

### Sloyd
- **Website:** https://www.sloyd.ai
- **Founded:** 2021
- **Funding:** $3.4M seed (2022)
- **Product/Service:** AI-powered 3D asset generation. Uses procedural generation combined with AI to create 3D models from text prompts. Primarily game/creative assets but extending to product design.
- **AI + CAD Relevance:** Text-to-3D generation with parametric editing capabilities.
- **Key Differentiator:** Parametric/procedural approach to AI 3D generation (editable outputs, not just static meshes).

---

### Kaedim
- **Website:** https://www.kaedim.com
- **Founded:** 2020
- **Funding:** $15M+ total (Series A 2023)
- **Product/Service:** AI platform that converts 2D images into 3D models. Primarily targets gaming, e-commerce, and product visualization.
- **AI + CAD Relevance:** Image-to-3D pipeline. While primarily creative/e-commerce focused, the technology is adjacent to image-to-CAD reconstruction.
- **Key Differentiator:** Production-quality 3D model generation from single images.

---

### Hayden AI (Hayden Labs -- "Text2CAD")
- **Website:** https://www.haydenai.com (Note: verify -- there is a separate Hayden AI in mobility/transit)
- **Founded:** ~2023
- **Funding:** Undisclosed seed
- **Product/Service:** Text-to-CAD generation tooling, focused on converting natural language descriptions into parametric 3D models.
- **AI + CAD Relevance:** Directly targets the text-to-CAD pipeline.
- **Key Differentiator:** Focus on parametric/editable output rather than mesh-only generation.

---

### Wove
- **Website:** https://www.wove.com
- **Founded:** ~2022
- **Funding:** Undisclosed seed/early stage
- **Product/Service:** AI-powered collaboration platform for hardware product development. Combines design, engineering, and project management with AI assistance.
- **AI + CAD Relevance:** AI for hardware product design workflows, including integration with CAD tools.
- **Key Differentiator:** Focus on the full hardware product development lifecycle, not just the CAD step.

---

### Bild AI
- **Website:** https://bild.ai (unverified)
- **Founded:** ~2023
- **Funding:** Early stage
- **Product/Service:** AI for architectural and engineering design, with capabilities in generating 3D models from requirements.
- **AI + CAD Relevance:** AI-driven 3D design generation for architecture and engineering.
- **Key Differentiator:** Cross-domain approach spanning architecture and mechanical design.

---

### ScadLM (Open Source)
- **Website / Repository:** https://github.com/KrishKrosh/ScadLM
- **Founded:** ~2024 (open source project)
- **Funding:** Open source / community
- **Product/Service:** Open source agentic AI CAD generation built on OpenSCAD. Uses LLMs to generate parametric OpenSCAD code from natural language descriptions.
- **AI + CAD Relevance:** Directly generates parametric CAD code (OpenSCAD) from text using agentic AI. Fully open source.
- **Key Differentiator:** Built on OpenSCAD (widely used open-source parametric CAD), agentic approach, fully open source.

---

### CQAsk (Open Source)
- **Website / Repository:** https://github.com/OpenOrion/CQAsk
- **Founded:** ~2024 (open source project)
- **Funding:** Open source / community
- **Product/Service:** Open source LLM-powered CAD generation tool using CadQuery. Generates engineering-grade CAD models from natural language via CadQuery Python scripts.
- **AI + CAD Relevance:** LLM-to-CAD generation using CadQuery, which produces STEP/BREP output suitable for engineering workflows. Open source.
- **Key Differentiator:** Uses CadQuery (which produces real BREP/STEP geometry, not meshes), open source, Python-based for easy extensibility.

---

## 2. Established CAD/Engineering Companies with AI

Large incumbents and established software vendors that have added or are developing significant AI capabilities.

---

### Autodesk (with Neural CAD)
- **Website:** https://www.autodesk.com
- **Founded:** 1982
- **Public company** (NASDAQ: ADSK), Market cap ~$50B+
- **AI Products/Features:**
  - **Autodesk Neural CAD** *(NEW -- Announced AU 2025):* New foundation model category for geometry generation. Two models: one for product geometry (integrated with Fusion), one for buildings (integrated with Forma). Accepts text, sketch, and image inputs to generate CAD geometry. Autodesk claims it can automate 80-90% of routine design tasks.
  - **Fusion 360 Generative Design:** Flagship AI feature since ~2018. Define constraints, loads, materials, and manufacturing methods; AI explores thousands of design alternatives.
  - **Autodesk AI:** Umbrella branding for AI features across product line (2024+).
  - **Forma (formerly Spacemaker):** AI for architectural/urban design (acquired 2020 for ~$240M).
  - **AutoCAD AI assistant:** Natural language features for drawing commands.
  - **Project Bernini:** Research project for AI-generated 3D geometry.
- **AI + CAD Relevance:** The largest CAD company with the most mature generative design product. Neural CAD (2025) represents a major step: dedicated foundation models for geometry generation, not just generative design optimization. This is Autodesk's direct answer to the text-to-CAD startup wave.
- **Key Differentiator:** Scale, installed base, integrated manufacturing/simulation workflow. Neural CAD puts them in the foundation model race alongside startups.

---

### Siemens Digital Industries Software (NX / Teamcenter)
- **Website:** https://www.sw.siemens.com
- **Founded:** Siemens SW division includes former UGS (acquired 2007), Mentor Graphics (2017), Altair (2024).
- **Division of Siemens AG** (public, market cap ~$150B+)
- **AI Products/Features:**
  - **NX with AI-driven design:** AI-powered design suggestions, automated feature recognition, intelligent modeling.
  - **Simcenter with AI/ML:** ML for simulation acceleration, reduced-order models, surrogate modeling.
  - **Teamcenter AI:** AI for PLM data management, search, and knowledge mining.
  - **Siemens Industrial Copilot:** Partnership with Microsoft for generative AI in engineering workflows (2023-2024).
  - **Xcelerator platform:** Comprehensive digital twin platform with AI throughout.
  - **Altair integration** *(post-acquisition):* HyperWorks, SimSolid, Inspire generative design now part of Siemens portfolio.
- **AI + CAD Relevance:** Massive investment in AI across the entire digital thread. Industrial Copilot is a major initiative. Altair acquisition (2024, ~$10B) significantly expands AI simulation and optimization capabilities.
- **Key Differentiator:** Broadest digital twin and industrial software portfolio. Deep manufacturing and factory automation integration. Altair acquisition adds best-in-class simulation-driven AI design.

---

### Altair Engineering (now Siemens)
- **Website:** https://www.altair.com
- **Founded:** 1985
- **Status:** Acquired by Siemens in 2024 for ~$10B. Operates within Siemens Digital Industries Software.
- **AI Products/Features (Updated 2025-2026):**
  - **HyperWorks 2025.1:** AI-powered engineering and optimization capabilities. *(Confirmed 2025)*
  - **Acquired Gen3D:** Generative design company acquisition strengthens AI design generation. *(Confirmed 2025-2026)*
  - **Ranked #1 by ABI Research** for AI in engineering. *(Confirmed 2025-2026)*
  - **Altair Inspire:** Generative design and topology optimization.
  - **Altair PhysicsAI:** AI tools for physics simulation.
  - **Altair SimSolid:** Meshless structural simulation.
  - **RapidMiner:** Data analytics platform.
- **AI + CAD Relevance:** Strong in AI for simulation-driven design, topology optimization, and generative design. #1 ABI Research ranking validates their AI engineering position.
- **Key Differentiator:** Combined simulation + data analytics + AI platform. Gen3D acquisition adds generative design IP. Now part of Siemens, creating a formidable AI-for-engineering powerhouse.

---

### Dassault Systemes (SOLIDWORKS, CATIA, 3DEXPERIENCE)
- **Website:** https://www.3ds.com
- **Founded:** 1981
- **Public company** (Euronext: DSY), Market cap ~$60B+
- **AI Products/Features:**
  - **3DEXPERIENCE platform AI:** AI-driven search, recommendation, and optimization.
  - **SOLIDWORKS AI features:** Intelligent suggestions for part design, assembly, drawing automation.
  - **CATIA with AI:** Advanced surfacing and design exploration.
  - **SIMULIA with ML:** ML for simulation, surrogate models, design of experiments.
  - **Delmia AI:** AI for manufacturing planning and optimization.
  - **Generative Design in CATIA/SOLIDWORKS:** Topology optimization and generative approaches.
- **AI + CAD Relevance:** Comprehensive AI integration across design, simulation, manufacturing, and PLM.
- **Key Differentiator:** Strongest in aerospace/automotive high-end design. 3DEXPERIENCE platform provides unified data model for AI.

---

### PTC (Creo, Windchill, Onshape)
- **Website:** https://www.ptc.com
- **Founded:** 1985
- **Public company** (NASDAQ: PTC), Market cap ~$20B+
- **AI Products/Features:**
  - **Creo Generative Design Extension (GDX):** Powered by Frustum technology (acquired 2018).
  - **Creo AI Assistant / Copilot:** Natural language interface for Creo operations.
  - **Onshape AI features:** Cloud-native CAD with AI-powered auto-constraining, intelligent suggestions. (Note: Adam AI plans Onshape integration, validating the platform's AI-readiness.)
  - **Windchill AI:** AI for PLM search, classification, data quality.
  - **FeatureScript:** Open language for defining CAD features, targetable by LLMs.
- **AI + CAD Relevance:** Strong generative design through Frustum. Onshape's cloud-native, API-first architecture is the most AI-ready among major CAD platforms.
- **Key Differentiator:** Cloud-native CAD (Onshape) combined with enterprise PLM. Onshape's architecture makes it the natural integration target for AI startups (Adam AI, others).

---

### nTop (nTopology)
- **Website:** https://www.ntop.com
- **Founded:** 2015 (New York)
- **Funding:** $95M+ total (Series D 2022 at $65M, led by Insight Partners)
- **Recent Activity (Updated 2025-2026):** Acquired Cloudfluid, a German CFD developer. Integrating GPU-native CFD solver into the nTop platform.
- **Product/Service:** Computational design platform for advanced manufacturing. Uses implicit modeling and field-driven design to create complex geometries (lattices, gyroids, optimized structures). Now expanding into integrated CFD simulation via Cloudfluid acquisition.
- **AI + CAD Relevance:** Next-generation engineering design tool with algorithmic/computational methods. Cloudfluid acquisition adds GPU-native simulation directly into the design loop.
- **Key Differentiator:** Implicit modeling approach enables designs impossible in traditional B-rep CAD. Cloudfluid acquisition creates a vertically integrated design + simulation platform for advanced manufacturing.

---

### Hexagon (MSC Software, Cradle, BricsCAD)
- **Website:** https://hexagon.com
- **Founded:** 1992 (Sweden)
- **Public company** (OMX: HEXA B), Market cap ~$30B+
- **AI Products/Features:**
  - **MSC Software with AI/ML:** Simulation tools (Nastran, Adams, Marc) enhanced with ML surrogate models.
  - **BricsCAD AI-assisted features:** Intelligent 2D-to-3D conversion, Blockify, Bimify.
  - **Hexagon Manufacturing Intelligence AI:** AI for metrology, quality, manufacturing optimization.
  - **Acquired Intact Solutions:** Meshless simulation with AI.
- **AI + CAD Relevance:** AI for simulation, manufacturing quality, and the design-to-manufacturing pipeline.
- **Key Differentiator:** Strongest in simulation and metrology/quality. Unique position bridging design simulation and physical measurement.

---

### Ansys (now Synopsys)
- **Website:** https://www.ansys.com
- **Founded:** 1970
- **Status:** Acquired by Synopsys in 2024 for $35B.
- **AI Products/Features:**
  - **Ansys SimAI:** Cloud-based AI-powered simulation platform predicting results in near real-time using ML.
  - **AI/ML acceleration:** Physics-informed neural networks (PINNs), reduced-order models.
  - **Ansys Discovery:** Real-time GPU-accelerated simulation.
  - **Ansys Granta MI with AI:** AI for materials selection.
- **AI + CAD Relevance:** Major player in AI-accelerated simulation. SimAI represents a paradigm shift from traditional FEA.
- **Key Differentiator:** Deepest simulation portfolio in the industry. Combined with Synopsys DSO.ai, spans electronic and mechanical AI design.

---

### Shapr3D
- **Website:** https://www.shapr3d.com
- **Founded:** 2015 (Budapest, Hungary)
- **Funding:** $45M+ total (Series B 2022)
- **Product/Service:** Mobile/tablet-first CAD built on Siemens Parasolid kernel. AI-driven UX with intelligent suggestions and constraint inference.
- **AI + CAD Relevance:** Modern CAD platform with AI-enhanced UX, well-positioned for further AI features due to modern architecture.
- **Key Differentiator:** iPad-first / mobile-first CAD. Modern codebase more amenable to AI integration than legacy CAD.

---

### Onshape (PTC)
- **Website:** https://www.onshape.com
- **Founded:** 2012 (acquired by PTC 2019 for $470M)
- **Product/Service:** Cloud-native CAD with FeatureScript, AI-powered defaults, auto-constraining sketches, smart assembly mating.
- **AI + CAD Relevance:** Most AI-ready architecture among major CAD platforms due to cloud-native, data-rich, API-first design. Natural target for AI startup integrations (e.g., Adam AI).
- **Key Differentiator:** Full cloud-native architecture with no file system. All data is API-accessible, making it ideal for AI integration.

---

### BricsCAD (Bricsys, Hexagon)
- **Website:** https://www.bricsys.com
- **Founded:** 2002 (acquired by Hexagon 2018)
- **Product/Service:** CAD platform with AI-assisted features: intelligent 2D-to-3D conversion, Blockify (auto-recognizes repeated geometry), Bimify (auto-classifies elements), ML for drawing recognition.
- **AI + CAD Relevance:** One of the earliest CAD platforms to ship ML-based features for drawing intelligence.
- **Key Differentiator:** Blockify and Bimify are practical, shipped AI features solving real CAD workflow problems.

---

## 3. Adjacent Companies

AI for manufacturing, simulation, 3D generation, and engineering -- related to but not exclusively focused on AI-for-CAD.

---

### Divergent Technologies
- **Website:** https://www.divergent3d.com
- **Founded:** 2015
- **Funding:** $400M+ total. Raised $230M additional round (2025), bringing total well above $400M. *(Updated 2025-2026)*
- **Product/Service:** AI-powered generative design + additive manufacturing for automotive/aerospace structures. The DAPS (Divergent Adaptive Production System) uses AI to design and manufacture optimized vehicle structures.
- **AI + CAD Relevance:** End-to-end AI generative design to additive manufacturing. Designs complete vehicle structures using AI.
- **Key Differentiator:** Full stack: AI design + manufacturing for production vehicles. Partnerships with major automakers. Among the best-funded companies in the AI-for-physical-design space.

---

### Applied Intuition
- **Website:** https://www.appliedintuition.com
- **Founded:** 2017
- **Funding:** $2.6B+ total, valued at $6B+
- **Product/Service:** AI-powered simulation and development platform for autonomous vehicles. Uses AI for vehicle design simulation and testing.
- **AI + CAD Relevance:** Adjacent -- AI simulation for automotive design and testing.
- **Key Differentiator:** Leading autonomy simulation platform. Massive funding.

---

### CloudNC
- **Website:** https://www.cloudnc.com
- **Founded:** 2016 (London, UK)
- **Funding:** $45M+ total
- **Recent Activity (Updated 2025-2026):** Launched CAM Assist 2.0 in 2025 with enhanced AI-automated CAM programming capabilities.
- **Product/Service:** AI-powered CNC manufacturing automation. CAM Assist uses AI to automatically generate optimal CNC toolpaths from CAD models. Version 2.0 extends automation capabilities.
- **AI + CAD Relevance:** AI that takes CAD models as input and generates manufacturing instructions (CAM). Directly in the CAD-to-manufacturing pipeline.
- **Key Differentiator:** AI-automated CAM programming. CAM Assist 2.0 (2025) represents continued momentum in AI-driven manufacturing automation.

---

### Machina Labs
- **Website:** https://www.machinalabs.ai
- **Founded:** 2019
- **Funding:** $72M+ total. Closed $32M Series B. *(Updated 2025-2026)*
- **Product/Service:** AI-powered robotic sheet metal forming. Uses AI to control robots that form metal parts directly from CAD models.
- **AI + CAD Relevance:** AI-driven manufacturing that takes CAD directly to production. Closes the loop between design and making.
- **Key Differentiator:** Robot-based manufacturing controlled by AI, directly from CAD. Series B signals market validation.

---

### aPriori Technologies
- **Website:** https://www.apriori.com
- **Founded:** 2003
- **Funding:** ~$200M+ total (private equity backed)
- **Product/Service:** Digital manufacturing simulation software. AI analyzes CAD models to estimate manufacturing cost, carbon footprint, and manufacturability across processes.
- **AI + CAD Relevance:** AI that directly analyzes CAD geometry for manufacturing intelligence. One of the most mature AI-for-DFM tools.
- **Key Differentiator:** The leading digital manufacturing cost/sustainability analysis platform. Deep physics-based + AI cost models.

---

### Vention
- **Website:** https://www.vention.io
- **Founded:** 2016 (Montreal, Canada)
- **Funding:** $120M+ total
- **Product/Service:** Cloud-based platform for designing and deploying industrial automation. Includes cloud CAD, automated design assistance, and component marketplace.
- **AI + CAD Relevance:** AI-assisted machine design platform with cloud CAD and automated suggestions.
- **Key Differentiator:** Full platform from design to deployment for industrial automation. Modular hardware + software.

---

### Rescale
- **Website:** https://www.rescale.com
- **Founded:** 2011
- **Funding:** $100M+ total
- **Product/Service:** Cloud HPC platform for engineering simulation with AI/ML integration. Runs simulations at scale and provides ML tools for engineering optimization.
- **AI + CAD Relevance:** Infrastructure for AI-powered engineering simulation and design optimization.
- **Key Differentiator:** Cloud HPC + AI/ML platform for engineering.

---

### NVIDIA (Omniverse, AI for 3D)
- **Website:** https://www.nvidia.com
- **Founded:** 1993
- **Public company** (NASDAQ: NVDA)
- **Product/Service:** Omniverse platform for 3D simulation and digital twins. AI for simulation, physics-informed ML, Modulus framework. USD ecosystem.
- **AI + CAD Relevance:** Infrastructure and platform provider for AI-driven 3D/engineering workflows.
- **Key Differentiator:** GPU compute + Omniverse platform + physics-ML frameworks.

---

### Luma AI
- **Website:** https://www.lumalabs.ai
- **Founded:** 2021
- **Funding:** $70M+ total (Series B)
- **Product/Service:** Neural radiance fields (NeRF) and 3D capture/generation from photos/video.
- **AI + CAD Relevance:** 3D reconstruction from images -- adjacent to image-to-CAD. Relevant for reverse engineering workflows.
- **Key Differentiator:** Consumer-accessible 3D capture with production-quality output.

---

### Instrumental
- **Website:** https://www.instrumental.com
- **Founded:** 2015
- **Funding:** $50M+ total (Series C)
- **Product/Service:** AI-powered manufacturing quality assurance using computer vision to detect defects.
- **AI + CAD Relevance:** AI connecting CAD design intent to manufacturing reality through inspection and quality analysis.
- **Key Differentiator:** Manufacturing-focused AI that closes the loop between design and production.

---

### PhysicsX
- **Website:** https://www.physicsx.ai
- **Founded:** 2019 (London, UK)
- **Funding:** $32M Series A (2023)
- **Product/Service:** AI for engineering simulation and design. Uses deep learning to accelerate physics simulations (CFD, FEA, thermal) by orders of magnitude.
- **AI + CAD Relevance:** AI-accelerated simulation directly impacting the design iteration loop.
- **Key Differentiator:** Deep physics expertise combined with ML. Founded by ex-F1 engineers.

---

### SimScale
- **Website:** https://www.simscale.com
- **Founded:** 2012 (Munich, Germany)
- **Funding:** $45M+ total
- **Product/Service:** Cloud-native simulation platform (CFD, FEA, thermal) with AI-assisted meshing, setup recommendations, and result analysis.
- **AI + CAD Relevance:** Cloud simulation with AI features connecting to CAD workflows.
- **Key Differentiator:** Fully cloud-native simulation with AI assistance. Accessible to designers, not just simulation experts.

---

### Neural Concept
- **Website:** https://www.neuralconcept.com
- **Founded:** 2018 (Lausanne, Switzerland)
- **Funding:** ~$10M+ total
- **Product/Service:** Deep learning platform for engineering design optimization. Uses 3D deep learning to predict simulation results on CAD geometries in real time.
- **AI + CAD Relevance:** Directly applies deep learning to 3D CAD geometries for design optimization.
- **Key Differentiator:** 3D deep learning directly on CAD geometry (point clouds, meshes). Trained on simulation data.

---

### Xometry
- **Website:** https://www.xometry.com
- **Founded:** 2013
- **Public company** (NASDAQ: XMTR)
- **Product/Service:** AI-driven on-demand manufacturing marketplace. Instant quoting using ML, automated DFM feedback.
- **AI + CAD Relevance:** AI that analyzes CAD files for manufacturability and pricing.
- **Key Differentiator:** AI-powered instant quoting from CAD files. Marketplace model.

---

### Synopsys (with Ansys)
- **Website:** https://www.synopsys.com
- **Founded:** 1986
- **Public company** (NASDAQ: SNPS)
- **Product/Service:** EDA tools with AI (DSO.ai for chip design). Now includes Ansys simulation portfolio (acquired 2024 for $35B).
- **AI + CAD Relevance:** AI-driven design space optimization for electronics. Combined with Ansys, spans electronic and mechanical AI.
- **Key Differentiator:** DSO.ai is one of the most successful AI-for-design-automation products. Ansys adds mechanical simulation AI.

---

### Cadence Design Systems
- **Website:** https://www.cadence.com
- **Founded:** 1988
- **Public company** (NASDAQ: CDNS)
- **Product/Service:** EDA tools with extensive AI/ML for semiconductor design. AI approaches analogous to AI for mechanical CAD.
- **AI + CAD Relevance:** Pioneering AI in design automation (for electronics). Technology transfer opportunity for MCAD.
- **Key Differentiator:** Most advanced AI in design automation, albeit for electronics.

---

### Monolith AI
- **Website:** https://www.monolithai.com
- **Founded:** 2016 (London, UK)
- **Funding:** $14M+ total (Series A)
- **Product/Service:** Self-service, no-code AI platform for engineering teams. Predictive models from test and simulation data.
- **AI + CAD Relevance:** AI for engineering design optimization using historical data.
- **Key Differentiator:** No-code AI for engineers. Bridges data science and engineering.

---

### Augmenta
- **Website:** https://www.augmenta.ai
- **Founded:** 2018 (London, UK)
- **Funding:** $11M+ total
- **Product/Service:** AI-powered building systems design. Automatically generates MEP designs for buildings.
- **AI + CAD Relevance:** AI generates engineering designs (MEP systems) directly.
- **Key Differentiator:** Fully automated MEP design generation.

---

### Paramatters
- **Website:** https://www.paramatters.com
- **Founded:** 2016 (Los Angeles, CA)
- **Funding:** $6M+ total
- **Product/Service:** AI-powered generative design, topology optimization, and automated DFM analysis.
- **AI + CAD Relevance:** Full AI-driven design-to-manufacturing platform.
- **Key Differentiator:** End-to-end: generative design, lightweighting, AND DFM in one platform.

---

### Formlabs
- **Website:** https://www.formlabs.com
- **Founded:** 2011
- **Funding:** $300M+ total (Series E)
- **Product/Service:** Desktop 3D printing (SLA, SLS). AI for print preparation, auto-orientation, auto-support generation.
- **AI + CAD Relevance:** AI for DFM in the additive manufacturing pipeline.
- **Key Differentiator:** Leading desktop 3D printing company with AI bridging design to manufacturing.

---

### Fictiv
- **Website:** https://www.fictiv.com
- **Founded:** 2013
- **Funding:** $190M+ total
- **Product/Service:** Digital manufacturing platform with AI-based DFM analysis, quoting, and supply chain management.
- **AI + CAD Relevance:** AI for analyzing CAD models for manufacturability and cost.
- **Key Differentiator:** Platform approach to manufacturing with AI at the CAD-to-manufacturing interface.

---

### Materialise
- **Website:** https://www.materialise.com
- **Founded:** 1990 (Belgium)
- **Public company** (NASDAQ: MTLS)
- **Product/Service:** 3D printing software and services. AI for build preparation, quality monitoring, design optimization for AM.
- **AI + CAD Relevance:** AI for the AM-specific portion of the CAD-to-part pipeline.
- **Key Differentiator:** Deepest AM software portfolio with AI for print optimization.

---

### Dyndrite
- **Website:** https://www.dyndrite.com
- **Founded:** 2017
- **Funding:** $20M+ total
- **Product/Service:** GPU-accelerated geometry kernel for additive manufacturing. AI/ML-powered geometry processing, lattice generation, build preparation.
- **AI + CAD Relevance:** Next-generation geometry kernel with AI for additive manufacturing design.
- **Key Differentiator:** GPU-native geometry kernel, purpose-built for AI and additive manufacturing.

---

### Atomic Industries
- **Website:** https://www.atomic.industries
- **Founded:** 2021
- **Funding:** ~$18M+ total
- **Product/Service:** AI-powered precision manufacturing with automated quality control and process optimization.
- **AI + CAD Relevance:** AI bridging CAD design to manufacturing execution.
- **Key Differentiator:** AI-first manufacturing company focused on precision.

---

### Diabatix
- **Website:** https://www.diabatix.com
- **Founded:** 2018 (Belgium)
- **Funding:** ~$5M+ total
- **Product/Service:** AI-powered thermal design. Generative design specifically for heat sinks and thermal management.
- **AI + CAD Relevance:** Domain-specific generative/AI design for thermal engineering. Generates CAD-ready geometries.
- **Key Differentiator:** Domain-specific AI generative design for thermal engineering.

---

### Synera (formerly ELISE)
- **Website:** https://www.synera.io
- **Founded:** 2018 (Germany)
- **Funding:** ~$10M+ total
- **Product/Service:** No-code engineering design automation platform connecting CAD, simulation, and optimization tools.
- **AI + CAD Relevance:** AI-driven automation of engineering design workflows.
- **Key Differentiator:** Visual, no-code approach to engineering design automation.

---

### Meshy AI
- **Website:** https://www.meshy.ai
- **Founded:** ~2023
- **Funding:** Seed stage
- **Product/Service:** AI text-to-3D and image-to-3D model generation for gaming, 3D printing, product visualization.
- **AI + CAD Relevance:** Text/image to 3D generation. Mesh-focused rather than CAD-parametric.
- **Key Differentiator:** Fast, accessible text-to-3D generation.

---

### Makersite
- **Website:** https://www.makersite.io
- **Founded:** 2018 (Germany)
- **Funding:** ~$18M+ total
- **Product/Service:** AI-powered product development intelligence for sustainability, cost, compliance, and supply chain analysis.
- **AI + CAD Relevance:** AI that analyzes engineering designs for non-geometric requirements.
- **Key Differentiator:** Sustainability and compliance AI for product design.

---

---

## Appendix: Key Open Source Projects

| Project | Repository | Description |
|---|---|---|
| CADAM | https://github.com/Adam-CAD/CADAM | Open source text-to-CAD by Adam AI |
| ScadLM | https://github.com/KrishKrosh/ScadLM | Agentic AI CAD generation on OpenSCAD |
| CQAsk | https://github.com/OpenOrion/CQAsk | LLM CAD generation using CadQuery |
| Zoo CAD Kernel | https://zoo.dev | Open source CAD kernel in Rust |

---

## Appendix: Recent M&A Activity (2024-2026)

| Acquirer | Target | Date | Value | Relevance |
|---|---|---|---|---|
| Synopsys | Ansys | 2024 | $35B | Creates electronic + mechanical AI simulation giant |
| Siemens | Altair | 2024 | ~$10B | Adds AI simulation/optimization to Siemens portfolio |
| Rubix LS | Katalyst Labs | 2025-2026 | Undisclosed | Open-source AI copilot for hardware design |
| Altair/Siemens | Gen3D | 2025-2026 | Undisclosed | Generative design technology |
| nTop | Cloudfluid | 2025-2026 | Undisclosed | GPU-native CFD solver |
| PTC | Frustum | 2018 | Undisclosed | Generative design (historical) |
| PTC | Onshape | 2019 | $470M | Cloud-native CAD (historical) |
| Hexagon | Intact Solutions | -- | Undisclosed | Meshless simulation (historical) |

---

## Appendix: Funding Leaderboard (Ranked by Total Raised)

| Company | Total Funding | Stage | Category |
|---|---|---|---|
| Project Prometheus | $6.2B | Mega-round | Pure-play AI-for-CAD |
| Divergent Technologies | $400M+ (incl. $230M 2025 round) | Late stage | Adjacent (AI manufacturing) |
| nTop | $95M+ | Series D | Pure-play AI-for-CAD |
| Machina Labs | $72M+ (incl. $32M Series B) | Series B | Adjacent (AI manufacturing) |
| Luma AI | $70M+ | Series B | Adjacent (3D generation) |
| Instrumental | $50M+ | Series C | Adjacent (manufacturing QA) |
| CloudNC | $45M+ | Growth | Adjacent (AI CAM) |
| Shapr3D | $45M+ | Series B | Established CAD w/ AI |
| PhysicsX | $32M | Series A | Adjacent (AI simulation) |
| Physna/Thangs | $30M+ | Series A | Pure-play AI-for-CAD |
| Zoo (KittyCAD) | $30M+ | Series A | Pure-play AI-for-CAD |
| Vizcom | $20M+ | Series A | Pure-play AI-for-CAD |
| Kaedim | $15M+ | Series A | Pure-play AI-for-CAD |
| Hyperganic | $13M+ | Series A | Pure-play AI-for-CAD |
| Adam AI | $4.1M | Seed (YC W25) | Pure-play AI-for-CAD |
| Sloyd | $3.4M | Seed | Pure-play AI-for-CAD |

---

*Document compiled February 8, 2026. Incorporates raw researcher knowledge supplemented and verified with live web search data from 2025-2026. Companies marked "Updated 2025-2026" contain confirmed information from live web searches. Some early-stage startup details (websites, exact funding) may change rapidly.*
