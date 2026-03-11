# LEGO Engineering Benchmark — Idea Doc

## The Core Idea

Hook up an LLM (Claude, GPT) to a LEGO Technic environment and ask it to design mechanisms — the same way we ask it to write code. The LLM writes an assembly, a validator runs it, errors feed back, it iterates.

```
prompt → LLM → assembly description → validator → result/errors → LLM → ...
```

This is the first benchmark where an AI has to reason about a real, named, constrained parts vocabulary — the same discipline a real engineer uses when opening McMaster-Carr.

---

## Why LEGO Technic

- Fixed, well-documented part library (~17k parts in LDraw, ~150 relevant Technic parts)
- Real mechanisms: gears have tooth counts, gear ratios are computable, rack-and-pinion converts rotation to linear motion
- Connections are physically unambiguous — a pin either fits a hole or it doesn't
- No material properties, no tolerances, no manufacturing constraints — pure mechanism reasoning
- Validation can be done analytically for many tasks (gear ratios, connectivity) without a full physics sim

---

## What You Need to Build

**1. Part library** (~150 curated Technic parts)
JSON file: part ID, description, connection points, tooth count if gear, hole positions if beam. LLM can search it.

**2. Assembly DSL** — a text format the LLM writes
Simple structured format, something like:
```json
{
  "parts": [
    {"id": "A", "type": "beam-5", "pos": [0,0,0], "orient": "horizontal"},
    {"id": "B", "type": "gear-24t", "pos": [4,0,0]},
    {"id": "C", "type": "gear-8t",  "pos": [4,2,0]}
  ],
  "connections": [
    {"from": "A.hole[4]", "to": "B.axle"},
    {"from": "B.mesh",    "to": "C.mesh"}
  ]
}
```

**3. Structural validator** (~1 day)
Parse output, check every connection is physically valid, detect overlaps, floating parts, missing connections. Returns plain-text errors the LLM can act on.

**4. Kinematic checker** (for simple tasks)
For gear trains: traverse the mesh graph, compute ratio analytically.
For rotation→linear: check for rack gear in chain.
Skip full physics sim for v1.

**5. Renderer**
LDraw file → BrickLink Studio / Three.js for visualization.

---

## Example Benchmark Tasks

| Level | Prompt |
|---|---|
| T1 | "Connect two gears with a 3:1 ratio" |
| T2 | "Build a drivetrain that runs two wheels from one axle" |
| T3 | "Build a planar-to-rotational mechanism using fewer than 20 parts that fits in a 16×16 stud area" |
| T4 | "Build a steering mechanism that fits in 10×10×5 studs" |
| T5 | "Design a 2-speed gearbox" |

### Key test prompt
> *"Build me a planar-to-rotational mechanism that uses fewer than 20 parts and fits in a 16×16 stud area."*

This is the core test. It requires the model to:
- Know what a planar-to-rotational mechanism is (rack and pinion, or crank-slider)
- Select appropriate parts from the library
- Arrange them spatially within the constraint
- Produce a valid assembly

---

## The Layered Vision (bigger picture)

This benchmark sits in a 3-level hierarchy for AI mechanical engineering:

```
Level 1: Mechanism reasoning       ← LEGO Technic benchmark (this)
Level 2: Part sourcing             ← McMaster-Carr / standard parts library
Level 3: Custom part generation    ← AI-for-CAD (what we're already building)
```

A model that aces LEGO but fails CAD → bottleneck is tool interface, not reasoning.
A model that aces CAD but fails LEGO → pattern-matching geometry, not engineering thinking.

---

## What's Actually Hard

1. Designing the DSL (expressive enough, writable by an LLM)
2. Structural validator (parsing + constraint checking)
3. Keeping LLM inside the part vocabulary (no hallucinated part IDs)
4. Kinematic sim for non-trivial motion (rack-and-pinion is easy; linkages are harder)

---

## Minimum Viable Demo

- ~50 Technic parts in JSON
- Task: "build a gear train with 3:1 ratio"
- LLM outputs JSON assembly
- Validator checks connections + computes actual gear ratio
- Feed errors back, LLM iterates
- Render in BrickLink Studio or Three.js

Estimated: 1-2 weeks of work.
