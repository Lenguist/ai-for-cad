import cadquery as cq
import math

# Dimensions
across_flats = 13.0
head_height = 8.0
shaft_diameter = 10.0
shaft_length = 30.0

# Convert across-flats to polygon diameter (across corners)
polygon_diameter = 2.0 * across_flats / math.sqrt(3.0)

# Build hex head and cylindrical shaft
result = (
    cq.Workplane("XY")
    .polygon(6, polygon_diameter)
    .extrude(head_height)
    .faces("<Z").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(-shaft_length)
)