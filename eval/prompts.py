"""
Benchmark prompt set — 20 prompts across 4 difficulty tiers.
Each prompt is designed to be unambiguous and verifiable.
"""

PROMPTS = [
    # ── Tier 1: Simple primitives ──────────────────────────────────────────
    # Expected success rate: ~90%+
    {
        "id": "t1_01",
        "tier": 1,
        "prompt": "A cube 20mm × 20mm × 20mm.",
    },
    {
        "id": "t1_02",
        "tier": 1,
        "prompt": "A solid cylinder 10mm in diameter and 30mm tall.",
    },
    {
        "id": "t1_03",
        "tier": 1,
        "prompt": "A solid sphere with a radius of 15mm.",
    },
    {
        "id": "t1_04",
        "tier": 1,
        "prompt": "A rectangular box 60mm long, 40mm wide, and 15mm tall.",
    },
    {
        "id": "t1_05",
        "tier": 1,
        "prompt": "A flat disk 50mm in diameter and 5mm thick.",
    },

    # ── Tier 2: Single part with features ──────────────────────────────────
    # Expected success rate: ~60–80%
    {
        "id": "t2_01",
        "tier": 2,
        "prompt": (
            "A rectangular plate 50mm × 30mm × 5mm with a single circular "
            "hole 8mm in diameter centered on the plate."
        ),
    },
    {
        "id": "t2_02",
        "tier": 2,
        "prompt": (
            "A solid cylinder 30mm in diameter and 20mm tall with a coaxial "
            "through-hole 10mm in diameter."
        ),
    },
    {
        "id": "t2_03",
        "tier": 2,
        "prompt": (
            "An L-shaped bracket: one arm 60mm long, the other arm 40mm long, "
            "both arms 20mm wide and 5mm thick."
        ),
    },
    {
        "id": "t2_04",
        "tier": 2,
        "prompt": (
            "A square plate 60mm × 60mm × 4mm with four circular holes 5mm in "
            "diameter, one near each corner, each hole center 8mm from the "
            "nearest two edges."
        ),
    },
    {
        "id": "t2_05",
        "tier": 2,
        "prompt": (
            "A disk 50mm in diameter and 8mm thick with six 4mm-diameter holes "
            "equally spaced on a 38mm-diameter bolt circle."
        ),
    },

    # ── Tier 3: Multi-feature parts ────────────────────────────────────────
    # Expected success rate: ~30–50%
    {
        "id": "t3_01",
        "tier": 3,
        "prompt": (
            "A flanged cylinder: a 20mm-diameter shaft 30mm tall sitting on a "
            "40mm-diameter flange 6mm thick. The flange has four 4mm holes "
            "equally spaced on a 32mm bolt circle."
        ),
    },
    {
        "id": "t3_02",
        "tier": 3,
        "prompt": (
            "A hollow rectangular box with outer dimensions 60mm × 50mm × 40mm, "
            "wall thickness 3mm on all sides, open on the top face."
        ),
    },
    {
        "id": "t3_03",
        "tier": 3,
        "prompt": (
            "A T-shaped cross-section bracket: a 80mm-wide horizontal top bar "
            "and a 40mm-tall vertical stem, all 6mm thick and 20mm deep "
            "(into the page)."
        ),
    },
    {
        "id": "t3_04",
        "tier": 3,
        "prompt": (
            "A stepped shaft with three coaxial cylinders stacked: "
            "bottom section 20mm diameter × 10mm tall, "
            "middle section 14mm diameter × 20mm tall, "
            "top section 10mm diameter × 15mm tall."
        ),
    },
    {
        "id": "t3_05",
        "tier": 3,
        "prompt": (
            "A rectangular plate 80mm × 60mm × 8mm with a rectangular pocket "
            "milled into the top face: the pocket is 60mm × 40mm × 4mm deep "
            "and centered on the plate."
        ),
    },

    # ── Tier 4: Complex functional parts ───────────────────────────────────
    # Expected success rate: ~5–20%
    {
        "id": "t4_01",
        "tier": 4,
        "prompt": (
            "A spur gear with 20 teeth, module 2mm (so pitch diameter 40mm), "
            "face width 10mm, and a central bore 8mm in diameter."
        ),
    },
    {
        "id": "t4_02",
        "tier": 4,
        "prompt": (
            "A hex bolt: a regular hexagonal head 13mm across flats and 8mm "
            "tall, with a cylindrical shaft 10mm in diameter and 30mm long "
            "below the head."
        ),
    },
    {
        "id": "t4_03",
        "tier": 4,
        "prompt": (
            "A 90-degree pipe elbow: 15mm inner diameter, 2mm wall thickness, "
            "with 25mm-long straight sections on each end of the bend. "
            "The bend centerline radius is 20mm."
        ),
    },
    {
        "id": "t4_04",
        "tier": 4,
        "prompt": (
            "A helical compression spring: 20mm outer diameter, 1.5mm wire "
            "diameter, 10 active coils, 50mm free length, with flat ground "
            "ends."
        ),
    },
    {
        "id": "t4_05",
        "tier": 4,
        "prompt": (
            "A countersunk screw hole pattern: a flat plate 80mm × 60mm × 6mm "
            "with four countersunk holes arranged in a rectangle "
            "(60mm × 40mm centers). Each hole is 3.5mm diameter, "
            "countersunk at 90° to 6.5mm diameter."
        ),
    },
]

if __name__ == "__main__":
    from tabulate import tabulate
    rows = [(p["id"], p["tier"], p["prompt"][:80] + "...") for p in PROMPTS]
    print(tabulate(rows, headers=["ID", "Tier", "Prompt (truncated)"], tablefmt="rounded_grid"))
    print(f"\nTotal: {len(PROMPTS)} prompts across {len(set(p['tier'] for p in PROMPTS))} tiers")
