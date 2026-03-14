import cadquery as cq

# Flange dimensions
flange_radius = 40 / 2
flange_height = 6

# Shaft dimensions
shaft_radius = 20 / 2
shaft_height = 30

# Hole dimensions
hole_diameter = 4
bolt_circle_radius = 32 / 2
num_holes = 4

# Create the flange
flange = cq.Workplane("XY").cylinder(flange_height, flange_radius)

# Create the shaft
shaft = cq.Workplane("XY").cylinder(shaft_height, shaft_radius)

# Position the shaft on top of the flange
# The shaft's base is at Z=0, so translate it up by the flange_height
shaft = shaft.translate((0, 0, flange_height))

# Union the flange and the shaft
combined_part = flange.union(shaft)

# Add holes to the flange
# Select the top face of the flange (which is Z=flange_height)
# and create a workplane there for the holes.
result = combined_part.faces(f">Z").workplane(offset=-flange_height/2).polarArray(bolt_circle_radius, 0, 360, num_holes).hole(hole_diameter)