import cadquery as cq

# --- Part 1: Flange and Cylinder ---
flange_radius = 0.02 * 0.04  # Scaled radius of the flange
cylinder_radius = 0.01 * 0.04  # Scaled radius of the cylinder
flange_height = 0.06
cylinder_height = 0.03
sketch_scale = 0.04

# Hole parameters (scaled)
hole_radius = 0.004 * sketch_scale
hole_centers = [
    (0.008 * sketch_scale, 0.012 * sketch_scale),
    (0.008 * sketch_scale, 0.028 * sketch_scale),
    (0.022 * sketch_scale, 0.012 * sketch_scale),
    (0.022 * sketch_scale, 0.028 * sketch_scale)
]

# Create the base shape (flange + cylinder)
part_1 = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_height)
)

# Cut the cylinder from the flange
part_1 = part_1.cut(cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height))

# Add holes to the flange
for center_x, center_y in hole_centers:
    part_1 = part_1.faces(">Z").workplane().pushPoints([(center_x - flange_radius, center_y - flange_radius)]).hole(2 * hole_radius)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.35, 0.35, 0.0))

# --- Assembly ---
assembly = part_1

# Export to STL
cq.exporters.export(assembly, "./stlcq/0079/00790900.stl")