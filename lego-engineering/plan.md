# Lego Mechanic Studio — Build Plan

**Vision:** User types a mechanism description → AI generates the assembly → site validates + visualizes it in 3D.
This is both a cool demo tool AND the actual benchmark runner for the paper.

**Live site:** lego-web-static.vercel.app

---

## Phase 1 — AI Generation (user prompts) [~1 day]

Turn the static site into a Vercel project with one serverless function.

### 1.1 Backend: `/api/generate` serverless function
- Input: `{ prompt: string }`
- Calls Claude Sonnet (`claude-sonnet-4-6`) with:
  - System prompt: parts library (full JSON) + assembly format instructions + mechanical facts
  - User message: the prompt
- Parses JSON from response
- Runs client-side validation before returning
- Returns: `{ assembly, reasoning, model, elapsed_ms }`
- Store `ANTHROPIC_API_KEY` as Vercel env var

### 1.2 Rate limiting
- Upstash Redis (same as cadarena setup)
- 3 generations/week anonymous
- 10 generations/week with email
- Same cookie-based upgrade flow as cadarena

### 1.3 UI changes
- Add a prompt input bar above the gallery strip
  - Placeholder: "Describe a mechanism... e.g. 'build a 9:1 gear reduction'"
  - "Generate ✦" button (calls /api/generate)
  - Loading state: spinning indicator while waiting
- On response: load assembly into editor, auto-compile, show 3D view
- Show model reasoning in results panel
- Keep gallery strip — prebuilt examples still useful

### 1.4 Convert to Vercel project with functions
- Currently: `lego-web-static/` (pure static)
- New structure:
  ```
  lego-web-static/
  ├── index.html          ← same frontend
  ├── api/
  │   └── generate.js     ← serverless function (Node, calls Anthropic SDK)
  └── vercel.json         ← updated routing
  ```
- Vercel auto-detects `api/` folder as serverless functions

---

## Phase 2 — Expanded Parts Library [~2-3 days]

### 2.1 Curate ~200 Technic parts
Current: 23 parts. Need to add:
- All beam lengths (1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 15) — straight + angular
- Angular/liftarm beams (3×5 L-shape, 2×4 L-shape, etc.)
- Cross blocks and perpendicular connectors
- All axle lengths (2, 3, 4, 5, 6, 7, 8, 10, 12)
- Axle connectors, axle joiners, half bushes
- Turntable (large + small)
- Linear actuator
- Differential gear housing
- Bevel gears (12T, 20T) — enable non-parallel axes
- Knob wheels — alternative worm-like meshing
- Chain links + sprockets (for chain drives)
- Pneumatic cylinder + pump (structural only, no simulation)

Each part needs: `id, name, category, length/radius/teeth, holes[], connection_points[], description`

### 2.2 3D mesh improvements
- Beams with actual hole geometry (already started)
- Bevel gears need angled tooth rendering
- Connectors need accurate shapes

### 2.3 Search interface upgrade
- With 200 parts, the left panel needs better UX
- Group by subcategory (beam, beam-angular, axle, gear-spur, gear-bevel, gear-worm, connector, actuator)
- "Insert into editor" button on part detail — appends a skeleton part JSON to the editor

---

## Phase 3 — Feedback Loop [~2 days]

This is the core research contribution: model sees validation errors and revises.

### 3.1 Multi-round generation
- After first generation, show validation results
- "Retry with feedback" button — sends original prompt + assembly + error list back to model
- Model revises and returns new assembly
- Show round history: Round 1 → Round 2 → Round 3
- Up to 3 rounds (configurable)

### 3.2 Error quality
- Current errors are already specific ("gear centers are 5.0 studs apart, need 4.0")
- Add: "did you mean to use gear-8t? its radius is 1, not 2"
- Add: missing connection suggestions ("gear-8t and gear-24t are 4 studs apart — did you mean to connect them?")

### 3.3 Round visualization
- Results panel shows per-round score
- 3D view animates transition between rounds (fade out / fade in)

---

## Phase 4 — Benchmark Mode [~1 day]

Connect the studio to the formal benchmark task set.

### 4.1 Task runner UI
- Tasks tab already lists all 20 tasks
- Add "Run" button per task → sends task prompt to /api/generate → validates → scores
- Show score (0/1/2) inline
- "Run all Tier N" button → runs all tasks in a tier sequentially
- Results table: task ID, score, rounds used, ratio achieved

### 4.2 Leaderboard
- Store results in Upstash Redis
- Show model vs. model comparison (Claude vs. GPT-4o vs. Gemini)
- This IS the paper's main result table

---

## Phase 5 — Multi-model comparison [~1 day]

Same as cadarena but for mechanisms.

### 5.1 Run same task on multiple models simultaneously
- Select models (Claude Sonnet, GPT-4o, Gemini 2.5)
- Show 3 assemblies side by side (or tabbed)
- Each gets validated + scored independently
- Highlight which model got the gear ratio right

### 5.2 Vote
- "Which assembly is better?" picker (same as cadarena)
- Store votes in Redis

---

## Tech Stack Summary

| Layer | Tool |
|---|---|
| Frontend | Vanilla JS + Three.js (no framework) |
| Hosting | Vercel static + serverless functions |
| AI | Claude Sonnet 4.6 (via Anthropic SDK in Node) |
| Rate limiting | Upstash Redis |
| 3D | Three.js r128 + OrbitControls |
| Parts data | Inline JSON (static) |
| Validation | Client-side JS (ported from Python) |

---

## Order of Attack

1. **Phase 1 first** — AI generation is the magic feature, unlocks everything else
2. **Phase 2 in parallel** — more parts makes generations more interesting, can do incrementally
3. **Phase 3** — feedback loop is the paper's thesis, needs Phase 1 working first
4. **Phase 4 + 5** — benchmark mode + multi-model, needed for the actual paper results

---

## Open Questions

1. **Rate limiting strategy:** Free tier with email unlock same as cadarena? Or just open for now while building?
2. **Parts metadata depth:** For 200 parts, do we need full connection point geometry or just category + dimensions?
3. **Model context size:** At 200 parts × ~100 chars each = ~20k tokens. Fine for Sonnet. Need to check if full library fits or if we need search tool.
4. **Domain:** Keep `lego-web-static.vercel.app` or get a real domain? (`mechbench.dev`? `legomechanic.dev`?)
