# Lego Engineering Benchmark — Full Design Space
## A taxonomy of what this could be

---

## 1. Task Space

What kinds of tasks could we ask a model to do?

### Axis 1: Output type

**Aesthetic / Structural**
The model produces something that looks like or represents a real object. Success is recognizability or structural coherence.
- "Build Big Ben out of Lego, ≤100 bricks"
- "Build a red sports car, ≤150 bricks"
- "Build a bridge that spans 20 studs"
- "Build a minifig-scale house with a door and two windows"

**Functional / Mechanical**
The model produces something that *does* something. Success is whether the mechanism works.
- "Build a gear train with 3:1 reduction"
- "Build a mechanism that converts rotation to linear motion"
- "Build a working steering mechanism"
- "Build a 2-speed gearbox"

**Functional + Aesthetic**
Both — the result must look like something AND work.
- "Build a vehicle with working drivetrain and steering, ≤200 bricks"
- "Build a crane with a working winch mechanism"
- "Build a clock tower where the clock hands are driven by a gear train"

**Structural / Engineering**
The result must satisfy a physical constraint (span, load, stability).
- "Build the longest bridge you can using ≤50 bricks"
- "Build the tallest freestanding tower using ≤100 bricks"
- "Build a structure that could support the weight of a standard Lego figure"

### Axis 2: Constraint type

**Unconstrained:** "Build a gear train with 3:1 reduction" — any valid solution accepted
**Part count:** "...using ≤20 parts"
**Volume:** "...that fits within a 16×16×10 stud bounding box"
**Part budget:** "...using only the parts in this specific set"
**Named parts required:** "...must use a worm gear"
**Named parts forbidden:** "...without using any axle longer than 5 studs"
**Optimality:** "...using the fewest possible parts" or "...with the highest possible ratio"

### Axis 3: Specificity

**Fully specified:** "Build a gear pair with exactly 3:1 reduction using an 8T and 24T gear"
→ One correct answer, easy to verify

**Under-specified:** "Build something that reduces speed"
→ Many valid answers, tests creative solution selection

**Open-ended:** "Build a clock escapement"
→ No single right answer, tests whether model knows what it doesn't know

**Impossible:** "Build a differential using only the parts in this library" (when no bevel/differential part exists)
→ Tests whether model recognizes impossibility vs. hallucinating

### Axis 4: Domain

| Domain | Examples | Evaluation |
|---|---|---|
| Classic Lego (stud-based) | Big Ben, vehicles, buildings | VLM judge / human eval |
| Technic mechanisms | Gear trains, rack/pinion, linkages | Programmatic / kinematic sim |
| Technic structural | Frames, chassis, trusses | Programmatic (connectivity) |
| Mindstorms / robotics | Sensors, motors, control logic | Requires simulation |
| Pneumatics | Air-powered actuators | Requires physics sim |
| Custom (MOC) | Novel designs from user description | Human eval |

---

## 2. Part Library Options

### Size tiers

**Micro (~50 parts):** MVP. Gear train tasks only.
Current state: 23 parts in mar11-demo-attempt.

**Small (~200 parts):** Covers Technic mechanisms + basic structural bricks.
Enough for: Big Ben silhouette, gear trains, simple vehicles.

**Medium (~1000 parts):** Curated "best of" Lego catalog.
Covers most MOC builds, all Technic, specialty parts.
Requires search interface to be usable.

**Full (~17,000+ parts):** Complete LDraw library.
Every official Lego part ever made.
Requires embeddings + semantic search to be usable at all.

### What metadata each part needs

```json
{
  "id": "gear-24t",
  "ldraw_id": "3648",
  "bricklink_id": "3648",
  "name": "Technic Gear 24 Tooth",
  "category": "technic_gear",
  "subcategory": "spur_gear",
  "description": "Spur gear, 24 teeth. Meshes with other spur gears and racks.",
  "teeth": 24,
  "radius_studs": 3.0,
  "connection_points": [
    {"type": "axle_hole", "pos": [0,0,0]},
    {"type": "gear_mesh", "radius": 3.0}
  ],
  "compatible_with": ["gear-8t", "gear-16t", "gear-40t", "rack-4", "gear-worm"],
  "notes": "Standard cross-axle bore. Meshes with 8T at 4 studs center distance."
}
```

### How the model accesses parts

