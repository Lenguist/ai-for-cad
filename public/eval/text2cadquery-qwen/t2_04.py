import cadquery as cq

# --- Parameters from JSON ---
plate_size = 0.6 * 0.6  # Scaled plate size
hole_radius = 0.025 * 0.6  # Scaled hole radius
plate_thickness = 0.04
corner_offset = 0.08 * 0.6  # Scaled corner offset for holes

# --- Create the base square plate ---
plate = cq.Workplane("XY").rect(plate_size, plate_size).extrude(plate_thickness)

# --- Define hole positions ---
hole_positions = [
    (corner_offset - plate_size/2, corner_offset - plate_size/2),  # Bottom-left
    (corner_offset - plate_size/2, plate_size/2 - corner_offset),  # Top-left
    (plate_size/2 - corner_offset, corner_offset - plate_size/2),  # Bottom-right
    (plate_size/2 - corner_offset, plate_size/2 - corner_offset)   # Top-right
]

# --- Cut the holes ---
for x, y in hole_positions:
    plate = plate.faces(">Z").workplane().pushPoints([(x, y)]).hole(2 * hole_radius)

# --- Export to STL ---
cq.exporters.export(plate, './stlcq/0017/00179300.stl')