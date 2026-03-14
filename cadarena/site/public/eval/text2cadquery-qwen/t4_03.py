import cadquery as cq

# --- Part 1: 90-degree pipe elbow ---
outer_radius = 0.025 * 0.75  # Scaled outer radius
inner_radius = 0.015 * 0.75  # Scaled inner radius
wall_thickness = 0.002 * 0.75  # Scaled wall thickness
straight_length = 0.025 * 0.75  # Scaled straight length
total_length = 0.75 * 0.75  # Scaled total length
extrude_depth = 0.002

part_1 = (
    cq.Workplane("XY")
    .moveTo(straight_length, 0)
    .lineTo(total_length - straight_length, 0)
    .threePointArc((total_length, straight_length), (total_length - straight_length, straight_length))
    .lineTo(straight_length, straight_length)
    .threePointArc((0, straight_length), (straight_length, straight_length))
    .close()
    .extrude(extrude_depth)
)

# Create the inner cylinder to cut
inner_cylinder = (
    cq.Workplane("XY")
    .moveTo(straight_length, 0)
    .lineTo(total_length - straight_length, 0)
    .threePointArc((total_length, straight_length), (total_length - straight_length, straight_length))
    .lineTo(straight_length, straight_length)
    .threePointArc((0, straight_length), (straight_length, straight_length))
    .close()
    .extrude(extrude_depth)
    .faces(">Z").workplane().circle(inner_radius).cutThruAll()
)

# Subtract the inner cylinder from the outer shape
part_1 = part_1.cut(inner_cylinder)

# --- Assembly ---
assembly = part_1

# Export to STL
cq.exporters.export(assembly, "./stlcq/0083/00834600.stl")