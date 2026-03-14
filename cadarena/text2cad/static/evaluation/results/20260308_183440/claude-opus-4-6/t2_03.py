import cadquery as cq

# L-shaped bracket
# One arm 60mm long, the other 40mm long
# Both arms 20mm wide and 5mm thick

thickness = 5.0
width = 20.0
arm1_length = 60.0
arm2_length = 40.0

# Create the horizontal arm (along X axis)
arm1 = cq.Workplane("XY").box(arm1_length, width, thickness)
# Center of arm1 is at origin, so it spans from -30 to +30 in X

# Create the vertical arm (along Y axis)
# The vertical arm should connect at the end of the horizontal arm
# arm2 goes upward from the end of arm1
arm2 = cq.Workplane("XY").box(thickness, arm2_length, width)

# Position the arms to form an L-shape
# Place arm1 so its left edge is at x=0
arm1 = arm1.translate((arm1_length / 2, 0, 0))

# Place arm2 so its bottom edge meets the top of arm1 at the left end
# arm2 center needs to be at x=thickness/2, y=arm2_length/2
arm2 = arm2.translate((thickness / 2, arm2_length / 2, 0))

# Union the two arms
result = arm1.union(arm2)

# Re-center so the corner of the L is at the origin
result = result.translate((0, -width / 2, 0))