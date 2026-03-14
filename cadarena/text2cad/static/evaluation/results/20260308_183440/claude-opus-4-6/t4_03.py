import cadquery as cq
import math

# Parameters
inner_diameter = 15.0
inner_radius = inner_diameter / 2.0
wall_thickness = 2.0
outer_radius = inner_radius + wall_thickness
bend_radius = 20.0  # centerline radius of the bend
straight_length = 25.0
bend_angle = 90.0

# Create the sweep path for the elbow
# Path: straight section along Z, 90-degree arc, then straight section
# We'll build the full path as a wire

# Strategy: Create the pipe by making individual sections and unioning them

# 1. First straight section along -Z direction (vertical, going down)
straight1 = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(straight_length)
    .translate((0, 0, -straight_length))
)

# 2. The 90-degree bend
# The bend goes from Z-axis to X-axis with centerline radius = bend_radius
# Center of the bend arc is at (bend_radius, 0, 0)
# We'll create this by sweeping a circle along an arc path

# Create the sweep path for the bend
# Arc from (0,0,0) going in Z=0 plane, curving from -Z direction to +X direction
# Actually, let's think about this differently.

# Place bend center at (bend_radius, 0, 0)
# The arc starts at (0, 0, 0) and ends at (bend_radius, 0, bend_radius)
# going 90 degrees

# Create a path for the bend using a 3D arc
# The bend transitions from the vertical (Z) direction to horizontal (X) direction
# Center of curvature at (bend_radius, 0, 0)

# Path as arc: starts at (0,0,0), center at (bend_radius, 0, 0), 
# ends at (bend_radius, 0, bend_radius)

bend_path = (
    cq.Workplane("XZ")
    .center(bend_radius, 0)
    .radiusArc((-bend_radius, bend_radius), -bend_radius)
)

# Sweep the annular cross-section along the bend path
bend_section = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .sweep(bend_path, isFrenet=True)
)

# 3. Second straight section along X direction starting from end of bend
# End of bend is at (bend_radius, 0, bend_radius), going in +X direction
straight2 = (
    cq.Workplane("XY")
    .transformed(offset=(bend_radius, 0, bend_radius), rotate=(0, 90, 0))
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(straight_length)
)

# Combine all parts
result = straight1.union(bend_section).union(straight2)