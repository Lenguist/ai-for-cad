import cadquery as cq

# Plate dimensions
plate_length = 60.0
plate_width = 60.0
plate_height = 4.0

# Hole dimensions
hole_diameter = 5.0
hole_offset = 8.0 # Distance from edge to hole center

# Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_height)

# Add the four holes
# Select the top face, create a workplane on it
# Move the workplane origin to the first hole position (relative to the plate's center)
# The plate is centered at (0,0).
# The first hole center is at (-plate_length/2 + hole_offset, -plate_width/2 + hole_offset)
# Which is (-30 + 8, -30 + 8) = (-22, -22)
# The spacing between holes will be (plate_length - 2 * hole_offset) = (60 - 2*8) = 44
result = result.faces(">Z").workplane().rect(plate_length - 2 * hole_offset, plate_width - 2 * hole_offset, forConstruction=True).vertices().hole(hole_diameter)