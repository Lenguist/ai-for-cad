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
# The path consists of: straight section -> 90° arc -> straight section
# We'll build this as a wire

# Strategy: Create outer and inner sweep paths, or use a single path and sweep a circle

# Let's build the path:
# Start with a straight section along Z, then arc in the XZ plane, then straight along X

# Path points:
# Straight section 1: from (0, 0, -straight_length) to (0, 0, 0)
# Arc: center at (bend_radius, 0, 0), from (0, 0, 0) sweeping 90° to (bend_radius, 0, bend_radius)
# Straight section 2: from (bend_radius, 0, bend_radius) to (bend_radius + straight_length, 0, bend_radius)

# Create the path as a wire using edges
path = (
    cq.Workplane("XZ")
    .moveTo(0, -straight_length)
    .lineTo(0, 0)
    .threePointArc(
        (bend_radius - bend_radius * math.cos(math.radians(45)), bend_radius * math.sin(math.radians(45))),
        (bend_radius, bend_radius)
    )
    .lineTo(bend_radius + straight_length, bend_radius)
)

# Create outer pipe by sweeping outer circle along path
outer_pipe = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -straight_length))
    .circle(outer_radius)
    .sweep(path, multisection=False, isFrenet=True)
)

# Create inner pipe (to cut out) by sweeping inner circle along path
inner_pipe = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -straight_length))
    .circle(inner_radius)
    .sweep(path, multisection=False, isFrenet=True)
)

# Cut inner from outer to create hollow pipe
result = outer_pipe.cut(inner_pipe)