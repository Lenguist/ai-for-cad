import cadquery as cq

result = (
    cq.Workplane("XY")
    .cylinder(8, 25)
    .faces(">Z").workplane()
    .polarArray(19, 0, 360, 6)
    .hole(4)
)