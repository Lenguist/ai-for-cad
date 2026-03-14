import cadquery as cq

length = 60
width = 40
height = 15

result = cq.Workplane("XY").box(length, width, height)