**Option A: Full list in system prompt**
Dump all parts as JSON. Works up to ~200 parts. Beyond that, context becomes unmanageable.

**Option B: Keyword/semantic search tool**
`search_parts(query: str) -> List[Part]`
Model calls: `search_parts("gear with high tooth count")`
Returns: top 5 matching parts with full specs.
This is the McMaster-Carr interface. Interesting for the paper.

**Option C: Hierarchical browse**
`list_categories() -> List[str]`
`list_parts(category: str) -> List[Part]`
`get_part(id: str) -> Part`
Mirrors how a human engineer browses a catalog.

**Option D: Hybrid**
Small curated "common parts" list always in context (top 30 most useful).
Search tool available for the long tail.

**Research question:** Does giving the model a search tool vs. a fixed list change performance?
Hypothesis: search tool helps on complex tasks (model finds the right part), hurts on simple tasks (model wastes turns searching for things it already knows).

---

## 3. Output Format Options

What language/format does the model use to describe the design?

### Option A: LDraw (.ldr)
The industry standard. Every brick has a part file, absolute 3D positioning, rotation matrices.
```
0 // My Assembly
1 16 0 0 0 1 0 0 0 1 0 0 0 1 3648.dat   // gear-24t at origin
1 16 40 0 0 1 0 0 0 1 0 0 0 1 3648b.dat  // gear-8t at x=40 (4 studs)
```
**Pros:** Directly renderable, complete ecosystem, standard
**Cons:** Rotation matrices are nearly impossible for LLMs to write correctly, no semantic structure, extremely verbose for complex builds

### Option B: JSON DSL (current approach)
```json
{
  "parts": [
    {"id": "g1", "type": "gear-24t", "pos": [0,0,0], "axis": "y"},
    {"id": "g2", "type": "gear-8t",  "pos": [4,0,0], "axis": "y"}
  ],
  "connections": [
    {"from": "g1.mesh", "to": "g2.mesh"}
  ]
}
```
**Pros:** LLM-friendly, easy to parse/validate, explicit connection semantics
**Cons:** Non-standard, need to build renderer from scratch, axis-only rotation is limiting for classic Lego (which needs arbitrary orientations)

### Option C: Python builder API
```python
from brickenv import Assembly, parts

a = Assembly()
g1 = a.add(parts.Gear24T(), at=(0,0,0), axis='y', name='g1')
g2 = a.add(parts.Gear8T(),  at=(4,0,0), axis='y', name='g2')
a.connect(g1.mesh, g2.mesh)
a.connect(g1.axle_hole, a.add(parts.Axle5(), name='a1').end)
```
**Pros:** LLMs are excellent at Python, expressive (loops, variables, functions), readable, self-documenting
**Cons:** Need to implement the API + execution environment, more infrastructure

### Option D: Scratch/Blockly-style visual DSL
Not really suitable for LLM output. Skip.

### Option E: Natural language → structured (two-pass)
Model describes design in prose, second LLM pass converts to formal format.
**Pros:** Removes output burden from model, captures reasoning
**Cons:** Conversion is lossy, adds latency and cost, hard to evaluate cleanly

### Option F: SCAD-style (constructive solid geometry text)
Like OpenSCAD but for Lego. Declarative, composable.
```scad
gear_pair(driver=24, driven=8, spacing=4, axis="y");
rack_pinion(rack_length=4, gear_teeth=8, origin=[0,0,0]);
```
**Pros:** Clean, readable, compositional
**Cons:** Need to define the language and implement it

### Recommended progression
1. **Now:** JSON DSL — fastest to build, good for Technic tasks
2. **Paper v1:** Python API — more expressive, LLMs are better at it, more compelling as a contribution
3. **Long term:** Python API + LDraw export — best of both worlds

---

## 4. Validation & Evaluation Options

How do we check if the design is correct?

### Programmatic validation (current)
Parse output → check part IDs exist → check no overlaps → check connections valid → compute kinematics

**What it can check:**
- Part validity (no hallucinated parts)
- Structural connectivity (is it one connected piece?)
- Gear ratio (analytically)
- Rack-and-pinion detection
- Part count constraints
- Bounding box constraints

**What it cannot check:**
- Whether a complex mechanism actually functions
- Whether something "looks like Big Ben"
- Whether a linkage transmits force correctly
- Whether a structure is stable under load

