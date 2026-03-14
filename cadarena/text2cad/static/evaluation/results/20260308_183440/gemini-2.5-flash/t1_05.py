import cadquery as cq

# Define parameters
disk_diameter = 50.0
disk_thickness = 5.0
disk_radius = disk_diameter / 2.0

# Create the flat disk (cylinder)
result = cq.Workplane("XY").cylinder(disk_thickness, disk_radius)