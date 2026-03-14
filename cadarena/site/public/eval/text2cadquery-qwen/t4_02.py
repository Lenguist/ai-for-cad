import cadquery as cq
import math
from cadquery.vis import show

# --- Part 1: Hex Bolt ---
sketch_scale = 0.13

# Scaled dimensions
scaled_x1 = 0.0 * sketch_scale
scaled_y1 = 0.0275 * sketch_scale
scaled_x2 = 0.065 * sketch_scale
scaled_y2 = 0.0 * sketch_scale
scaled_x3 = 0.13 * sketch_scale
scaled_y3 = 0.0275 * sketch_scale
scaled_x4 = 0.13 * sketch_scale
scaled_y4 = 0.1025 * sketch_scale
scaled_x5 = 0.065 * sketch_scale
scaled_y5 = 0.13 * sketch_scale
scaled_x6 = 0.0 * sketch_scale
scaled_y6 = 0.1025 * sketch_scale

# Hole parameters (scaled)
hole_center_x = 0.065 * sketch_scale
hole_center_y = 0.065 * sketch_scale
hole_radius = 0.05 * sketch_scale

# Extrusion depth
extrude_depth = 0.08 + 0.08

# Create the hexagonal head
hex_head = (
    cq.Workplane("XY")
    .moveTo(scaled_x1, scaled_y1)
    .lineTo(scaled_x2, scaled_y2)
    .lineTo(scaled_x3, scaled_y3)
    .lineTo(scaled_x4, scaled_y4)
    .lineTo(scaled_x5, scaled_y5)
    .lineTo(scaled_x6, scaled_y6)
    .close()
    .extrude(extrude_depth)
)

# Create the hole
hole = (
    cq.Workplane("XY")
    .circle(hole_radius)
    .extrude(extrude_depth)
    .translate((hole_center_x, hole_center_y, 0))
)

# Cut the hole from the hex head
hex_bolt = hex_head.cut(hole)

# --- Coordinate System Transformation for Part 1 ---
hex_bolt = hex_bolt.rotate((0, 0, 0), (0, 0, 1), -90)
hex_bolt = hex_bolt.translate((0, 0.16, 0))

# Export to STL
cq