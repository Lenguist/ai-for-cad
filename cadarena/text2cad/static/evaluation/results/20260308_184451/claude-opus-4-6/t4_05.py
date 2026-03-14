import cadquery as cq

# Create the flat plate
plate = cq.Workplane("XY").box(80, 60, 6)

# Define hole pattern parameters
hole_diameter = 3.5
countersink_diameter = 6.5
countersink_angle = 90
x_spacing = 60
y_spacing = 40

# Create countersunk holes in a rectangular pattern
result = (
    plate
    .faces(">Z")
    .workplane()
    .rect(x_spacing, y_spacing, forConstruction=True)
    .vertices()
    .cboreHole(
        diameter=hole_diameter,
        cboreDiameter=0,
        cboreDepth=0
    )
)

# Redo with proper countersink holes using cskHole
result = (
    plate
    .faces(">Z")
    .workplane()
    .rect(x_spacing, y_spacing, forConstruction=True)
    .vertices()
    .cskHole(
        diameter=hole_diameter,
        cskDiameter=countersink_diameter,
        cskAngle=countersink_angle
    )
)