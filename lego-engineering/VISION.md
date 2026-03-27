# MechE-Claude — Vision & Build Plan
*Last updated: 2026-03-27*

---

## The Core Idea

An AI agent that can design physical LEGO mechanisms from a natural language prompt — and verify that they actually work.

```
"build me a working LEGO escalator using gears and motors"
        ↓
  Claude Code agent
        ↓
  action loop (place, inspect, simulate, iterate)
        ↓
  valid LDraw assembly  +  simulation result
        ↓
  "escalator belt moves at 0.3m/s, structurally sound"
```

This is different from prior work (BrickGPT, text-to-LEGO) because:
- Those systems generate assemblies that **look like** something
- We generate assemblies that **work like** something
- Functional correctness ("does the escalator escalate?") is the bar, not visual resemblance

---

## Why This Is Interesting

**Unlike Voyager (Minecraft agent):** Minecraft doesn't transfer to anything. LEGO Technic does. A system that can design a working LEGO robodog is one step away from designing an actual robot — same architecture, better physics engine.

**Unlike BrickGPT:** They fine-tune a model on known assemblies, asking "given this 3D shape, cover it with bricks." We ask "given this functional goal, design a mechanism that achieves it." Completely different problem.

**The optimization angle:** Once the agent can build working mechanisms, you can close the optimization loop:
```
"build the fastest walking LEGO robodog possible"
  → agent builds v1 → sim says 0.3 m/s
  → agent reasons why (leg length? gear ratio? weight distribution?)
  → agent builds v2 → sim says 0.5 m/s
  → ...
```
Claude as the search heuristic, simulator as the objective function. Closer to FunSearch than AlphaFold.

**The real-world path:**
```
LEGO robodog (proof of concept)
  → LEGO robodog optimized for terrain X (optimization works)
    → actual robot designed by same system (swap simulator)
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Claude Code Agent                   │
│  (receives prompt, calls tools, reasons, iterates)  │
└──────────────────────┬──────────────────────────────┘
                       │ tool calls
┌──────────────────────▼──────────────────────────────┐
│               Agent Environment (Python)             │
│  search_parts · place · remove · inspect · simulate  │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                        ▼
┌─────────────────┐    ┌───────────────────────┐
│  Assembly State │    │   Evaluation Layers    │
│  (LDraw file)   │    │                        │
│                 │    │  L1: Semantic valid    │
│  parts[]        │    │  L2: Static physical   │
│  positions      │    │  L3: Kinematic sim     │
│  connections    │    │  L4: Full physics      │
└────────┬────────┘    └───────────────────────┘
         │
         ▼
┌─────────────────┐
│    Website      │
│ (inspection +   │
│  demo layer)    │
│                 │
│ Three.js viewer │
│ agent log       │
│ human feedback  │
└─────────────────┘
```

**Key principle:** The website is NOT the agent runtime. It's a window into it. The agent runs locally via Claude Code. The website reads the agent's output files and renders them. Human feedback is written to a file; the agent picks it up on the next iteration.

---

## The Four Evaluation Layers

### L1 — Semantic Validator
*Does this connection make sense in principle?*

Runs before compilation. Fast. Pure logic.
- Does part type A have a connection point of type X?
- Can a 1x4 brick sit on a 1x2 brick? → yes (partially supported)
- Can a standard brick connect to an axle hole? → no

Returns: list of semantic errors with specific part IDs and reasons.

### L2 — Physical Validator (Static)
*Given actual positions, do parts fit together physically?*

Runs after compilation to LDraw coordinates.
- Do any bricks overlap in 3D space?
- Does every non-floor brick have at least one stud supported?
- For Technic: do pin holes actually align between beams?
- For gears: is center distance correct for tooth mesh?

Returns: list of collisions / unsupported parts with positions.

### L3 — Kinematic Simulator
*Does the mechanism move as intended?*

Builds a motion propagation graph from the assembly.
- Motor → axle spins at RPM
- Gears on axle spin → check tooth mesh contact → drive other gears at ratio
- Rack in contact with gear → converts to linear motion
- Each step: verify contact exists before propagating

Returns: motion state (which parts move, at what speed/direction), stall detection.

### L4 — Physics Simulator *(later)*
*Do forces and torques balance? Does it hold together under load?*

Full rigid body dynamics. Contact forces. Friction. Structural failure.
This is the "final boss" — only needed for optimization and sim-to-real.

---

## The Assembly DSL

