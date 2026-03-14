import cadquery as cq

# Bottom section
bottom_radius = 20 / 2
bottom_height = 10
bottom_cylinder = cq.Workplane("XY").cylinder(bottom_height, bottom_radius)

# Middle section
middle_radius = 14 / 2
middle_height = 20
middle_cylinder = cq.Workplane("XY").cylinder(middle_height, middle_radius).translate((0, 0, bottom_height))

# Top section
top_radius = 10 / 2
top_height = 15
top_cylinder = cq.Workplane("XY").cylinder(top_height, top_radius).translate((0, 0, bottom_height + middle_height))

# Union all sections
result = bottom_cylinder.union(middle_cylinder).union(top_cylinder)