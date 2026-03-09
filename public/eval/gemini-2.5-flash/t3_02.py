import cadquery as cq

# Outer dimensions
length = 60.0
width = 50.0
height = 40.0
thickness = 3.0

# Create the solid outer box
box = cq.Workplane("XY").box(length, width, height)

# Apply the shell operation, removing the top face and making it hollow inwards
# The top face is the one in the positive Z direction
result = box.faces(">Z").shell(-thickness)