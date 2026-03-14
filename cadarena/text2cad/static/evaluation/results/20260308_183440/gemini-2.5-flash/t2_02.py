import cadquery as cq

# Main cylinder dimensions
cylinder_radius = 30 / 2
cylinder_height = 20

# Hole dimensions
hole_radius = 10 / 2
# The hole height should be at least the cylinder height to ensure it's a through-hole
hole_height = cylinder_height

# Create the main cylinder
main_cylinder = cq.Workplane("XY").cylinder(cylinder_height, cylinder_radius)

# Create the coaxial through-hole
# We can create a cylinder for the hole and cut it from the main cylinder
hole_cylinder = cq.Workplane("XY").cylinder(hole_height, hole_radius)

# Cut the hole from the main cylinder
result = main_cylinder.cut(hole_cylinder)