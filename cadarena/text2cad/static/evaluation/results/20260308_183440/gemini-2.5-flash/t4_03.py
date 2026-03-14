import cadquery as cq

# Parameters
inner_diameter = 15.0
wall_thickness = 2.0
bend_centerline_radius = 20.0
straight_section_length = 25.0

# Calculated dimensions
inner_radius = inner_diameter / 2.0
outer_radius = inner_radius + wall_thickness

# 1. Create the 2D profile (annulus)
# The profile should be on a plane perpendicular to the start of the path.
# The path starts along the Y-axis, so the profile is on the XZ plane.
profile = (
    cq.Workplane("XZ")
    .circle(outer_radius)
    .cut(cq.Work