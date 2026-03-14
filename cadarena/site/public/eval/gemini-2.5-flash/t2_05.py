import cadquery as cq

# Disk dimensions
disk_diameter = 50.0
disk_radius = disk_diameter / 2.0
disk_thickness = 8.0

# Hole dimensions
hole_diameter = 4.0
num_holes = 6
bolt_circle_diameter = 38.0
bolt_circle_radius = bolt_circle_diameter / 2.0

# Create the base disk
result = cq.Workplane("XY").cylinder(disk_thickness, disk_radius)

# Add the holes
result = result.faces(">Z").workplane().polarArray(
    bolt_circle_radius, 0, 360, num_holes
).hole(hole_diameter)