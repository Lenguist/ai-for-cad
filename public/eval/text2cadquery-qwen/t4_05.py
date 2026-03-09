import cadquery as cq

# --- Parameters from JSON ---
plate_length = 0.8 * 0.8  # Scaled length
plate_width = 0.6 * 0.8  # Scaled width
plate_thickness = 0.06
hole_radius = 0.0175 * 0.8  # Scaled radius
hole_depth = 0.065

# Hole positions (scaled)
hole_positions = [
    (0.03 * 0.8, 0.03 * 0.8),
    (0.03 * 0.8, 0.3 * 0.8),
    (0.77 * 0.8, 0.03 * 0.8),
    (0.77 * 0.8, 0.3 * 0.8)
]

# --- Create the plate ---
plate = cq.Workplane("XY").rect(plate_length, plate_width).extrude(plate_thickness)

# --- Add the holes ---
for x, y in hole_positions:
    plate = plate.faces(">Z").workplane().hole(2 * hole_radius)

# --- Export to STL ---
cq.exporters.export(plate, './stlcq/0017/00170000.stl')