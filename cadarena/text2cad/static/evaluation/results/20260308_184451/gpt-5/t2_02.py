import cadquery as cq

result = cq.Workplane("XY").cylinder(20, 15).faces(">Z").workplane().hole(10)