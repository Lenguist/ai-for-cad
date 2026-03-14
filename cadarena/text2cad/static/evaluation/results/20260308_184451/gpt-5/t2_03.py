import cadquery as cq

length_long = 60.0
length_short = 40.0
width = 20.0
thickness = 5.0

points = [
    (0, 0),
    (length_long, 0),
    (length_long, width),
    (width, width),
    (width, length_short),
    (0, length_short)
]

result = cq.Workplane("XY").polyline(points).close().extrude(thickness)