import cadquery as cq

# L-shaped bracket
# One arm 60mm long, the other 40mm long, both 20mm wide and 5mm thick

thickness = 5
width = 20

# Horizontal arm: 60mm long along X
arm1 = cq.Workplane("XY").box(60, width, thickness).translate((30, width / 2, thickness / 2))

# Vertical arm: 40mm long along Y
arm2 = cq.Workplane("XY").box(thickness, 40, width).translate((thickness / 2, 20, width / 2))

# Union the two arms
result = arm1.union(arm2)