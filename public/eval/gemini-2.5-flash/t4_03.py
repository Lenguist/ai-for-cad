import cadquery as cq

# Parameters
inner_diameter = 15.0
wall_thickness = 2.0
bend_centerline_radius = 20.0
straight_section_length = 25.0

# Calculated dimensions
outer_diameter = inner_diameter + 2 * wall_thickness
inner_radius = inner_diameter