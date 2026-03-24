# Lego Technic as a Benchmark for Engineering Intelligence in AI

## Status: outline / vision
## Target: full conference paper (~8-10 pages)

---

## Core Thesis

Mechanical engineering tasks and software engineering tasks are structurally equivalent
in complexity: both require hierarchical decomposition, both are simulatable, and both
require iterative feedback. Yet AI performs dramatically worse on mechanical tasks.

We argue the gap is explained by one specific capability bottleneck:
**mechanical feedback interpretation** — the ability to take physical/spatial error
signals ("these pieces don't connect here") and decide how to fix them.
This is harder than software feedback ("TypeError on line 47") because it requires
spatial reasoning about 3D structure, not pattern matching on error strings.

We claim this capability is a *necessary condition* for AI to become useful in
real mechanical engineering. We do not solve it. We name it, demonstrate it exists,
measure it, and release a benchmark so others can work on it.

---

## Why Lego Technic

- **Discrete and verifiable**: pieces either connect or they don't — binary success signal
- **Simulatable**: LDraw format allows programmatic validity checking
- **Complexity ceiling is very high**: from a single brick to a working differential gearbox
- **Maps to real ME primitives**: gears, levers, cams, linkages, ratchets
- **Culturally legible**: reviewers understand what a gear train is
- **Data-sparse for AI**: almost nothing in training data → fair test of generalization

---

## The Structural Equivalence Argument (to flesh out)

| | Software task | Lego Technic task |
|---|---|---|
| Decomposition | "Build auth, then UI, then API" | "Build escapement, then gear train, then hands" |
| Simulation | Run the code | Render + check LDraw connections |
| Feedback | Stack trace, test failure | Piece collision, missing connection |
| Iteration | Fix the error | Fix the spatial conflict |
| Complexity ceiling | Arbitrarily high | Arbitrarily high |

The difference: software feedback maps to fixes via pattern matching (billions of training examples). Mechanical feedback requires spatial reasoning to diagnose and fix (near-zero training examples).

---

## Outline

### 1. Introduction (~1 page)
- AI has transformed software engineering (Copilot, Devin, etc.)
- Mechanical engineering remains largely untouched
- Common assumption: "physics is harder" — we argue this mislocates the problem
- The real bottleneck is mechanical feedback interpretation, not task complexity
- We introduce the Lego Engineering Benchmark to demonstrate and measure this

### 2. Related Work (~1 page)
- Text-to-CAD benchmarks (Text2CAD, CAD Arena, ShapeNet-based)
- Code generation benchmarks (HumanEval, SWE-bench) — what makes them work
- Physical reasoning in AI (intuitive physics, embodied AI)
- BrickGPT and Lego-adjacent work — what exists, what's missing
- Assembly planning literature

### 3. The Structural Equivalence Thesis (~1 page)
- Formal argument: both task types are (decomposable, simulatable, feedback-driven)
- Prediction: if equivalence holds, performance gap = feedback interpretation gap
- How we test this: ablation that isolates decomposition from feedback-response

### 4. The Lego Engineering Benchmark (~2 pages)
- Dataset construction: prompts + reference assemblies + complexity tiers
  - Tier 1: static structures (a bridge, a house)
  - Tier 2: simple mechanisms (a gear reduction, a lever)
  - Tier 3: functional systems (a working clock, a vehicle drivetrain)
- Evaluator: LDraw validity checker + functional simulation
- Metrics: connection validity, functional correctness, decomposition quality
- Feedback protocol: how we give models mechanical error signals

### 5. Experiments (~2 pages)
- Models evaluated: GPT-4o, Claude 3.5 Sonnet, Gemini 2.5, [specialized models]
- Baseline: zero-shot, chain-of-thought, with/without mechanical feedback
- Key result: models can decompose reasonably well, fail at feedback response
- Ablation: give model perfect decomposition → still fails at feedback-response
  (this is the key experiment that proves the thesis)

### 6. Analysis: Where Models Fail (~1 page)
- Decomposition failure rate vs. feedback-response failure rate
- Examples of each failure type
- Qualitative: what kinds of mechanical feedback are hardest to act on?
- Complexity tier breakdown

### 7. Discussion (~0.5 pages)
- Mechanical feedback interpretation as necessary condition (the argument)
- What a system that solves this might look like (RL harness, spatial world model)
- Why this matters beyond Lego: real ME tasks have the same structure
- Limitations

### 8. Conclusion
- We named the bottleneck
- We measured it
- Here's the platform to keep working on it

---

## Key Experiments Needed

1. **Main benchmark run**: N models × M prompts across 3 tiers, score each
2. **Decomposition ablation**: provide perfect step-by-step decomposition, measure if performance improves → if yes, decomposition is a bottleneck too; if no, feedback-response is the only bottleneck
3. **Feedback ablation**: give model the error message + gold fix, measure if it can apply fix → tests whether model can even *use* perfect feedback
4. **Human baseline**: how does a non-expert human do with the same prompts + same feedback format?

---

## What's Missing Before Submission

- [ ] Benchmark dataset built (prompts + reference assemblies)
- [ ] LDraw evaluator written
- [ ] At least 3-4 models run
- [ ] Ablation experiment designed and run
- [ ] BrickGPT results (closest prior work — must reproduce + cite)
- [ ] Faculty co-author or advisor (this needs someone who knows the assembly planning literature)

---

## Possible Submission Targets

See `../venues.md` for full analysis.

**Best fit (full papers):**
- NeurIPS 2026 (deadline ~May/June) — Datasets & Benchmarks track
- ICML 2026 — main track if framing is right
- ICLR 2027 — strong fit if we have good ablations
- CoRL 2026 (Conference on Robot Learning) — physical reasoning angle fits well

**Also relevant:**
- IROS / ICRA — robotics venues, assembly planning audience
- arXiv first as always

---

## Timeline (rough)

- Benchmark dataset v1: 1-2 months
- Evaluator: 2-3 weeks once dataset exists
- Initial model runs: 1 week
- Ablations: 2-3 weeks
- Draft: ~3 months from now
- NeurIPS 2026 submission: May 2026 (tight but possible)
- ICLR 2027: Oct 2026 (more realistic)
