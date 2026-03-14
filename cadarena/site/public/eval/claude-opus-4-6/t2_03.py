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
# Center of arm1 is at origin, so it extends from -30 to +30 in X

# Create the vertical arm (along Y axis)
# Position it so that the arms form an L-shape, connecting at the corner
arm2 = cq.Workplane("XY").box(thickness, arm2_length, width)
# We need to position arm2 at the end of arm1

# Strategy: 
# Arm1 (horizontal): 60mm in X, 20mm in Z (width), 5mm in Y (thickness)
# Arm2 (vertical): 5mm in X (thickness), 40mm in Y, 20mm in Z (width)
# They share a corner

# Let's rebuild more carefully
# Arm1 lies flat: length along X, width along Z, thickness along Y
arm1 = cq.Workplane("XZ").box(arm1_length, width, thickness)
# This gives a box centered at origin: X from -30 to 30, Z from -10 to 10, Y from -2.5 to 2.5

# Move arm1 so its left edge is at X=0, bottom edge at Y=0
arm1 = arm1.translate((arm1_length / 2, thickness / 2, 0))
# Now arm1: X from 0 to 60, Y from 0 to 5, Z from -10 to 10

# Arm2 goes upward from the left end of arm1
arm2 = cq.Workplane("XZ").box(thickness, width, arm2_length)
# Move arm2 so its bottom aligns with arm1's bottom and its left edge at X=0
arm2 = arm2.translate((thickness / 2, arm2_length / 2, 0))
# Now arm2: X from 0 to 5, Y from 0 to 40, Z from -10 to 10

# Union the two arms
result = arm1.union(arm2)