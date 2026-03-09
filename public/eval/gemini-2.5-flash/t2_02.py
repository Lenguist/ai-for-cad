import cadquery as cq

# Main cylinder dimensions
main_diameter = 30
main_radius = main_diameter / 2
main_height = 20

# Hole dimensions
hole_diameter = 10
hole_radius = hole_diameter / 2

# Create the main cylinder
main_cylinder = cq.Workplane("XY").cylinder(main_height, main_radius)

# Create the hole cylinder (make it slightly taller than the main cylinder to ensure a through-cut)
hole_cylinder = cq.Workplane("XY").cylinder(main_height + 2, hole_radius)

# Cut the hole from the main cylinder
result = main_cylinder.cut(hole_cylinder)