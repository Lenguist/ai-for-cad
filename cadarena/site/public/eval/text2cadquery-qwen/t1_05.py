import cadquery as cq

# --- Part 1: Disk ---
part_1_radius = 0.025 * 0.05  # Sketch radius scaled
part_1_height = 0.005

part_1 = cq.Workplane("XY").circle(part_1_radius).extrude(part_1_height)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.35, 0.35, 0))

# --- Assembly (if needed, based on the single part) ---
# In this case, there's only one part, so no assembly is needed.
# If there were multiple parts, you would use .union() or .cut() to combine them.

# --- Final Result ---
result = part_1

cq.exporters.export(result, './stlcq/0047/00479860.stl')