import cadquery as cq

# Hex bolt parameters
across_flats = 13  # mm
head_height = 8    # mm
shaft_diameter = 10  # mm
shaft_length = 30   # mm

# Calculate the circumscribed radius for a regular hexagon from across-flats dimension
# across_flats = 2 * (apothem), so apothem = across_flats / 2
# For a regular hexagon: apothem = circumradius * cos(30°) = circumradius * (sqrt(3)/2)
# So circumradius = apothem / cos(30°) = (across_flats / 2) / (sqrt(3)/2) = across_flats / sqrt(3)
import math
circumradius = across_flats / math.sqrt(3)

# Create the hexagonal head
head = (
    cq.Workplane("XY")
    .polygon(6, circumradius * 2)  # polygon takes the circumscribed diameter
    .extrude(head_height)
)

# Create the cylindrical shaft below the head
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(-shaft_length)
)

# Combine head and shaft
result = head.union(shaft)