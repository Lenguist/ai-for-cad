# LEGO Technic Bench — Mar 11 Demo

Flask web app: parts browser + 3D assembly visualizer. First step toward an AI mechanism design benchmark.

## Run

```bash
pip install flask
python app.py
# → http://localhost:5050
```

## What's built

**`/` and `/parts`** — Parts library browser. 23 curated Technic parts (beams, gears, axles, pins, rack, connectors). Filter by category, search by name. Images from BrickLink CDN with emoji fallback.

**`/assemble`** — Assembly editor + 3D viewer.
- JSON editor (Cmd+Enter to run)
- Four built-in examples: 3:1 gear pair, rack & pinion, 9:1 compound gear train, beam frame
- Three.js schematic viewer: beams=gray boxes with hole dots, gears=gold cylinders, axles=dark rods, rack=orange with teeth marks. Orbit/zoom/pan.
- Validator: checks part types exist, no duplicate IDs, basic overlap detection
- Kinematic analyser: detects meshing gear pairs by center distance (radius1+radius2), computes gear ratios, detects rack-and-pinion → flags rotational→linear motion conversion

## Assembly format

```json
{
  "name": "My Assembly",
  "parts": [
    {"id": "b1", "type": "beam-7", "pos": [0, 0, 0], "axis": "x"},
    {"id": "g1", "type": "gear-24t", "pos": [3, 0, 0], "axis": "y"}
  ]
}
```

- `pos`: [x, y, z] in stud units (1 stud = 8mm). Technic is a regular cubic grid.
- `axis`: which direction the part extends / axle points (`x`, `y`, `z`)
- For beams: `pos` is the position of hole[0]; beam extends along `axis`
- For gears: `pos` is the center; `axis` is the axle direction
- For axles/pins: `pos` is one end; extends along `axis`

## Parts

| ID | Category | Key spec |
|---|---|---|
| beam-3/5/7/9/11/15 | beam | length in holes |
| gear-8t/16t/24t/40t | gear | teeth, radius_studs |
| gear-worm | gear | 1T effective |
| rack-4 | rack | 4 studs long |
| axle-3/4/5/6/8/10 | axle | length in studs |
| pin / pin-friction / pin-long | pin | standard Technic pins |
| bush / connector-2x2 | connector | spacer / 90° join |

## Gear meshing distances (stud units)

| Pair | Distance |
|---|---|
| 8T + 8T | 2 |
| 8T + 24T | 4 |
| 16T + 24T | 5 |
| 24T + 24T | 6 |
| 8T + 40T | 6 |

## Next steps

- Add more parts (L-beams, turntables, differentials, pneumatics)
- Hook up an LLM to write assemblies given a prompt, with validator feedback loop
- Replace schematic rendering with real LDraw geometry (via pyldraw + LeoCAD → OBJ)
- Add task prompts + evaluation (does this assembly achieve the required gear ratio / motion type?)
