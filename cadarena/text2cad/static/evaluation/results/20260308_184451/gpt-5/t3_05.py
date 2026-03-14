import cadquery as cq
result = cq.Workplane("XY").box(80, 60, 8).faces(">Z").workplane().rect(60, 40).cutBlind(-4)