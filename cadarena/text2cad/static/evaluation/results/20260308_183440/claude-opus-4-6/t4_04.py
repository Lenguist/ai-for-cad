import cadquery as cq
import math

# Spring parameters
outer_diameter = 20.0  # mm
wire_diameter = 1.5  # mm
active_coils = 10
free_length = 50.0  # mm
mean_diameter = outer_diameter - wire_diameter
mean_radius = mean_diameter / 2.0

# Flat ground ends add approximately 1 dead coil at each end
# Total coils = active coils + 2 dead coils (1 each end)
dead_coils_per_end = 1.0
total_coils = active_coils + 2 * dead_coils_per_end

# Pitch for active coils region
# Free length = solid height of dead coils + active coil pitch * active_coils
# For flat ground ends, the dead coils are compressed (pitch = wire_diameter)
dead_coil_height = dead_coils_per_end * wire_diameter * 2  # top and bottom
active_length = free_length - dead_coil_height
pitch = active_length / active_coils

# Build the helix as a swept wire along a helical path
# We'll create the path using points and then sweep a circle along it

# Number of segments per coil for smoothness
segments_per_coil = 60
total_segments = int(total_coils * segments_per_coil)

# Build helix points with variable pitch for ground ends
# Bottom dead coil: coil 0 to dead_coils_per_end - gradual transition
# Active coils: dead_coils_per_end to dead_coils_per_end + active_coils
# Top dead coil: last dead_coils_per_end coils

points = []
for i in range(total_segments + 1):
    coil_fraction = i / segments_per_coil  # which coil we're on (float)
    angle = coil_fraction * 2 * math.pi  # total angle in radians
    
    # Calculate z based on which region we're in
    if coil_fraction <= dead_coils_per_end:
        # Bottom ground end - flat (pitch = ~0, gradually increasing)
        # Transition from 0 pitch to active pitch
        t = coil_fraction / dead_coils_per_end  # 0 to 1
        # Use smooth transition
        local_pitch = wire_diameter * (1 - t) + pitch * t * 0.5
        z = wire_diameter * 0.5 * t * coil_fraction
        # Simple linear approach for dead coil
        z = coil_fraction * wire_diameter * 0.5
    elif coil_fraction >= (total_coils - dead_coils_per_end):
        # Top ground end
        coils_into_top = coil_fraction - (total_coils - dead_coils_per_end)
        t = coils_into_top / dead_coils_per_end  # 0 to 1
        # Height at start of top dead coil
        z_start = dead_coils_per_end * wire_diameter * 0.5 + active_coils * pitch
        z = z_start + (1 - 0.5 * t) * wire_diameter * 0.5 * coils_into_top
    else:
        # Active coils region
        active_fraction = coil_fraction - dead_coils_per_end
        z_bottom = dead_coils_per_end * wire_diameter * 0.5
        z = z_bottom + active_fraction * pitch
    
    x = mean_radius * math.cos(angle)
    y = mean_radius * math.sin(angle)
    points.append((x, y, z))

# Normalize z so total height = free_length
z_min = min(p[2] for p in points)
z_max = max(p[2] for p in points)
current_height = z_max - z_min
if current_height > 0:
    scale = free_length / current_height
    points = [(p[0], p[1], (p[2] - z_min) * scale) for p in points]

# Create the helix path as a spline
helix_path = cq.Workplane("XY").spline(points)

# Create the wire cross-section at the start point
# Position workplane at the first point, perpendicular to the helix
start_point = points[0]
direction = (points[1][0] - points[0][0], 
             points[1][1] - points[0][1], 
             points[1][2] - points[0][2])

# Use CadQuery sweep approach
# Create path as a 3D spline wire
path_edges = cq.Workplane("XY").spline(points).val()

# Build the spring using sweep
path_wire = cq.Wire.assembleEdges([path_edges])

# Create circle at start for sweeping
circle_plane = cq.Workplane("XY").transformed(offset=start_point).circle(wire_diameter / 2.0)

result = circle_plane.sweep(cq.Workplane("XY").spline(points), isFrenet=True)