import cadquery as cq

# --- Part 1: L-shaped Bracket ---
sketch_scale = 0.75
extrude_depth = 0.05 * sketch_scale

# Scaled dimensions
p1 = (0.0 * sketch_scale, 0.3 * sketch_scale)
p2 = (0.05 * sketch_scale, 0.3 * sketch_scale)
p3 = (0.05 * sketch_scale, 0.4 * sketch_scale)
p4 = (0.0 * sketch_scale, 0.4 * sketch_scale)

p5 = (0.05 * sketch_scale, 0.0 * sketch_scale)
p6 = (0.65 * sketch_scale, 0.0 * sketch_scale)
p7 = (0.65 * sketch_scale, 0.3 * sketch_scale)
p8 = (0.6 * sketch_scale, 0.3 * sketch_scale)
p9 = (0.6 * sketch_scale, 0.4 * sketch_scale)
p10 = (0.65 * sketch_scale, 0.4 * sketch_scale)
p11 = (0.65 * sketch_scale, 0.7 * sketch_scale)
p12 = (0.0 * sketch_scale, 0.7 * sketch_scale)

part_1 = (
    cq.Workplane("XY")
    .moveTo(p1[0], p1[1])
    .lineTo(p2[0], p2[1])
    .lineTo(p3[0], p3[1])
    .lineTo(p4[0], p4[1])
    .close()
    .moveTo(p5[0], p5[1])
    .lineTo(p6[0], p6[1])
    .lineTo(p7[0], p7[1])
    .lineTo(p8[0], p8[1])
    .lineTo(p9[0], p9[1])
    .lineTo(p10[0], p10[1])
    .lineTo(p11[0], p11[1])
    .lineTo(p12[0], p12[1])
    .close()
    .extrude(extrude_depth)
)

# --- Assembly ---
assembly = part_1

# Export to STL
cq.exporters.export(assembly, "./stlcq