### Physics simulation
Put the assembly into a physics engine and simulate it.

**Options:**
- **Mujoco:** best-in-class for robot simulation, has Lego-adjacent work
- **PyBullet:** open source, good Python API, used in robotics research
- **Unity/Unreal:** overkill for this purpose
- **Custom rigid-body sim:** possible for Technic (constrained joints) but a lot of work

**What sim enables:**
- Does the gear train actually transmit motion?
- Does the structure collapse under gravity?
- Does the steering mechanism actually steer?
- What's the actual mechanical advantage?

**Cost:** Significant infrastructure. Probably v2.

### LDraw render + VLM judge
Render the assembly to an image → ask GPT-4V / Claude to judge it.

`"Does this image show a working 3:1 gear reduction? Answer yes/no and explain."`

**Pros:** Can evaluate aesthetic tasks ("does this look like Big Ben"), catches things programmatic eval misses
**Cons:** VLM judgments are noisy, expensive per-call, not deterministic

**Best use:** Aesthetic tasks (T1-structural, open-ended designs) where programmatic eval breaks down.

### Human evaluation
Crowdsourced or expert human judges rate outputs.
Required for: "is this a good Big Ben?", creative tasks, comparing designs that all pass validation.
Not scalable for automated benchmarking but needed for paper ground truth.

### Hybrid approach (recommended for paper)
```
Tier 1 (structural) → programmatic connectivity check + VLM judge
Tier 2-3 (mechanisms) → programmatic kinematic check
Tier 4 (constrained) → programmatic check (constraints are computable)
Tier 5 (open) → programmatic + VLM judge + human eval for top outputs
```

---

## 5. Environment / Assembly Options

How does the design actually get assembled/rendered?

### Option A: LDraw ecosystem
Convert output → .ldr file → render with LeoCAD, BrickLink Studio, or Blender+ImportLDraw
**Pros:** Industry standard, photorealistic renders, huge community
**Cons:** Desktop apps, not web-native, conversion step required

### Option B: ldraw.js / WebGL in browser
Pure JavaScript LDraw renderer.
**Pros:** Web-native, embeddable in a platform like cadarena
**Cons:** Lower fidelity, less mature than desktop tools

### Option C: BrickLink Studio API (if it exists)
BrickLink Studio is the most popular consumer Lego CAD tool.
**Cons:** No public API as of 2025, closed ecosystem

### Option D: Custom Three.js renderer
Build brick mesh library → render in browser using Three.js (same as cadarena STL viewer).
**Pros:** Full control, web-native, customizable
**Cons:** Need to model every brick as a 3D mesh. Significant art asset work.

### Option E: Physical assembly (human)
Output instructions → human builds it → photograph/validate.
BrickGPT did this for their paper (assembled by humans, photographed).
**Pros:** Ground truth on buildability
**Cons:** Not scalable, expensive, slow

### Option F: Robotic assembly
CMU's BrickGPT paper has a bimanual robotic system that assembles Lego.
**Pros:** Automated physical ground truth
**Cons:** Very expensive infrastructure, not reproducible by others