Claude writes assemblies in a mid-level DSL. Not raw LDraw coordinates (too low-level for an LLM), not pure natural language (too ambiguous). The DSL compiles down to LDraw.

**Phase 1 (basic bricks):**
```json
{
  "bricks": [
    {"id": "b1", "type": "2x4", "pos": [0, 0, 0], "rot": 0},
    {"id": "b2", "type": "2x4", "pos": [0, 0, 1], "rot": 0},
    {"id": "b3", "type": "1x4", "pos": [2, 0, 2], "rot": 90}
  ]
}
```
`pos` = [stud_x, stud_y, layer], `rot` = 0/90/180/270.
Connections are implicit — if studs align, they connect.
Compiler resolves to LDraw units (1 stud = 20 LDraw units, 1 brick = 24 LDraw units height).

**Phase 2 (Technic, connection graph):**
```json
{
  "parts": [
    {"id": "axle1", "type": "axle-4", "pos": [0,0,0], "dir": [1,0,0]},
    {"id": "gear_small", "type": "gear-8t",  "on": "axle1", "at": 1},
    {"id": "gear_large", "type": "gear-24t", "mesh_with": "gear_small", "on": "axle2", "at": 1},
    {"id": "axle2",  "type": "axle-4", "parallel_to": "axle1"}
  ]
}
```
Semantic connections. Compiler solves for positions (gear center distance = r1+r2).

---

## Agent Action Space

Tools available to Claude Code:

```python
search_parts(query: str) -> list[Part]
# fuzzy search: "gear with ~20 teeth", "1x4 brick", "axle longer than 6"

get_part(id: str) -> Part
# full spec: connection points, dimensions, LDraw number, description

look_at(target: str, angle: str = "iso") -> image
# render image of a single part or the current assembly
# angles: "iso", "top", "front", "side"

place(spec: dict) -> Result
# add part(s) to assembly. accepts single part or list.
# returns: ok or list of errors (semantic + physical)

remove(part_id: str) -> Result
# remove a part from the current assembly

group(part_ids: list, name: str) -> None
# name a set of parts as a sub-assembly for reference

inspect(angle: str = "iso") -> AssemblyState
# returns: rendered image + JSON state (parts, connections, current errors)

simulate(level: int = 2) -> SimResult
# level 1: semantic only
# level 2: semantic + static physical
# level 3: + kinematic (requires motor defined)
# returns structured result Claude can reason about

save(filename: str) -> str
# write LDraw file to workspace, triggers website refresh

feedback() -> str | None
# check if human has left feedback in workspace
# returns feedback string or None
```

**Batch commands:** Claude can send a list of `place` calls at once and gets back a summary. It doesn't need to round-trip for every brick.

**Skill library (Voyager-style):** successful sub-assemblies (e.g. "1:4 gear reduction", "motor mount bracket") saved as named, reusable components. Claude can call them in future builds.

---

## Build Phases

### Phase 1: Basic LEGO Bricks ← START HERE
*Goal: Claude Code can receive "stack three 2x4 bricks in a staggered pattern" and produce a valid LDraw file that renders on the website.*

Components to build:
- [ ] **Parts data** — JSON for standard bricks (1x1→2x8, plates). Footprint, height, LDraw part number.
- [ ] **Compiler** — `pos + rot` → LDraw absolute coordinates. Grid math only.
- [ ] **L1 validator** — brick type exists, pos is integer, rot is 0/90/180/270
- [ ] **L2 validator** — overlap check (3D grid occupancy), support check (at least 1 stud below)
- [ ] **Agent tools** — `place`, `remove`, `inspect`, `save` as Python functions
- [ ] **Website watcher** — filesystem watch → auto-refresh Three.js viewer
- [ ] **Agent log panel** — website shows Claude's reasoning step by step

Success metric: Claude Code builds a structurally valid wall, staircase, or simple house shape without human intervention.

### Phase 2: Technic Mechanisms
*Goal: Claude Code can build a 1:4 gear reduction that the kinematic sim confirms works.*

Components to build:
- [ ] **Technic parts data** — axles, gears, beams, pins, motors. Connection point geometry.
- [ ] **DSL v2** — connection graph (semantic). `on`, `mesh_with`, `parallel_to`, `at`.
- [ ] **Compiler v2** — resolve positions from connection semantics. Gear center distance solver.
- [ ] **L1 validator** — connection type compatibility (axle-through vs pin-through vs stud)
- [ ] **L2 validator** — updated for Technic geometry (axle hole alignment, gear overlap)
- [ ] **L3 kinematic sim** — motion propagation graph. Motor → gear train → output.
- [ ] **`simulate(level=3)`** — returns RPM, direction, stall state

