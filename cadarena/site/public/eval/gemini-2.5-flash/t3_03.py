import cadquery as cq

# Define dimensions
top_bar_width = 80.0
stem_height = 40.0
thickness = 6.0
depth = 20.0

# Calculate half dimensions for easier sketching
half_top_bar_width = top_bar_width / 2.0
half_thickness = thickness / 2.0

# Create the T-shaped profile
result = (
    cq.Workplane("XY")
    .moveTo(-half_top_bar_width, 0)
    .lineTo(half_top_bar_width, 0)
    .lineTo(half_top_bar_width, -thickness)
    .lineTo(half_thickness, -thickness)
    .lineTo(half_thickness, -(thickness + stem_height))
    .lineTo(-half_thickness, -(thickness + stem_height))
    .lineTo(-half_thickness, -thickness)
    .lineTo(-half_top_bar_width, -thickness)
    .close()
    .extrude(depth)
)