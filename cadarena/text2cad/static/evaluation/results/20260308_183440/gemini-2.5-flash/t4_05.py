import cadquery as cq

# Plate dimensions
plate_length = 80.0
plate_width = 60.0
plate_height = 6.0

# Hole parameters
hole_diameter = 3.5
countersink_diameter = 6.5
# For cskHole, the angle is the half-angle from the vertical axis.
# A 90-degree countersink means the cone angle is 90 degrees,
# so the half-angle from the center axis is 45 degrees.
countersink_angle = 45.0

# Hole pattern dimensions
hole_pattern_x = 60.0
hole_pattern_y = 40.0

# Create the base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_height)

# Add the countersunk holes
# The rarray centers the pattern, so we need to calculate the offsets
# for the individual holes from the center of the pattern.
# For a 60x40 pattern, the holes are at (+/- 30, +/- 20) from the center.
# rarray takes xSpacing and ySpacing, and xCount, yCount.
# To get 4 holes at (+/- 30, +/- 20), we need xSpacing = 60, ySpacing = 40, xCount = 2, yCount = 2.
# The rarray will then place points at (-30, -20), (30, -20), (-30, 20), (30, 20) relative to the workplane origin.
result = result.faces(">Z").workplane().rarray(hole_pattern_x, hole_pattern_y, 2, 2).cskHole(
    hole_diameter, countersink_diameter, countersink_angle, depth=plate_height
)