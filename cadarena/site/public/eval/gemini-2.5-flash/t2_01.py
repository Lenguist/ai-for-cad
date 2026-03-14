import cadquery as cq

# Create the rectangular plate
plate_length = 50
plate_width = 30
plate_height = 5
result = cq.Workplane("XY").box(plate_length, plate_width, plate_height)

# Add a centered circular hole
hole_diameter = 8
result = result.faces(">Z").workplane().hole(hole_diameter)