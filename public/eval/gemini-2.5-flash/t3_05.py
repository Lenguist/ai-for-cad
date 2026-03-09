import cadquery as cq

# Create the base rectangular plate
plate_length = 80
plate_width = 60
plate_height = 8

# Create the rectangular pocket dimensions
pocket_length = 60
pocket_width = 40
pocket_depth = 4

result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_height)
    .faces(">Z")  # Select the top face of the plate
    .workplane()  # Create a new workplane on the top face
    .rect(pocket_length, pocket_width)  # Draw the rectangle for the pocket
    .cutExtrude(-pocket_depth)  # Cut the pocket downwards by its depth
)