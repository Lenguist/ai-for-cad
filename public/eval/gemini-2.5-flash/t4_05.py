import cadquery as cq

# Plate dimensions
plate_length = 80.0
plate_width = 60.0
plate_height = 6.0

# Hole parameters
hole_diameter = 3.5
countersink_diameter = 6.5
# CadQuery's cskHole uses a half-angle for the cone.
# A 90-degree countersink means the cone angle is 90 degrees,
# so the half-angle is 45 degrees.
countersink_half_angle = 45.0

# Hole pattern dimensions (centers)
hole_pattern_x = 60.0
hole_pattern_y = 40.0

# Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_height)

# Add the four countersunk holes
# The rarray method places the origin at the center of the array.
# We need to calculate the offset for the first hole from the center of the plate.
# For a 60x40mm pattern, the first hole will be at (-30, -20) relative to the pattern center.
# Since the plate is centered, the pattern center is also the plate center.
result = result.faces(">Z").workplane() \
    .rarray(hole_pattern_x, hole_pattern_y, 2, 2, centered=True) \
    .cskHole(hole_diameter, countersink_diameter, countersink_half_angle)