import cadquery as cq

# Hexagonal head dimensions
head_across_flats = 13.0
head_height = 8.0
head_radius = head_across_flats / 2.0

# Cylindrical shaft dimensions
shaft_diameter = 10.0
shaft_length = 30.0
shaft_radius = shaft_diameter / 2.0

# Create the hexagonal head
# Start on the XY plane, create a 6-sided polygon with the specified radius (across flats / 2)
# Extrude it upwards by the head_height
hex_head = (
    cq.Workplane("XY")
    .polygon(6, head_radius)
    .extrude(head_height)
)

# Create the cylindrical shaft
# Start on the XY plane, create a circle with the specified radius
# Extrude it downwards by the shaft_length
cyl_shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(-shaft_length)
)

# Combine the head and the shaft
# The head is extruded from Z=0 to Z=head_height
# The shaft is extruded from Z=0 to Z=-shaft_length
# Unioning them will place the shaft directly below the head, sharing the Z=0 plane
result = hex_head.union(cyl_shaft)