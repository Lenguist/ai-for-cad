import cadquery as cq

# Plate dimensions
plate_length = 80.0
plate_width = 60.0
plate_height = 8.0

# Pocket dimensions
pocket_length = 60.0
pocket_width = 40.0
pocket_depth = 4.0

# Create the base plate
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_height)

# Create the pocket by selecting the top face, creating a workplane,
# drawing the rectangle, and then cutting downwards.
result = plate.faces(">Z").workplane().rect(pocket_length, pocket_width).cutBlind(-pocket_depth)