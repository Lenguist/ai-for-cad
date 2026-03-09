import cadquery as cq

# Parameters
outer_diameter = 20.0
wire_diameter = 1.5
active_coils = 10
free_length = 50.0

# Derived parameters
mean_diameter = outer_diameter - wire_diameter
helix_radius = mean_diameter / 2.0

# For flat ground ends