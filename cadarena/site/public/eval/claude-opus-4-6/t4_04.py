import cadquery as cq
import math

# Spring parameters
outer_diameter = 20.0  # mm
wire_diameter = 1.5  # mm
active_coils = 10
free_length = 50.0  # mm
mean_diameter = outer_diameter - wire_diameter
mean_radius = mean_diameter / 2.0

# Flat ground ends: typically 1 dead coil at each end (ground flat)
dead_coils_per_end = 1.0
total_coils = active_coils + 2 * dead_coils_per_end  # 12 total coils

# Pitch for active coils
# The dead coils at each end have zero pitch (flat)
# Total height = dead_end_height_bottom + active_height + dead_end_height_top
# For ground ends, the dead coils are compressed (pitch ~ 0) and ground flat
# Free length = active_coils * pitch + 2 * wire_diameter (approx for flat ends)
pitch = (free_length - 2 * wire_diameter) / active_coils

# Build the helix as a swept circle along a helical path
# We'll create the path using points along the helix
# Break into segments: bottom dead coil + active coils + top dead coil

segments_per_coil = 60  # points per coil for smoothness

# Build the helical spine points
points = []

# Bottom dead coil (ground flat - no rise, 1 coil)
n_bottom = int(dead_coils_per_end * segments_per_coil)
for i in range(n_bottom + 1):
    t = i / segments_per_coil  # fraction of coil
    angle = 2 * math.pi * t
    x = mean_radius * math.cos(angle)
    y = mean_radius * math.sin(angle)
    # Gradual transition: start at z = wire_diameter/2 (ground flat sits at z=0)
    z = wire_diameter / 2.0  # flat at bottom
    points.append((x, y, z))

# Active coils (with pitch)
z_start = wire_diameter / 2.0
n_active = int(active_coils * segments_per_coil)
for i in range(1, n_active + 1):
    t = i / segments_per_coil  # fraction of coil
    angle = 2 * math.pi * (dead_coils_per_end + t)
    x = mean_radius * math.cos(angle)
    y = mean_radius * math.sin(angle)
    z = z_start + (t / active_coils) * (active_coils * pitch)
    points.append((x, y, z))

# Top dead coil (ground flat - no rise, 1 coil)
z_top = z_start + active_coils * pitch
n_top = int(dead_coils_per_end * segments_per_coil)
for i in range(1, n_top + 1):
    t = i / segments_per_coil
    angle = 2 * math.pi * (dead_coils_per_end + active_coils + t)
    x = mean_radius * math.cos(angle)
    y = mean_radius * math.sin(angle)
    z = z_top + wire_diameter / 2.0 - wire_diameter / 2.0  # flat at top
    z = z_top
    points.append((x, y, z))

# Add transition zones: smooth the transition from flat to helical
# Re-build with proper transitions
points = []
transition_coils = 0.5  # half coil for transition

total_segments = int(total_coils * segments_per_coil)
for i in range(total_segments + 1):
    coil_pos = i / segments_per_coil  # position in coils from start
    angle = 2 * math.pi * coil_pos
    x = mean_radius * math.cos(angle)
    y = mean_radius * math.sin(angle)
    
    # Calculate z based on position
    if coil_pos <= dead_coils_per_end:
        # Bottom dead coil - flat
        z = wire_diameter / 2.0
    elif coil_pos >= (total_coils - dead_coils_per_end):
        # Top dead coil - flat
        z = wire_diameter / 2.0 + active_coils * pitch
    else:
        # Active region
        active_pos = coil_pos - dead_coils_per_end
        z = wire_diameter / 2.0 + active_pos * pitch
    
    points.append((x, y, z))

# Create the helix path as a spline
path = cq.Workplane("XZ").spline(points)

# Create the wire cross-section at the start of the path
# Position the circle at the first point, perpendicular to the path
start_point = points[0]
next_point = points[1]
tangent = (next_point[0] - start_point[0], next_point[1] - start_point[1], next_point[2] - start_point[2])

# Sweep a circle along the helical path
result = (
    cq.Workplane("XY")
    .center(start_point[0], start_point[1])
    .workplane(offset=start_point[2])
    .circle(wire_diameter / 2.0)
    .sweep(path, isFrenet=True)
)