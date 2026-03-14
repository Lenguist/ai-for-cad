import cadquery as cq

# --- Part 1: Rectangular Box ---
outer_width = 0.06 * 0.06  # Scaled width
outer_height = 0.05 * 0.06  # Scaled height
inner_offset = 0.0037 * 0.06  # Scaled offset for inner rectangle
depth = 0.04

# Create the outer rectangle and extrude it to form a solid
outer_rect = cq.Workplane("XY").rect(outer_width, outer_height).extrude(depth)

# Create the inner rectangle (offset) and extrude it to form a solid
inner_rect = cq.Workplane("XY").rect(outer_width - 2 * inner_offset, outer_height - 2 * inner_offset).extrude(depth)

# Cut the inner solid from the outer solid to create the hollow box
part_1 = outer_rect.cut(inner_rect)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.0089, 0.0089, 0))

# --- Assembly ---
assembly = part_1

# Export to STL
cq.exporters.export(assembly, "./stlcq/0060/00600810.stl")