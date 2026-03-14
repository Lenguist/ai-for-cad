import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(80, 60, 6)
    .faces(">Z").workplane()
    .pushPoints([(-30, -20), (30, -20), (30, 20), (-30, 20)])
    .cskHole(3.5, 6.5, 90)
)