### Recommended path
**MVP:** JSON/Python output → convert to LDraw → render with BrickLink Studio or Blender
**Web platform:** ldraw.js in browser (same model as cadarena's STL viewer)
**Paper figures:** Blender + ImportLDraw (photorealistic)

---

## 6. The Full Benchmark Design Space

### Dimension 1: Task type
```
Aesthetic ←————————————————→ Functional
"Build Big Ben"          "Build a differential"
     ↑ VLM/human eval         ↑ Programmatic eval
```

### Dimension 2: Constraint level
```
Unconstrained ←————————————→ Multi-constrained
"Build a gear train"    "9:1 reduction, ≤10 parts, fits 10×10×5"
```

### Dimension 3: Part vocabulary
```
Micro (50)  ←————————————→  Full library (17k)
Fixed list         Requires search tool
```

### Dimension 4: Feedback loop
```
Zero-shot ←————————————→  Iterative (agentic)
One attempt     Model sees errors, revises N times
```

### Dimension 5: Output format
```
JSON DSL ←————————→ Python API ←————————→ LDraw
Easiest           Most expressive     Industry standard
```

### Dimension 6: Evaluation
```
Programmatic ←——→ Physics sim ←——→ VLM judge ←——→ Human
Fastest/cheapest    Most accurate    Middle ground    Ground truth
```

---

## 7. Possible Benchmark Configurations

Different configurations answer different research questions.

**Config A: "Mechanism IQ test" (current direction)**
- Part vocab: Technic only (~200 parts), list in prompt
- Tasks: T1-T5 mechanism tasks
- Output: JSON DSL
- Eval: Programmatic kinematic validator
- Feedback: None (zero-shot) + With errors (1-3 rounds)
- Research question: Can models reason about mechanisms? Does feedback help?

**Config B: "Lego architect"**
- Part vocab: Classic Lego (~1000 parts), search tool
- Tasks: "Build X in ≤N bricks" (buildings, vehicles, animals)
- Output: Python API or JSON
- Eval: VLM judge + human eval
- Research question: Can models design recognizable structures under constraints?

**Config C: "Engineering agent"**
- Part vocab: Full library, semantic search tool
- Tasks: Complex functional designs ("design a Mars rover with working wheels")
- Output: Python API
- Eval: Physics sim + human eval
- Feedback: Full agentic loop (model queries parts, builds, tests, iterates)
- Research question: Can an LLM-powered agent do real engineering design?

**Config D: "Impossibility detector"**
- Focused on tasks that are impossible with available parts
- Tests: Does the model recognize when a task is impossible vs. hallucinating a solution?
- Research question: Does the model know what it doesn't know?

**Config E: "Cross-benchmark" (long term)**
- Run the same model on Lego Technic AND CadQuery (cadarena)
- Same functional task, different substrate
- Research question: Does good performance on one predict good performance on the other?
  If yes → mechanism reasoning transfers. If no → it's pattern matching to syntax.

---

## 8. The Layered Vision

```
Level 3: Open-ended engineering design
         "Design a Mars rover"
         Parts: full library + custom CAD generation
         Eval: physics sim + expert human
              ↑
Level 2: Constrained engineering design
         "Build a 2-speed gearbox in ≤15 parts"
         Parts: Technic library (~200)
         Eval: kinematic simulation
              ↑
Level 1: Mechanism vocabulary
         "Build a 3:1 gear reduction"
         Parts: Technic micro (~50)
         Eval: programmatic (current)
```

The benchmark we're building now is Level 1. Level 2 requires physics sim. Level 3 requires the full CAD generation stack (connects back to cadarena).

**The cross-benchmark insight:**
A model that aces Level 1 (Lego Technic) but fails Level 3 (CadQuery)
→ Can reason about mechanisms, can't translate to CAD
A model that aces Level 3 but fails Level 1
→ Pattern-matching CAD syntax, not doing mechanism reasoning

This is the paper.

---

## 9. What Doesn't Exist Yet That We'd Be Building

To be clear about novelty:

- **BrickGPT (ICCV 2025):** Text to static Lego structures (aesthetic). No mechanisms. No feedback loop. No benchmark tasks. Fine-tuned small model.
- **Text2CAD / CAD Arena:** Text to CAD geometry. No Lego. No mechanisms. No feedback loop.
- **Assembly planning literature (robotics):** Sequence planning for known assemblies, not generative design.
- **LegoGPT (if it exists):** Unknown, would need to check.

**What we'd be first at:**
- Benchmark for AI *mechanism design* (not just structure generation)
- Measuring mechanical feedback interpretation specifically
- The feedback loop as an experimental variable
- Cross-benchmark comparison between Lego and CAD performance

---

## 10. Open Questions / Design Decisions Still To Make

1. **JSON DSL vs Python API?** Python is more expressive but needs execution environment. JSON is faster to build. Decision gate: can we build a clean Python API in a week?

2. **Validation-first or generation-first?** Build the validator fully before running any models, or run models quickly against a rough validator and iterate?

3. **Feedback loop design:** How many rounds? What exactly does the model see — raw error strings, or structured feedback? Does it see the rendered image?

4. **Scope for paper:** Is Config A (mechanism IQ test) enough for a paper? Or do we need the feedback loop experiment to make the thesis?

5. **Part library curation:** Who curates the ~200 Technic parts? What metadata do we need?

6. **Aesthetic tasks:** Include now or defer? Including them makes the benchmark richer but adds VLM eval complexity.
