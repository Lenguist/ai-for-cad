import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(10.0).extrude(10.0)
    .faces(">Z").workplane().circle(7.0).extrude(20.0)
    .faces(">Z").workplane().circle(5.0).extrude(15.0)
)