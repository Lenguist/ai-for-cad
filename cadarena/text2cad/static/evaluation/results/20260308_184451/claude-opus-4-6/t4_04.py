import cadquery as cq
import math

# Spring parameters
outer_diameter = 20.0  # mm
wire_diameter = 1.5  # mm
active_coils = 10
free_length = 50.0  # mm
mean_radius = (outer_diameter - wire_diameter) / 2.0  # 9.25 mm

# Total coils including ground ends (add ~1 coil total for flat ground ends)
dead_coils_each_end = 0.75  # typical for flat ground ends
total_coils = active_coils + 2 * dead_coils_each_end  # 11.5

# Pitch for active coils region
# Free length = active coils * pitch + 2 * dead_coil_height
# Dead coil height is roughly wire_diameter (ground flat)
dead_coil_height = wire_diameter * dead_coils_each_end
active_length = free_length - 2 * dead_coil_height
pitch = active_length / active_coils

# Build the helix as a swept circle along a helical path
# We'll create the path using many points

num_points_per_coil = 60
total_points = int(total_coils * num_points_per_coil) + 1

# Build helical spine points with variable pitch
# Bottom dead coils: constant low pitch (nearly zero for ground ends)
# Active coils: constant pitch
# Top dead coils: constant low pitch

path_points = []
for i in range(total_points):
    t = i / num_points_per_coil  # t in units of coils
    
    # Angle
    angle = 2.0 * math.pi * t
    
    # Calculate z based on which section we're in
    if t <= dead_coils_each_end:
        # Bottom dead coil region - transition from flat to pitched
        # Linear transition in pitch from 0 to full pitch
        frac = t / dead_coils_each_end
        # Smooth transition using sine
        z = dead_coil_height * (frac - math.sin(math.pi * frac) / math.pi) / (1 - 0)
        # Simple linear rise over dead coil region
        z = (t / dead_coils_each_end) * dead_coil_height
        # Use smooth transition
        frac = t / dead_coils_each_end
        z = dead_coil_height * (0.5 - 0.5 * math.cos(math.pi * frac))
    elif t <= dead_coils_each_end + active_coils:
        # Active coil region - constant pitch
        active_t = t - dead_coils_each_end
        z = dead_coil_height + active_t * pitch
    else:
        # Top dead coil region - transition from pitched to flat
        top_t = t - dead_coils_each_end - active_coils
        frac = top_t / dead_coils_each_end
        z = dead_coil_height + active_length + dead_coil_height * (0.5 - 0.5 * math.cos(math.pi * frac))
    
    x = mean_radius * math.cos(angle)
    y = mean_radius * math.sin(angle)
    
    path_points.append((x, y, z))

# Create the helix path as a spline
helix_path = cq.Workplane("XY").spline(path_points)

# Get the wire from the path
path_wire = helix_path.val()

# Create the sweep cross-section at the start of the path
# We need a circle perpendicular to the helix at the start point
start_point = path_points[0]
# Direction at start
dx = path_points[1][0] - path_points[0][0]
dy = path_points[1][1] - path_points[0][1]
dz = path_points[1][2] - path_points[0][2]
length_dir = math.sqrt(dx*dx + dy*dy + dz*dz)
dx, dy, dz = dx/length_dir, dy/length_dir, dz/length_dir

# Create the spring by sweeping a circle along the helix
# Use CQ's sweep functionality
path_edges = helix_path.val()

# Build path as a Wire
wire = cq.Wire.assembleEdges([path_edges])

# Create circle at start point, perpendicular to tangent
result = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(start_point[0], start_point[1], start_point[2]),
                 rotate=cq.Vector(0, 0, 0))
    .circle(wire_diameter / 2.0)
    .sweep(helix_path, isFrenet=True)
)