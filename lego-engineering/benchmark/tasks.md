# Lego Engineering Benchmark — Task Set v1

20 tasks across 5 tiers. Each task has a machine-checkable success criterion (see tasks.json).

---

## Tier 1 — Structural Assembly (3 tasks)
*Tests: basic part usage, connectivity, no kinematics required*

| ID | Name | Prompt summary | Key check |
|---|---|---|---|
| T1-01 | Parallel axle frame | Hold two axles 4 studs apart in a rigid beam frame | 2 axles present, spacing = 4 |
| T1-02 | Rectangular beam frame | 9×7 stud outer frame, beams connected at corners with pins | Bounding box ≤ 9×7×2 |
| T1-03 | Axle through beam | Axle through center of two beams, 3 studs apart, bushes on ends | 1 axle, 2 beams, 2 bushes |

---

## Tier 2 — Single Mechanism (5 tasks)
*Tests: specific mechanism knowledge, one mechanism type per task*

| ID | Name | Prompt summary | Key check |
|---|---|---|---|
| T2-01 | 3:1 gear reduction | Gear pair with 3:1 speed reduction, mounted on frame | Gear ratio = 3.0 ± 0.05 |
| T2-02 | 2:1 gear reduction | Gear pair with 2:1 speed reduction | Gear ratio = 2.0 ± 0.05 |
| T2-03 | 5:1 gear reduction | Gear pair or train with 5:1 reduction | Gear ratio = 5.0 ± 0.05 |
| T2-04 | Rack and pinion | Gear drives rack, converts rotation to linear motion | motion_type = rotational_to_linear |
| T2-05 | Worm gear reduction | Worm gear driving 24T spur gear | worm present, ratio ≥ 20:1 |

**Note on T2-03:** No single gear pair gives exactly 5:1 with available parts. The only solution is 8T + 40T. This tests whether the model knows actual tooth counts (8, 16, 24, 40) vs. hallucinating a "20T gear."

---

## Tier 3 — Mechanism Reasoning (5 tasks)
*Tests: multi-step reasoning, direction awareness, optimization*

| ID | Name | Prompt summary | Key check |
|---|---|---|---|
| T3-01 | 9:1 compound gear train | Two 3:1 stages, intermediate axle, total 9:1 | Gear ratio = 9.0 ± 0.1, ≥ 4 gears |
| T3-02 | Maximum ratio with 4 gears | Highest ratio using exactly 4 gears, explain why | Exactly 4 gears, ratio ≥ 9.0 |
| T3-03 | Rotation reversal | Output spins opposite direction to input, minimum gears | output_direction = reversed |
| T3-04 | Speed increase (overdrive) | Output spins ≥ 3× faster than input | Gear ratio ≤ 0.34 |
| T3-05 | Three-axle gear chain | 3 axles in series, each stage 3:1, total 9:1, all aligned | Ratio = 9.0, ≥ 3 axles |

**T3-02 is a key discriminator:** The optimal answer is worm(1T) + gear-40t(40T) = 40:1, which is higher than two 3:1 stages (9:1). Models that just repeat the 9:1 compound train from T3-01 score lower than models that recognize the worm gear option.

---

## Tier 4 — Constrained Design (4 tasks)
*Tests: reasoning under constraints (volume, part count)*

| ID | Name | Prompt summary | Key check |
|---|---|---|---|
| T4-01 | Compact 3:1 reduction | 3:1 gear reduction within 10×5×5 stud bounding box | Ratio = 3.0, bbox ≤ [10,5,5] |
| T4-02 | Minimal rack-and-pinion | Rack and pinion in ≤ 6 parts total | motion_type = rotational_to_linear, parts ≤ 6 |
| T4-03 | 9:1 under part budget | ≥ 9:1 reduction using ≤ 10 parts total | Ratio ≥ 9.0, parts ≤ 10 |
| T4-04 | Symmetric dual-output | One input drives two output axles at same speed | ≥ 3 axles, symmetric arrangement |

**T4-03 reveals a key insight:** Worm + 40T gear (40:1) needs fewer parts than two-stage 8T+24T+8T+24T (9:1). Models that use worms score better here — the constraint forces efficient design.

---

## Tier 5 — Open Design (4 tasks)
*Tests: creative mechanism design, reasoning about limitations*

| ID | Name | Prompt summary | Key check |
|---|---|---|---|
| T5-01 | Highest ratio from 6 parts | Any 6 parts, maximize ratio, explain reasoning | Exactly 6 parts, ratio ≥ 24:1 |
| T5-02 | Motion conversion chain | 3-stage: gear reduction → rack/pinion → rotation out | Ratio = 3:1 AND motion_type present |
| T5-03 | Differential concept | Input drives two outputs that can spin at different speeds | ≥ 4 gears, reasoning quality |
| T5-04 | Clock escapement | Simulate a clock escapement: controlled tick-tick rotation | Qualitative — scored manually |

**T5-03 and T5-04 are intentionally unsolvable with current parts.** T5-03 has no differential part in the library. T5-04 has no pawl/ratchet part. These are diagnostic tasks: we want to see if the model recognizes the limitation and explains it, or just hallucinates parts that don't exist.

---

## Scoring Rubric

| Score | Meaning |
|---|---|
| 2 | Fully passes all success criteria |
| 1 | Partial pass — valid assembly, wrong mechanism or constraint violated |
| 0 | Invalid assembly (validator errors) or hallucinated parts |
| -1 | Reserved for tasks where model claims to succeed but misunderstands the task |

**Per-tier aggregate:**
- T1 average: structural competence
- T2 average: mechanism vocabulary
- T3 average: multi-step mechanical reasoning
- T4 average: constrained optimization
- T5 average: open-ended design + knowing what's impossible

---

## Key Diagnostic Questions This Task Set Answers

1. **Does the model know tooth counts?** (T2-03: 5:1 requires 8T+40T, no 20T exists)
2. **Does it understand compound gearing?** (T3-01, T3-05)
3. **Does it reason about direction?** (T3-03, T3-04)
4. **Does it optimize or just satisfy?** (T3-02, T4-03, T5-01)
5. **Does it hallucinate parts?** (T5-03, T5-04 — worm detection)
6. **Can it recognize unsolvability?** (T5-03, T5-04)
7. **Does it reason about spatial constraints?** (T4-01, T4-02)

Questions 5 and 6 are the most interesting for the paper — they directly test mechanical feedback interpretation vs. mechanical knowledge.
