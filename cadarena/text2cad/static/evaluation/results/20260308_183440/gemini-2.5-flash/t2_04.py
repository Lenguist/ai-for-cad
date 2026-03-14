import cadquery as cq

# Plate dimensions
plate_length = 60.0
plate_width = 60.0
plate_height = 4.0

# Hole dimensions
hole_diameter = 5.0
hole_radius = hole_diameter / 2.0
edge_offset = 8.0

# Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_height)

# Calculate hole positions relative to the plate's center
# The plate is centered at (0,0) on the XY plane.
# Its X range is -plate_length/2 to plate_length/2
# Its Y range is -plate_width/2 to plate_width/2
x_pos_offset = plate_length / 2.0 - edge_offset
y_pos_offset = plate_width / 2.0 - edge_offset

# Create the holes using rarray for a rectangular pattern
# The rarray method starts from the current workplane's origin.
# We need to move the workplane to the center of the first hole.
# The first hole will be at (-x_pos_offset, -y_pos_offset)
# The spacing between holes will be 2 * x_pos_offset and 2 * y_pos_offset
result = result.faces(">Z").workplane() \
    .rarray(2 * x_pos_offset, 2 * y_pos_offset, 2, 2, center=(True, True)) \
    .hole(hole_diameter)