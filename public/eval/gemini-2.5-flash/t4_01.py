import cadquery as cq

# Gear parameters
n_teeth = 20
module = 2.0
face_width = 10.0
bore_diameter = 8.0

# Standard pressure angle for spur gears
pressure_angle = 20.0

# Calculate addendum and dedendum based on module
addendum = module
dedendum = 1.25 * module

# Create the gear profile using the gear function
gear_profile = cq.Workplane("XY").gear(
    n_teeth=n_teeth,
    module=module,
    pressure_angle=pressure_angle,
    addendum=addendum,
    dedendum=dedendum
)

# Extrude the gear profile to the specified face width
gear_body = gear_profile.extrude(face_width)

# Add the central bore
result = gear_body.faces(">Z").workplane().hole(bore_diameter)