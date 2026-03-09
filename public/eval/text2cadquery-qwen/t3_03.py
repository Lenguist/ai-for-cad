import cadquery as cq

# --- Part 1 ---
part_1 = (
    cq.Workplane("XY")
    .moveTo(0.0, 0.0)
    .lineTo(0.0804 * 0.0804, 0.0)
    .lineTo(0.0804 * 0.0804, 0.0402 * 0.0804)
    .lineTo(0.0402 * 0.0804, 0.0402 * 0.0804)
    .lineTo(0.0402 * 0.0804, 0.0804 * 0.0804)
    .lineTo(0.0, 0.0804 * 0.0804)
    .lineTo(0.0, 0.0)
    .close()
    .extrude(-0.0201)
)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.rotate((0, 0, 0), (0, 0, 1), -90)
part_1 = part_1.translate((0, 0.0201, 0))

# --- Assembly ---
assembly = part_1

cq.exporters.export(assembly, "./stlcq/0035/00357000.stl")