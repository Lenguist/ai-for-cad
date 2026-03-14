import cadquery as cq

arm1 = cq.Workplane("XY").rect(60, 20, centered=False).extrude(5)
arm2 = cq.Workplane("XY").rect(20, 40, centered=False).extrude(5)
result = arm1.union(arm2)