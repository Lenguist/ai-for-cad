import cadquery as cq

# --- Part 1: Disk with Holes ---
disk_radius = 0.025 * 0.05  # Sketch radius scaled
hole_radius = 0.004 * 0.05  # Hole radius scaled
disk_height = 0.008

hole_centers = [
    (0.0105 * 0.05, 0.0105 * 0.05),
    (0.0105 * 0.05, 0.0395 * 0.05),
    (0.0395 * 0.05, 0.0105 * 0.05),
    (0.0395 * 0.05, 0.0395 * 0.05)
]

part_1 = cq.Workplane("XY").circle(disk_radius).extrude(disk_height)

for center_x, center_y in hole_centers:
    part_1 = part_1.faces(">Z").workplane().moveTo(center_x - disk_radius, center_y - disk_radius).circle(hole_radius).cutThruAll()

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.0675, 0.0675, 0))

# --- Assembly ---
assembly = part_1

# --- Export to STL ---
cq.exporters.export(assembly, "./stlcq/0010/00100220.stl")