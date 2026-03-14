import cadquery as cq

# Create the flange (40mm diameter, 6mm thick)
flange = cq.Workplane("XY").cylinder(6, 20, centered=(True, True, False))

# Create the shaft (20mm diameter, 30mm tall) sitting on top of the flange
shaft = cq.Workplane("XY").workplane(offset=6).cylinder(30, 10, centered=(True, True, False))

# Union the flange and shaft
result = flange.union(shaft)

# Add four 4mm holes on a 32mm bolt circle (radius=16mm) on the flange top face
result = (
    result
    .faces("<Z")
    .workplane()
    .polarArray(16, 0, 360, 4)
    .hole(4)
)