import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(50, 30, 5)
    .faces(">Z").workplane()
    .hole(8)
)