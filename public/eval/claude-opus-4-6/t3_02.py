import cadquery as cq

# Create outer box
outer = cq.Workplane("XY").box(60, 50, 40)

# Create inner box to hollow out
# Inner dimensions: (60-2*3) x (50-2*3) x (40-3) = 54 x 44 x 37
# The inner box is shifted up by 3/2 = 1.5mm to keep 3mm bottom wall and open top
inner = cq.Workplane("XY").box(54, 44, 37).translate((0, 0, 1.5))

# Cut inner from outer to create hollow box open on top
result = outer.cut(inner)