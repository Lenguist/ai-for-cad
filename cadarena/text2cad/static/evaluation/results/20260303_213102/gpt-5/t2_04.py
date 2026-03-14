import cadquery as cq

size = 60
thickness = 4
edge_distance = 8
hole_diameter = 5

half = size / 2
offset = half - edge_distance

result = (
    cq.Workplane("XY")
    .box(size, size, thickness)
    .faces(">Z").workplane()
    .pushPoints([
        ( offset,  offset),
        ( offset, -offset),
        (-offset,  offset),
        (-offset, -offset),
    ])
    .hole(hole_diameter)
)