import cadquery as cq

# --- Part 1: Spring ---
outer_diameter = 0.02 * 0.02  # Scaled outer diameter
inner_diameter = 0.01 * 0.02  # Scaled inner diameter
wire_diameter = 0.0015 * 0.02  # Scaled wire diameter
height = 0.75  # Extrusion depth

# Create the basic shape of the spring (a cylinder with a hole)
spring = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
)

# Cut out the inner cylinder to create the hollow center
inner_cylinder = (
    cq.Workplane("XY")
    .circle(inner_diameter / 2)
    .extrude(height)
)

spring = spring.cut(inner_cylinder)

# Create the wire by extruding a circle
wire = (
    cq.Workplane("XY")
    .circle(wire_diameter / 2)
    .extrude(height)
)

# Position the wire at the top of the cylinder
wire = wire.translate((0, 0, height))

# Combine the cylinder and the wire
combined_shape = spring.union(wire)

# Create the first loop by extruding a circle
loop1 = (
    cq.Workplane("XY")
    .circle(wire_diameter / 2)
    .extrude(height)
)

# Position the first loop at the top of the cylinder
loop1 = loop1.translate((0, 0, height))

# Create the second loop by extruding a circle
loop2 = (
    cq.Workplane("XY")
    .circle(wire_diameter / 2)
    .extrude(height)
)

# Position the second loop at the top of the cylinder
loop2 = loop2.translate((0, 0, height))

# Create the third loop by extruding a circle
loop3 = (
    cq.Workplane("XY")
    .circle(wire_diameter / 2)
    .extrude(height)
)

# Position the third loop at the top of the cylinder
loop3 = loop3.translate((0, 0, height))

# Create the fourth loop by extruding a circle
loop4 = (
    cq.Workplane("XY")
    .circle(wire_diameter / 2)
    .extrude(height)
)

# Position the fourth loop at the top of the