// Main body dimensions
module main_body() {
    difference() {
        cube([105, 65, 25], center = false); // Main box
        filleted_corners(); // Add filleted corners
    }
}

// Filleted corners approximation
module filleted_corners() {
    for (x = [0, 105]) {
        for (y = [0, 65]) {
            translate([x, y, 0]) sphere(r = 2);
        }
    }
}

// USB port
module usb_port() {
    translate([65 / 2 - 7.25, -30, 25 / 2 - 0.75])
        cube([14.5, 6, 1.5]);
}

// DC port
module dc_port() {
    translate([65 / 2 - 10, -30, 25 / 2 - 0.75])
        cylinder(r = 5.5 / 2, h = 1.5, center = false);
}

// Switch
module switch_cutout() {
    translate([65 / 2 + 10, -30, 25 / 2 - 1])
        cube([6, 10, 2]);
}

// LED holes
module led_holes() {
    for (i = [0:4])
        translate([15 + i * 15, 0, 25 - 0.25])
            cylinder(r = 1, h = 0.5, center = false);
}

// Final model
difference() {
    main_body();
    usb_port();
    dc_port();
    switch_cutout();
    led_holes();
}

// Save STL programmatically
// This line is ignored in OpenSCAD GUI, but you can execute this in a terminal
// OpenSCAD CLI command: openscad -o battery.stl battery.scad
