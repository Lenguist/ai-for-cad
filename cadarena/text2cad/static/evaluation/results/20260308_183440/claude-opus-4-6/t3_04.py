import cadquery as cq

# Bottom section: 20mm diameter × 10mm tall
bottom = cq.Workplane("XY").cylinder(10, 10)  # height=10, radius=10

# Middle section: 14mm diameter × 20mm tall, stacked on top of bottom
middle = cq.Workplane("XY").cylinder(20, 7).translate((0, 0, 10/2 + 20/2))  # radius=7

# Top section: 10mm diameter × 15mm tall, stacked on top of middle
top = cq.Workplane("XY").cylinder(15, 5).translate((0, 0, 10/2 + 20 + 15/2))  # radius=5

# Union all sections together
result = bottom.union(middle).union(top)