import cadquery as cq
import math

# Gear parameters
num_teeth = 20
module = 2.0
pitch_diameter = num_teeth * module  # 40mm
face_width = 10.0
bore_diameter = 8.0

# Derived gear geometry
pressure_angle = 20.0  # degrees, standard
pa_rad = math.radians(pressure_angle)

addendum = module  # 2mm
dedendum = 1.25 * module  # 2.5mm

outer_radius = pitch_diameter / 2.0 + addendum  # 22mm
root_radius = pitch_diameter / 2.0 - dedendum  # 17.5mm
base_radius = (pitch_diameter / 2.0) * math.cos(pa_rad)  # base circle radius
pitch_radius = pitch_diameter / 2.0  # 20mm

# Function to generate involute curve point at parameter t
def involute_point(base_r, t):
    """Return (x, y) on the involute of a circle with radius base_r at parameter t (radians)."""
    x = base_r * (math.cos(t) + t * math.sin(t))
    y = base_r * (math.sin(t) - t * math.cos(t))
    return (x, y)

# Find the involute parameter t for a given radius
def involute_param_at_radius(base_r, r):
    if r <= base_r:
        return 0.0
    return math.sqrt((r / base_r) ** 2 - 1)

# Involute angle at a given radius
def involute_angle(base_r, r):
    if r <= base_r:
        return 0.0
    t = involute_param_at_radius(base_r, r)
    return t - math.atan(t)

# Angular tooth thickness at pitch circle
# At pitch circle, tooth thickness = pi * module / 2
tooth_thickness_pitch = math.pi * module / 2.0
half_tooth_angle_pitch = tooth_thickness_pitch / (2.0 * pitch_radius)

# Involute angle at pitch radius
inv_at_pitch = involute_angle(base_radius, pitch_radius)

# Build one tooth profile
# The tooth is symmetric about its center line
# We'll generate points for the right flank (involute) and mirror for left

num_points = 20

# Parameter range for involute: from base circle to outer circle
t_base = 0.0
t_outer = involute_param_at_radius(base_radius, outer_radius)

# Generate right side involute points
right_flank_points = []
for i in range(num_points + 1):
    t = t_base + (t_outer - t_base) * i / num_points
    x, y = involute_point(base_radius, t)
    r = math.sqrt(x**2 + y**2)
    angle = math.atan2(y, x)
    # Rotate so that at pitch circle, the tooth surface is at half_tooth_angle_pitch
    angle_offset = half_tooth_angle_pitch + inv_at_pitch
    new_angle = angle + angle_offset
    right_flank_points.append((r * math.cos(new_angle), r * math.sin(new_angle)))

# Generate left side involute points (mirror of right side about x-axis, then rotate)
left_flank_points = []
for i in range(num_points + 1):
    t = t_base + (t_outer - t_base) * i / num_points
    x, y = involute_point(base_radius, t)
    r = math.sqrt(x**2 + y**2)
    angle = math.atan2(y, x)
    angle_offset = half_tooth_angle_pitch + inv_at_pitch
    new_angle = -(angle + angle_offset)
    left_flank_points.append((r * math.cos(new_angle), r * math.sin(new_angle)))

# Build the full gear profile as a list of 2D points
tooth_angle = 2.0 * math.pi / num_teeth
gear_points = []

for tooth in range(num_teeth):
    rotation = tooth * tooth_angle

    # Left flank (from root to tip)
    for i, pt in enumerate(reversed(left_flank_points)):
        r = math.sqrt(pt[0]**2 + pt[1]**2)
        a = math.atan2(pt[1], pt[0]) + rotation
        if r < root_radius:
            r = root_radius
        gear_points.append((r * math.cos(a), r * math.sin(a)))

    # Right flank (from tip to root)
    for i, pt in enumerate(right_flank_points):
        r = math.sqrt(pt[0]**2 + pt[1]**2)
        a = math.atan2(pt[1], pt[0]) + rotation
        if r < root_radius:
            r = root_radius
        gear_points.append((r * math.cos(a), r * math.sin(a)))

    # Root arc to next tooth - connect to next tooth's left flank at root
    next_rotation = (tooth + 1) * tooth_angle
    last_right_pt = right_flank_points[0]
    r_root = root_radius
    a_end = math.atan2(last_right_pt[1], last_right_pt[0]) + rotation
    next_left_pt = left_flank_points[-1]
    a_start_next = math.atan2(next_left_pt[1], next_left_pt[0]) + next_rotation

    # Add a few points along the root circle
    num_root_pts = 3
    for j in range(1, num_root_pts + 1):
        frac = j / (num_root_pts + 1)
        a_interp = a_end + frac * (a_start_next - a_end)
        gear_points.append((r_root * math.cos(a_interp), r_root * math.sin(a_interp)))

# Close the profile
gear_points.append(gear_points[0])

# Create the gear as a 2D wire then extrude
gear_2d = cq.Workplane("XY").polyline(gear_points).close()
gear_3d = gear_2d.extrude(face_width)

# Center the gear vertically
gear_3d = gear_3d.translate((0, 0, -face_width / 2.0))

# Add the central bore
result = gear_3d.faces(">Z").workplane().hole(bore_diameter)