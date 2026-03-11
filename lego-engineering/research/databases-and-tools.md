# LEGO Technical Resources: Databases, Simulators & Tools

---

## 1. Part Databases / Libraries

### LDraw Parts Library
**URL:** https://ldraw.org / https://library.ldraw.org
**Download:** https://library.ldraw.org/library/updates/complete.zip

The canonical open-source 3D part library for LEGO. Foundation used by virtually every non-commercial LEGO CAD tool.

- 3D geometry for individual LEGO parts: plain-text `.dat` files describing triangles, quads, lines
- Covers full LEGO catalog: Technic beams, axles, gears, connectors, Mindstorms, flex elements
- 17,000+ total files (parts, subparts, primitives); grows continuously
- 2025-08 update alone added 532 new parts
- **License:** Creative Commons (CCAL v2.0 / CC BY 4.0 / CC0 — author's choice). Freely redistributable.
- **Benchmark relevance:** Single most important resource. Every part has precise geometry. LegoGPT uses this format (`.ldr`).

### Rebrickable Database
**URL:** https://rebrickable.com
**Downloads:** https://rebrickable.com/downloads/ (free CSV, updated daily)
**API:** https://rebrickable.com/api/v3/docs/

Comprehensive catalog of all official LEGO sets, parts, minifigs, and inventories. Metadata only (no geometry — use LDraw for that).

CSV downloads include:
- `parts.csv` — all parts with numbers, names, categories
- `sets.csv` — all sets with year, theme, part count
- `inventory_parts.csv` — exactly which parts (and colors) are in each set
- `colors.csv` — all colors with RGB values
- `part_relationships.csv` — mold equivalences

**Benchmark relevance:** Best source for part IDs, set inventories, color data. Combine with LDraw for complete picture.

### BrickLink Catalog
**URL:** https://www.bricklink.com/catalog.asp
**API:** https://www.bricklink.com/v2/api/welcome.page
**Technic parts:** https://www.bricklink.com/catalogList.asp?catID=36

World's largest LEGO marketplace (owned by LEGO Group since 2019). Catalog covers every part/set ever made with BL item numbers, pricing, images.

- Third numbering system (alongside LEGO Design IDs and LDraw filenames — mapping tables exist)
- REST API, OAuth 1.0. Python wrappers: `python-bricklink-api`, `bricklink_py`
- Not freely bulk-downloadable like Rebrickable
- **Benchmark relevance:** Part name/ID cross-referencing.

### LEGO Official Part / Design ID System
LEGO has two internal ID systems:
- **Design ID:** Identifies the mold (4-5 digits, e.g. 3001 = classic 2×4 brick). Molded into part undersides since ~1985.
- **Element ID:** Identifies part + color combo (6-7 digits, SAP system).

LEGO does not publish an official geometry library. LDraw is the community's reverse-engineered recreation. LDraw filenames mostly match Design IDs but not perfectly.

---

## 2. LEGO CAD Software

### BrickLink Studio (formerly Stud.io)
**URL:** https://www.bricklink.com/v2/build/studio.page
**Status:** Free, closed-source, Windows/macOS. Official tool, owned by LEGO Group.

- Full visual LEGO CAD editor with complete BrickLink part catalog
- Photorealistic rendering (PovRay-based), building instruction generator
- **Export:** LDraw (`.ldr`/`.mpd`), LXFML (`.lxf`), POV-Ray, PDF
- **No scripting API** — GUI only
- **Benchmark relevance:** Good for viewing/validating LDraw outputs. Not automatable.

### LeoCAD
**URL:** https://www.leocad.org
**GitHub:** https://github.com/leozide/leocad
**Status:** Free, open-source (GPL v2), cross-platform.

- LDraw-compatible editor, handles 4,000+ piece models
- **Export:** LDraw, OBJ, COLLADA DAE, 3DS, BrickLink XML
- **Benchmark relevance:** Best open-source option for LDraw → OBJ/COLLADA conversion in rendering pipelines. Can be invoked via CLI.

### LDView
**URL:** https://tcobbs.github.io/ldview/
**Status:** Free, open-source viewer/renderer.

Can export LDraw `.dat` files to STL, 3DS, POV-Ray. Useful for converting individual parts to STL for geometry processing.

### LDCad
**URL:** http://www.melkert.net/LDCad
**Status:** Free (not fully open-source), Windows/Linux.

Most powerful LDraw editor for complex models, especially flexible parts (hoses, Technic flex cables). No scripting API.

---

## 3. Physics Simulation Tools

### Virtual Robotics Toolkit (VRT)
**URL:** https://www.virtualroboticstoolkit.com/
**Status:** Commercial, paid. Windows only.

Most capable LEGO physics simulator. Designed for FLL/WRO robotics.
- Imports LDraw files, assigns physical properties (mass, collision geometry)
- **Does simulate gear trains and drive trains through LDraw models**
- Runs EV3-G/NXT-G programs in simulation
- Focused on Mindstorms/robotics, not general Technic kinematics
- **Benchmark relevance:** Only tool found that does real mechanism simulation from LDraw input, but commercial and robotics-focused.

### Sariel's Gear Ratio Calculator
**URL:** https://gears.sariel.pl/
**Status:** Free web tool.

Covers 20 Technic gear types including differentials and turntables. Calculates gear ratios between any two meshing gears given axle positions. Android app also available.

### TechnicBrickPower Gearing Tool
**URL:** https://technicbrickpower.com
**Status:** Free web tool.

Accepts `.ldr` files, identifies gearing components, calculates full gear train ratios, **visualizes gear system in motion**. Closest thing to a free Technic mechanism simulator.

### marian42/gears
**URL:** https://github.com/marian42/gears / https://marian42.de/gears/
**Status:** Free, open-source web app.

Finds gear sequences for a target transmission ratio. Calculates axle spacing for any gear pair.

### Key Gap
**No free/open full kinematic simulation for arbitrary Technic mechanisms (gear trains + linkages + pneumatics) exists.** VRT handles Mindstorms robots but not general Technic kinematics. This is a significant gap for validation in a benchmark.

---

## 4. Blender Plugins

### ImportLDraw (TobyLobster)
**GitHub:** https://github.com/TobyLobster/ImportLDraw
Supports `.mpd`, `.ldr`, `.l3b`, `.dat`. PBR materials (brick, transparent, rubber, chrome, metal, etc.). Works Blender 2.81–4.5+.

### ldr_tools_blender (ScanMountGoat)
**GitHub:** https://github.com/ScanMountGoat/ldr_tools_blender
Optimized for very large models via geometry instancing. More memory-efficient for large scenes. Blender 4.1+.

---

## 5. Programmatic Assembly Tools (Python)

### pyldraw (michaelgale)
**GitHub:** https://github.com/michaelgale/pyldraw

Python library for creating and manipulating LDraw files programmatically. Place bricks at positions and orientations, output `.ldr` files. **Core tool for programmatic LEGO assembly.**

### python-ldraw (rienafairefr)
**GitHub:** https://github.com/rienafairefr/python-ldraw

Makes the complete LDraw parts library importable as Python modules. Older project.

---

## 6. LDraw File Format

**Spec:** https://www.ldraw.org/article/218.html
**MPD spec:** https://www.ldraw.org/article/47.html

Plain text, UTF-8, one command per line.

**Line types:**
- `0` — comment or META command
- `1` — sub-file reference: `1 <colour> x y z a b c d e f g h i <filename>` (position + 3×3 rotation matrix + part filename)
- `2` — line segment
- `3` — triangle
- `4` — quadrilateral
- `5` — optional/conditional edge

**Units:** 1 LDU = 0.4mm. Standard stud pitch = 20 LDU = 8mm.
**Coordinate system:** Y-axis points **down** (unusual).
**File extensions:** `.dat` (part), `.ldr` (model), `.mpd` (multi-part document)

---

## 7. Technic Part Coverage in LDraw

LDraw comprehensively covers Technic:
- **Axles:** lengths 2–32 studs, with/without stop
- **Beams:** straight, L-shape, T-shape, curved, triangle — many lengths
- **Gears:** 8T, 12T, 16T, 20T, 24T, 36T, 40T spur; bevel 12T/20T; worm; rack; clutch; differentials; turntables
- **Pins:** friction/frictionless, long/short, with/without axle hole
- **Connectors, bushes, CV joints, universal joints**
- **Pneumatics:** pumps, cylinders, switches, hoses
- **Motors, sensors:** Mindstorms/Powered Up

---

## 8. Curated Lists

- **awesome-lego-machine-learning:** https://github.com/360er0/awesome-lego-machine-learning — best starting point for ML+LEGO research
- **awesome-lego:** https://github.com/ad-si/awesome-lego — broader tools/libraries/APIs/datasets catalog

---

## Summary: Recommended Stack for Benchmark

| Resource | Use |
|---|---|
| LDraw Parts Library | Ground truth part geometry; output format for AI |
| Rebrickable CSV | Part/set metadata, color data, ID cross-reference |
| pyldraw | Programmatic LDraw read/write in Python |
| LeoCAD CLI | LDraw → OBJ/COLLADA for rendering pipeline |
| ImportLDraw / ldr_tools_blender | Render in Blender for visual evaluation |
| Sariel / TechnicBrickPower | Validate Technic gear train correctness |
| LegoGPT methodology | State-of-the-art generation baseline + StableText2Lego dataset |
