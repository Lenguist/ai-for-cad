import cadquery as cq
import math

# Dimensions
head_across_flats = 13.0
head_height = 8.0
shaft_diameter = 10.0
shaft_length = 30.0

# Create the hexagonal head
# The sketch().polygon method takes the diameter of the inscribed circle (across flats)
hex_head = (
    cq.Workplane("XY")
    .sketch()
    .polygon(6, head_across_flats, makeRegular=True)
    .extrude(head_height)
)

# Create the cylindrical shaft
# The cylinder is created with its base on the XY plane and extruded in +Z
cyl_shaft = cq.Workplane("XY").cylinder(shaft_length, shaft_diameter / 2.0)

# Position the shaft below the head
# The head's bottom face is at Z=0 (if extruded from XY plane in +Z).
# The shaft's top face should also be at Z=0.
# Since the cylinder is created from Z=0 to Z=shaft_length,
# we need to translate it downwards by its full length.
cyl_shaft = cyl_shaft.translate((0, 0, -shaft_length))

# Combine the head and the shaft
result = hex_head.union(cyl_shaft)