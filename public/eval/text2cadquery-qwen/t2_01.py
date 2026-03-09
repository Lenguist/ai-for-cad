import cadquery as cq

# --- Part 1: Rectangular Plate with Hole ---
plate_length = 0.5 * 0.5  # Scaled length
plate_width = 0.3 * 0.5  # Scaled width
plate_height = 0.05

hole_center_x = 0.25 * 0.5  # Scaled center x
hole_center_y = 0.15 * 0.5  # Scaled center y
hole_radius = 0.04 * 0.5  # Scaled radius

part_1 = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_height)
    .faces(">Z")
    .workplane()
    .moveTo(hole_center_x - (plate_length/2), hole_center_y - (plate_width/2))
    .circle(hole_radius)
    .cutThruAll()
)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.translate((0.125, 0.125, 0))

# --- Assembly ---
assembly = part_1

# --- Export to STL ---
cq.exporters.export(assembly, "./stlcq/0069/00697000.stl")