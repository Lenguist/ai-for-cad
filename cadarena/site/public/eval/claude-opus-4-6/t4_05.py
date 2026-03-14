import cadquery as cq

# Create the flat plate
plate = cq.Workplane("XY").box(80, 60, 6)

# Define hole pattern parameters
hole_diameter = 3.5
countersink_diameter = 6.5
hole_spacing_x = 60
hole_spacing_y = 40

# Countersink angle of 90° means the cone half-angle is 45°
# Countersink depth = (countersink_diameter - hole_diameter) / 2 * tan(45°) = (6.5 - 3.5) / 2 = 1.5mm

# Create countersunk holes using cBoreHole or cboreHole approach
# We'll use the top face and create the hole pattern
result = (
    plate
    .faces(">Z")
    .workplane()
    .rect(hole_spacing_x, hole_spacing_y, forConstruction=True)
    .vertices()
    .cboreHole(hole_diameter, countersink_diameter, 0)
)

# The cboreHole with zero depth doesn't give a proper countersink.
# Instead, let's cut countersink cones and through holes manually.

# Start fresh
plate = cq.Workplane("XY").box(80, 60, 6)

# Hole positions
positions = [
    (hole_spacing_x / 2, hole_spacing_y / 2),
    (-hole_spacing_x / 2, hole_spacing_y / 2),
    (hole_spacing_x / 2, -hole_spacing_y / 2),
    (-hole_spacing_x / 2, -hole_spacing_y / 2),
]

# Through holes
plate_with_holes = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints(positions)
    .hole(hole_diameter)
)

# Countersink depth for 90° included angle (45° half angle)
# depth = (countersink_diameter / 2) since from the top the cone goes from countersink_diameter to 0
# But we only need the cone from countersink_diameter down to hole_diameter
countersink_depth = (countersink_diameter - hole_diameter) / 2.0  # 1.5mm

# Create countersink cuts using cones
# A cone from countersink_diameter/2 at top to hole_diameter/2 at bottom, depth = countersink_depth
# Position at top of plate (z = 3, top surface)

import math

for pos in positions:
    # Create a cone for countersink
    # The cone should sit with its wide end flush with the top surface
    # Using a solid of revolution
    cone = (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .lineTo(countersink_diameter / 2, 0)
        .lineTo(hole_diameter / 2, -countersink_depth)
        .lineTo(0, -countersink_depth)
        .close()
        .revolve(360, (0, 0, 0), (0, -1, 0))
        .translate((pos[0], pos[1], 3))  # top surface is at z=3
    )
    plate_with_holes = plate_with_holes.cut(cone)

result = plate_with_holes