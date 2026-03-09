import cadquery as cq

result = cq.Workplane("XY").box(60, 50, 40).faces(">Z").shell(-3)