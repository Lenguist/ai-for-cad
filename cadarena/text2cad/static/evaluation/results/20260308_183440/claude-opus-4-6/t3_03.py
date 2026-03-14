import cadquery as cq

# T-shaped cross-section bracket
# Horizontal top bar: 80mm wide, 6mm thick, 20mm deep
# Vertical stem: 6mm thick, 40mm tall, 20mm deep

depth = 20  # depth into the page (along Y axis)

# Horizontal top bar (flange)
flange_width = 80
flange_thickness = 6
top_bar = cq.Workplane("XY").box(flange_width, depth, flange_thickness)
# Move the top bar so its bottom face is at z=0
top_bar = top_bar.translate((0, 0, flange_thickness / 2))

# Vertical stem (web)
stem_width = 6
stem_height = 40
stem = cq.Workplane("XY").box(stem_width, depth, stem_height)
# Move the stem so its top face is at z=0 (connecting to bottom of flange)
stem = stem.translate((0, 0, -stem_height / 2))

# Union the two parts
result = top_bar.union(stem)