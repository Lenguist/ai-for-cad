import cadquery as cq

# Hex bolt parameters
across_flats = 13.0  # distance across flats of hexagonal head
head_height = 8.0
shaft_diameter = 10.0
shaft_length = 30.0

# Calculate the circumscribed radius (across corners / 2) from across flats
# For a regular hexagon: across_flats = 2 * r * cos(30°) = r * sqrt(3)
hex_radius = across_flats / (3**0.5)  # circumscribed radius

# Create the hexagonal head
head = (
    cq.Workplane("XY")
    .polygon(6, hex_radius * 2)  # polygon takes the circumscribed diameter
    .extrude(head_height)
)

# Create the cylindrical shaft below the head (extending in -Z direction)
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2.0)
    .extrude(-shaft_length)
)

# Combine head and shaft
result = head.union(shaft)