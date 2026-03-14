import cadquery as cq

# --- Part 1: Rectangular Plate ---
part_1_length = 0.08 * 0.08  # Scaled length
part_1_width = 0.06 * 0.08   # Scaled width
part_1_height = 0.008

part_1 = (
    cq.Workplane("XY")
    .rect(part_1_length, part_1_width)
    .extrude(part_1_height)
)

# --- Part 2: Rectangular Cutout ---
part_2_length = 0.06 * 0.06  # Scaled length
part_2_width = 0.04 * 0.06   # Scaled width
part_2_height = 0.004

part_2 = (
    cq.Workplane("XY")
    .rect(part_2_length, part_2_width)
    .extrude(-part_2_height)  # Extrude in the opposite direction for cutting
)

# --- Assembly: Cutout from Plate ---
assembly = part_1.cut(part_2.translate((0.01, 0.01, part_1_height)))

# --- Export to STL ---
cq.exporters.export(assembly, './stlcq/0073/00735900.stl')