import cadquery as cq

# Create the base rectangular plate: 80mm x 60mm x 8mm
result = (
    cq.Workplane("XY")
    .box(80, 60, 8)
)

# Mill a rectangular pocket into the top face: 60mm x 40mm x 4mm deep, centered
pocket = (
    cq.Workplane("XY")
    .workplane(offset=8/2 - 4)  # Position at top surface minus pocket depth
    .box(60, 40, 4)
    .translate((0, 0, 4/2))  # Shift up so top of pocket aligns with top of plate
)

# Actually, let me redo this more cleanly
result = (
    cq.Workplane("XY")
    .box(80, 60, 8)
    .faces(">Z")
    .workplane()
    .rect(60, 40)
    .cutBlind(-4)
)