Success metric: "build a 1:4 gear ratio drivetrain with a medium motor" → sim reports output shaft at 95 RPM (380/4), direction correct.

### Phase 3: Complex Mechanisms + Agent Loop
*Goal: Claude Code builds a working escalator (belt + motor + structure) with iterative sim feedback.*

Components to build:
- [ ] **Skill library** — save/load named sub-assemblies as reusable tools
- [ ] **Human feedback loop** — website feedback input → file → agent picks up
- [ ] **Multi-round logging** — website shows each agent iteration with diff
- [ ] **L3 sim extended** — chain/belt drives, linear actuators, compound gear trains

Success metric: "build a working LEGO escalator" → Claude iterates 3-5 times → sim confirms belt moves → human can watch the iteration in real time on website.

### Phase 4: Optimization Loop
*Goal: Claude optimizes a robodog walking mechanism for speed on flat terrain.*

Components to build:
- [ ] **Objective function interface** — `simulate` returns scalar metric (speed, efficiency, etc.)
- [ ] **Iteration history** — agent tracks all versions + scores
- [ ] **Design parameter reasoning** — agent explains why it's changing what
- [ ] **L4 physics sim** — rigid body, contact forces (PyBullet or MuJoCo)

Success metric: starting from a naive robodog, agent improves walking speed by >50% over 10 iterations with sim-confirmed results.

### Phase 5: Public Demo + Paper
- Clean website demo anyone can try
- Benchmark task set (T1→T5 difficulty levels)
- Comparison: Claude vs other models vs human designers
- Paper: "LLM-driven iterative mechanical design with simulation feedback"

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Agent | Claude Code (local) | already is the agent loop |
| Agent tools | Python | fast iteration, good libs |
| Assembly format | LDraw (.ldr) | universal LEGO standard |
| 3D rendering | Three.js + LDrawLoader | already working |
| Parts data | JSON | simple, LLM-readable |
| L3 sim | Python (custom) | simple graph traversal |
| L4 sim | PyBullet or MuJoCo | later |
| Website | Next.js (existing) | already built |
| Hosting | Vercel | existing setup |

---

## Directory Structure (target)

```
lego-engineering/
├── VISION.md                  ← this file
├── agent/
│   ├── tools.py               ← all agent tool functions
│   ├── workspace/             ← agent's working directory
│   │   ├── assembly.json      ← current DSL spec
│   │   ├── assembly.ldr       ← compiled LDraw (website reads this)
│   │   ├── sim_result.json    ← latest simulation output
│   │   └── feedback.txt       ← human feedback (agent polls this)
│   └── skills/                ← saved sub-assemblies (skill library)
├── compiler/
│   ├── compiler.py            ← DSL → LDraw
│   ├── validator_semantic.py  ← L1
│   └── validator_physical.py  ← L2
├── simulator/
│   ├── kinematic.py           ← L3
│   └── physics.py             ← L4 (later)
├── parts/
│   ├── bricks.json            ← standard LEGO bricks
│   └── technic.json           ← Technic parts (phase 2)
└── site/                      ← Next.js website
    ├── app/
    │   ├── viewer/            ← Three.js LDraw viewer (done)
    │   ├── parts/             ← parts browser (done)
    │   └── build/             ← agent log + feedback UI
    └── public/
        └── ldraw/             ← LDraw parts files (done)
```

---

## What's Already Built

- [x] Three.js LDraw renderer (viewer page — renders any part, orbit controls, auto-rotation)
- [x] Parts browser (26 Technic parts, search + filter + detail view)
- [x] LDraw parts files (135 .dat files for all 26 Technic parts + dependencies)
- [x] Next.js site structure with all 5 routes
- [x] Parts API route (`/api/parts`)

---

## First Session Goal

Build Phase 1:
1. `parts/bricks.json` — standard brick types with footprints + LDraw IDs
2. `compiler/compiler.py` — pos/rot grid → LDraw file
3. `compiler/validator_semantic.py` — type exists, valid pos/rot
4. `compiler/validator_physical.py` — overlap + support check
5. `agent/tools.py` — place, remove, inspect, save
6. Test: run Claude Code with "build a 2x4 staircase" → valid LDraw → renders

*Technic comes in Phase 2. Kinematics in Phase 3. Everything is proven on simple bricks first.*
