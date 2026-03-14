import cadquery as cq

# Define dimensions
arm1_length = 60.0
arm2_length = 40.0
arm_width = 20.0
arm_thickness = 5.0

# Create the first arm (along the X-axis)
# The box is created with its corner at (0,0,0)
arm1 = cq.Workplane("XY").box(arm1_length, arm_width, arm_thickness, centered=(False, False, False))

# Create the second arm (along the Y-axis)
# The box is also created with its corner at (0,0,0), overlapping the first arm
arm2 = cq.Workplane("XY").box(arm_width, arm2_length, arm_thickness, centered=(False, False, False))

# Union the two arms to form the L-shape
result = arm1.union(arm2)