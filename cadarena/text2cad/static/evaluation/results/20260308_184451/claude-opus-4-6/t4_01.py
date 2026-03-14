import cadquery as cq
import math

# Gear parameters
num_teeth = 20
module = 2.0
pitch_diameter = num_teeth * module  # 40mm
face_width = 10.0
bore_diameter = 8.0

# Derived gear parameters
pressure_angle = 20.0  # degrees, standard
pa_rad = math.radians(pressure_angle)
pitch_radius = pitch_diameter / 2.0  # 20mm
addendum = module  # 2mm
dedendum = 1.25 * module  # 2.5mm
outer_radius = pitch_radius + addendum  # 22mm
root_radius = pitch_radius - dedendum  # 17.5mm
base_radius = pitch_radius * math.cos(pa_rad)  # base circle radius

# Function to generate involute curve point at parameter t
def involute_point(base_r, t):
    """Return (x, y) on the involute of a circle with radius base_r at parameter t."""
    x = base_r * (math.cos(t) + t * math.sin(t))
    y = base_r * (math.sin(t) - t * math.cos(t))
    return (x, y)

# Find the involute parameter t for a given radius
def involute_param_at_radius(base_r, r):
    """Find parameter t where the involute reaches radius r."""
    # r^2 = base_r^2 * (1 + t^2)
    if r <= base_r:
        return 0.0
    return math.sqrt((r / base_r) ** 2 - 1)

# Angular position of involute at a given radius
def involute_angle_at_radius(base_r, r):
    """Return the angle (from center) of the involute point at radius r."""
    t = involute_param_at_radius(base_r, r)
    return t - math.atan(t)

# Tooth thickness angle at pitch circle (half tooth)
tooth_thickness_angle = math.pi / (2 * num_teeth)  # half angular pitch = pi/(2*N)

# Involute angle at pitch circle
inv_at_pitch = involute_angle_at_radius(base_radius, pitch_radius)

# Number of points for involute curve
n_points = 20

# Parameter range for involute
t_max = involute_param_at_radius(base_radius, outer_radius)
t_min = 0.0  # starts at base circle

# Generate one tooth profile (right flank involute)
# We'll build the full gear profile as a 2D wire

def rotate_point(x, y, angle):
    """Rotate point (x,y) by angle (radians) around origin."""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

# Build complete gear tooth profile
# Each tooth: right involute, tip arc, left involute (mirror), root arc
tooth_angle = 2 * math.pi / num_teeth

# The right involute starts at base circle and goes to outer_radius
# We offset it so tooth is symmetric about x-axis
# Offset angle: tooth_thickness_angle + inv_at_pitch (to center the tooth)
offset_angle = tooth_thickness_angle + inv_at_pitch

gear_points = []

for i in range(num_teeth):
    rotation = i * tooth_angle
    
    # Right flank involute (from root to tip)
    if root_radius < base_radius:
        # Add radial line from root to base circle
        px, py = rotate_point(root_radius, 0, -offset_angle + rotation)
        gear_points.append((px, py))
        px, py = rotate_point(base_radius, 0, -offset_angle + rotation)
        gear_points.append((px, py))
    
    for j in range(n_points + 1):
        t = t_min + (t_max - t_min) * j / n_points
        ix, iy = involute_point(base_radius, t)
        # Rotate to center tooth
        px, py = rotate_point(ix, iy, -offset_angle + rotation)
        gear_points.append((px, py))
    
    # Tip point at outer_radius (tiny arc approximated)
    
    # Left flank involute (mirror of right, from tip to root)
    for j in range(n_points, -1, -1):
        t = t_min + (t_max - t_min) * j / n_points
        ix, iy = involute_point(base_radius, t)
        # Mirror about x-axis then rotate
        px, py = rotate_point(ix, -iy, offset_angle + rotation)
        gear_points.append((px, py))
    
    if root_radius < base_radius:
        px, py = rotate_point(base_radius, 0, offset_angle + rotation)
        gear_points.append((px, py))
        px, py = rotate_point(root_radius, 0, offset_angle + rotation)
        gear_points.append((px, py))
    
    # Root arc point (midpoint between teeth at root)
    next_rotation = (i + 1) * tooth_angle
    mid_root_angle = rotation + tooth_angle / 2 + tooth_angle / 2
    root_mid = rotate_point(root_radius, 0, -offset_angle + next_rotation)
    gear_points.append(root_mid)

# Close the profile
gear_points.append(gear_points[0])

# Create the gear as a 2D profile extruded
gear_profile = cq.Workplane("XY").polyline(gear_points).close()
gear_body = gear_profile.extrude(face_width)

# Center the gear on Z
gear_body = gear_body.translate((0, 0, -face_width / 2))

# Add the central bore
result = gear_body.faces(">Z").workplane().hole(bore_diameter)