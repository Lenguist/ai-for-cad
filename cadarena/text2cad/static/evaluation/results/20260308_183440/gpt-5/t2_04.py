import cadquery as cq

plate = cq.Workplane("XY").box(60, 60, 4)
hole_centers = [(22, 22), (22, -22), (-22, 22), (-22, -22)]
result = plate.faces(">Z").workplane().pushPoints(hole_centers).hole(5)