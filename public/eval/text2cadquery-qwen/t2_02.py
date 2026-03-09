import cadquery as cq

# --- Part 1: Cylinder with Hole ---
outer_radius = 0.015 * 0.03  # Sketch radius scaled
inner_radius = 0.005 * 0.03  # Inner hole radius scaled
height = 0.2

part_1 = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .cut(cq.Workplane("XY").circle(inner_radius).extrude(height))
)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.015, 0.015, 0))

# --- Assembly ---
assembly = part_1

# Export to STL
cq.exporters.export(assembly, "./stlcq/0047/00478960.stl")