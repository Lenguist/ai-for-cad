import cadquery as cq

# --- Part 1: Rectangular Box ---
length = 0.6 * 0.6  # Scaled length
width = 0.4 * 0.6   # Scaled width
height = 0.15

part_1 = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.12, 0.12, 0))

# --- Assembly ---
assembly = part_1

# Export to STL
cq.exporters.export(assembly, "./stlcq/0038/00387900.stl")