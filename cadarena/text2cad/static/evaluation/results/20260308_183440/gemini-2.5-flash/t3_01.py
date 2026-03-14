import cadquery as cq

# Flange dimensions
flange_diameter = 40
flange_radius = flange_diameter / 2
flange_thickness = 6

# Shaft dimensions
shaft_diameter = 20
shaft_radius = shaft_diameter / 2
shaft_height = 30

# Hole dimensions
hole_diameter = 4
bolt_circle_diameter = 32
bolt_circle_radius = bolt_circle_diameter / 2
num_holes = 4

# Create the flange
flange = cq.Workplane("XY").cylinder(flange_thickness, flange_radius)

# Add holes to the flange
flange_with_holes = (
    flange
    .faces(">Z") # Select the top face of the flange
    .workplane() # Create a workplane on this face
    .polarArray(bolt_circle_radius, 0, 360, num_holes) # Create points for holes
    .hole(hole_diameter) # Cut the holes
)

# Create the shaft
# The shaft is created starting from the XY plane, so its base is at Z=0.
# It needs to be translated up by the flange_thickness to sit on top of the flange.
shaft = cq.Workplane("XY").cylinder(shaft_height, shaft_radius)

# Translate the shaft to sit on top of the flange
shaft_translated = shaft.translate((0, 0, flange_thickness))

# Union the flange with holes and the translated shaft
result = flange_with_holes.union(shaft_translated)