import cadquery as cq

# Create the square plate
result = (
    cq.Workplane("XY")
    .box(60, 60, 4)
)

# Define hole positions: 8mm from each edge
# Plate is centered at origin, so edges are at ±30
# Hole centers at ±(30-8) = ±22 in both X and Y
offset = 30 - 8  # 22mm from center

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        ( offset,  offset),
        (-offset,  offset),
        ( offset, -offset),
        (-offset, -offset)
    ])
    .hole(5)
)