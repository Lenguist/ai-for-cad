import cadquery as cq

# --- Part 1: Cylinder ---
part_1_radius = 0.005 * 0.01  # Sketch radius scaled
part_1_height = 0.3

part_1 = cq.Workplane("XY").circle(part_1_radius).extrude(part_1_height)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.0025, 0.0025, 0))

# --- Assembly (if needed, based on the single part) ---
# In this case, there's only one part, so no assembly is needed.
# If there were multiple parts, you would use .union() or .cut() to combine them.

# --- Final Result ---
result = part_1
cq.exporters.export(result, './stlcq/0089/00894670.stl')