import cadquery as cq

# --- Part 1: Spur Gear ---
outer_radius = 0.02 * 0.04  # Sketch radius scaled
inner_radius = 0.01 * 0.04  # Inner hole radius scaled
tooth_width = (0.025 - 0.015) * 0.04  # Width of each tooth
num_teeth = 20
extrude_depth = 0.01

part_1 = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(extrude_depth)
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutThruAll()
)

# Create the teeth profile
tooth_profile = (
    cq.Workplane("XY")
    .moveTo(0.01 * 0.04, 0)
    .lineTo(0.02 * 0.04, 0)
    .lineTo(0.02 * 0.04, tooth_width)
    .lineTo(0.015 * 0.04, tooth_width)
    .lineTo(0.01 * 0.04, 0)
    .close()
)

# Extrude the teeth profile to create the teeth
tooths = tooth_profile.extrude(extrude_depth)

# Position the teeth on the gear
for i in range(num_teeth):
    angle = i * 360 / num_teeth
    rotated_tooths = tooths.rotate((0, 0, 0), (0, 0, 1), angle)
    part_1 = part_1.union(rotated_tooths)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.005, 0.005, 0))

# --- Assembly ---
assembly = part_1

# Export to STL
cq.exporters.export(assembly, "./stlcq/0079/00795900.stl")