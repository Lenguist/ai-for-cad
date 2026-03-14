import cadquery as cq

# Flange base
result = cq.Workplane("XY").circle(20).extrude(6)

# Four 4mm holes on 32mm bolt circle
result = result.faces(">Z").workplane().polarArray(16, 0, 360, 4).hole(4)

# Shaft on top
result = result.faces(">Z").workplane().circle(10).extrude(30)