import cadquery as cq

# Create the base disk
result = (
    cq.Workplane("XY")
    .cylinder(8, 50 / 2)
    .faces(">Z")
    .workplane()
    .polarArray(38 / 2, 0, 360, 6)
    .hole(4)
)