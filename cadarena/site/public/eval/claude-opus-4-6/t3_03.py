import cadquery as cq

# T-shaped cross-section bracket
# Horizontal top bar: 80mm wide, 6mm thick (tall), 20mm deep
# Vertical stem: 6mm thick (wide), 40mm tall, 20mm deep

# Parameters
top_bar_width = 80.0
top_bar_thickness = 6.0
stem_height = 40.0
stem_thickness = 6.0
depth = 20.0

# Create the horizontal top bar
top_bar = (cq.Workplane("XY")
           .box(top_bar_width, depth, top_bar_thickness)
           .translate((0, 0, stem_height + top_bar_thickness / 2)))

# Create the vertical stem
stem = (cq.Workplane("XY")
        .box(stem_thickness, depth, stem_height)
        .translate((0, 0, stem_height / 2)))

# Union the two parts to form the T-shape
result = top_bar.union(stem)