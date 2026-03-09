import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(10).extrude(10)
    .faces(">Z").workplane().circle(7).extrude(20)
    .faces(">Z").workplane().circle(5).extrude(15)
)