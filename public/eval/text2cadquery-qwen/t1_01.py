import cadquery as cq

# --- Part 1: Cube ---
part_1_size = 0.2 * 0.2  # Sketch size scaled
part_1_height = 0.2

part_1 = cq.Workplane("XY").box(part_1_size, part_1_size, part_1_height)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.375, 0.0, 0.0))

# --- Assembly (if needed, based on the single part) ---
# In this case, there's only one part, so no assembly is needed.
# If there were multiple parts, you would use .union() or .cut() to combine them.

# --- Final Result ---
result = part_1

cq.exporters.export(result, './stlcq/0046/00468900.stl')