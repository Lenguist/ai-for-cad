import cadquery as cq

plate = cq.Workplane("XY").box(60, 60, 4)

offset = 30 - 8  # half of 60 minus edge distance
holes = [(offset, offset), (offset, -offset), (-offset, offset), (-offset, -offset)]

result = plate.faces(">Z").workplane().pushPoints(holes).hole(5)