import cadquery as cq
import math

# Gear parameters
module = 2.0
num_teeth = 20
face_width = 10.0
bore_diameter = 8.0
pressure_angle_deg = 20.0

# Derived dimensions
pitch_diameter = module * num_teeth
addendum = module
dedendum =