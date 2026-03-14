import cadquery as cq

plate = cq.Workplane("XY").box(60, 60, 4)
hole_offset = 30 - 8
result = (
    plate
    .faces(">Z").workplane()
    .pushPoints([
        ( hole_offset,  hole_offset),
        ( hole_offset, -hole_offset),
        (-hole_offset,  hole_offset),
        (-hole_offset, -hole_offset)
    ])
    .hole(5)
)