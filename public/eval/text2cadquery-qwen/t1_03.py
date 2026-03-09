import cadquery as cq

# --- Part 1: Sphere ---
part_1_radius = 0.015 * 0.03  # Sketch radius scaled
part_1_height = 0.015

part_1 = cq.Workplane("XY").circle(part_1_radius).extrude(part_1_height)

# --- Assembly (if needed, based on the single part) ---
# In this case, there's only one part, so no assembly is needed.
# If there were multiple parts, you would use .union() or .cut() to combine them.

# --- Final Result ---
result = part_1
cq.exporters.export(result, './stlcq/0026/00264978.stl')