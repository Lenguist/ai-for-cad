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

# Function to generate involute point at parameter t
def involute_point(base_r, t):
    """Return (x, y) on the involute curve for parameter t (radians)."""
    x = base_r * (math.cos(t) + t * math.sin(t))
    y = base_r * (math.sin(t) - t * math.cos(t))
    return (x, y)

# Find the involute parameter t for a given radius
def involute_param_at_radius(base_r, r):
    """Find t such that the involute is at radius r."""
    if r <= base_r:
        return 0.0
    return math.sqrt((r / base_r) ** 2 - 1)

# Involute function: inv(alpha) = tan(alpha) - alpha
def involute_function(angle):
    return math.tan(angle) - angle

# Angular half-thickness of tooth at pitch circle
tooth_half_angle = math.pi / (2 * num_teeth) + involute_function(pa_rad)

# Generate one tooth profile and replicate
# We'll build the gear as a 2D profile then extrude

# Parameters for involute sampling
t_tip = involute_param_at_radius(base_radius, outer_radius)
t_root = involute_param_at_radius(base_radius, root_radius)
num_points = 20

# Build one tooth profile (right side involute)
def get_involute_profile(base_r, t_max, num_pts):
    points = []
    for i in range(num_pts + 1):
        t = t_max * i / num_pts
        pt = involute_point(base_r, t)
        points.append(pt)
    return points

# Get right side involute points
right_involute = get_involute_profile(base_radius, t_tip, num_points)

# The involute starts at angle 0 on base circle. We need to rotate
# the tooth so it's symmetric about a radial line.
# The angular position of the involute at the pitch circle:
t_pitch = involute_param_at_radius(base_radius, pitch_radius)
pitch_angle_right = math.atan2(involute_point(base_radius, t_pitch)[1],
                                involute_point(base_radius, t_pitch)[0])

# Rotation to center the tooth: rotate right involute by tooth_half_angle - pitch_angle_right
rotation_angle = tooth_half_angle - pitch_angle_right

def rotate_point(px, py, angle):
    cs = math.cos(angle)
    sn = math.sin(angle)
    return (px * cs - py * sn, px * sn + py * cs)

def mirror_point_x(px, py):
    """Mirror about x-axis."""
    return (px, -py)

# Build complete gear profile as a list of (x,y) tuples
gear_points = []

for tooth_idx in range(num_teeth):
    tooth_angle = tooth_idx * 2 * math.pi / num_teeth
    
    # Right flank (rotated and then rotated to tooth position)
    right_pts = []
    for pt in right_involute:
        rp = rotate_point(pt[0], pt[1], rotation_angle + tooth_angle)
        right_pts.append(rp)
    
    # Left flank (mirror of right about tooth center, then rotate to tooth position)
    left_pts = []
    for pt in right_involute:
        mp = mirror_point_x(pt[0], pt[1])
        rp = rotate_point(mp[0], mp[1], -rotation_angle + tooth_angle)
        left_pts.append(rp)
    left_pts.reverse()
    
    # Tip arc: connect right_pts[-1] to left_pts[0] via the tip (approximation: straight line or arc)
    # Root arc: connect left_pts[-1] to next tooth's right_pts[0] via root circle
    
    # Add right flank
    gear_points.extend(right_pts)
    # Add left flank  
    gear_points.extend(left_pts)
    
    # Add root fillet point (arc along root circle to next tooth)
    next_tooth_angle = (tooth_idx + 1) * 2 * math.pi / num_teeth
    next_right_start = rotate_point(right_involute[0][0], right_involute[0][1],
                                     rotation_angle + next_tooth_angle)
    
    # Current left end
    left_end = left_pts[-1]
    left_end_angle = math.atan2(left_end[1], left_end[0])
    next_right_angle = math.atan2(next_right_start[1], next_right_start[0])
    
    if next_right_angle < left_end_angle:
        next_right_angle += 2 * math.pi
    
    # Add points along root circle
    num_root_pts = 5
    for i in range(1, num_root_pts):
        a = left_end_angle + (next_right_angle - left_end_angle) * i / num_root_pts
        gear_points.append((root_radius * math.cos(a), root_radius * math.sin(a)))

# Close the profile by connecting back to start
# Convert to the format cadquery expects (list of 2D tuples, starting from the second point)
# We use a polyline through all points

# Create the 2D wire and extrude
# CadQuery's polyline needs relative or absolute coordinates on a workplane

# Use CadQuery's Wire approach
edges = []
wire_points = gear_points

# Build gear as a 2D profile extruded
# Start from the first point, draw lines through all others
start_point = wire_points[0]

# Create a workplane and use lineTo for each point
gear_profile = cq.Workplane("XY").moveTo(wire_points[0][0], wire_points[0][1])

for i in range(1, len(wire_points)):
    gear_profile = gear_profile.lineTo(wire_points[i][0], wire_points[i][1])

gear_profile = gear_profile.close()

# Extrude the gear profile
gear = gear_profile.extrude(face_width)

# Center the gear vertically
gear = gear.translate((0, 0, -face_width / 2.0))

# Cut the central bore
gear = gear.faces(">Z").workplane().hole(bore_diameter)

result = gear