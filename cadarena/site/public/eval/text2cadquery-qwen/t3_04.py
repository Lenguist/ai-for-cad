import cadquery as cq

# --- Part 1 ---
sketch_scale = 0.75
extrude_depth_bottom = 0.01 * sketch_scale
extrude_depth_middle = 0.02 * sketch_scale
extrude_depth_top = 0.015 * sketch_scale

outer_radius_bottom = 0.01 * sketch_scale
inner_radius_bottom = 0.005 * sketch_scale

outer_radius_middle = 0.007 * sketch_scale
inner_radius_middle = 0.005 * sketch_scale

outer_radius_top = 0.005 * sketch_scale
inner_radius_top = 0.0035 * sketch_scale

part_1 = (
    cq.Workplane("XY")
    # Bottom Cylinder
    .moveTo(0.01 * sketch_scale, 0.01 * sketch_scale)
    .circle(outer_radius_bottom)
    .moveTo(0.01 * sketch_scale, 0.01 * sketch_scale)
    .circle(inner_radius_bottom)
    .extrude(extrude_depth_bottom)

    # Middle Cylinder
    .moveTo(0.01 * sketch_scale, 0.01 * sketch_scale)
    .circle(outer_radius_middle)
    .moveTo(0.01 * sketch_scale, 0.01 * sketch_scale)
    .circle(inner_radius_middle)
    .extrude(extrude_depth_middle)

    # Top Cylinder
    .moveTo(0.01 * sketch_scale, 0.01 * sketch_scale)
    .circle(outer_radius_top)
    .moveTo(0.01 * sketch_scale, 0.01 * sketch_scale)
    .circle(inner_radius_top)
    .extrude(extrude_depth_top)
)

# --- Coordinate System Transformation for Part 1 ---
part_1 = part_1.rotate((0, 0, 0), (0, 0, 1), -90)
part_1 = part_1.translate((0, 0.015, 0))

# --- Assembly ---
assembly = part_1

cq.exporters.export(assembly, "./stlcq/0086/00860020.stl")