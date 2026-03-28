"""
test_physics.py — Unit tests for the geometry-driven kinematic compiler.

Run:  python -m pytest test_physics.py -v
  or  python test_physics.py
"""

import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))

import json
from physics import compile_and_simulate

# ── Load parts library ───────────────────────────────────────────────────────

with open(os.path.join(os.path.dirname(__file__), "parts_library.json")) as f:
    LIB = json.load(f)


# ── Helpers ──────────────────────────────────────────────────────────────────

def assembly(*parts):
    return {"parts": list(parts)}

def part(pid, ptype, pos, axis="x"):
    return {"id": pid, "type": ptype, "pos": pos, "axis": axis}


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_no_parts():
    """Empty assembly → no kinematics."""
    result = compile_and_simulate(assembly(), LIB)
    assert "gear_pairs"  not in result
    assert "rack_pinion" not in result
    assert "motors"      not in result


def test_single_gear_no_motion():
    """One gear with no motor and no mesh → nothing moves."""
    a = assembly(part("g1", "gear-8t", [0, 0, 0], "y"))
    result = compile_and_simulate(a, LIB)
    assert "gear_pairs"  not in result
    assert "motors"      not in result
    assert result.get("angular_velocities", {}) == {}


def test_gear_pair_correct_distance():
    """
    8T (r=1) + 24T (r=3) placed exactly r1+r2=4 studs apart → meshed.
    Ratio derived from geometry: 3/1 = 3.0
    """
    a = assembly(
        part("g1", "gear-8t",  [0, 0, 0], "y"),
        part("g2", "gear-24t", [4, 0, 0], "y"),  # dist=4 = 1+3 ✓
    )
    result = compile_and_simulate(a, LIB)
    assert "gear_pairs" in result
    assert len(result["gear_pairs"]) == 1
    pair = result["gear_pairs"][0]
    assert abs(pair["ratio"] - 3.0) < 0.01


def test_gear_pair_wrong_distance_no_mesh():
    """
    THE KEY TEST: same gears but placed 6 studs apart (gap of 2).
    No contact → no constraint → no gear_pairs in output.
    """
    a = assembly(
        part("g1", "gear-8t",  [0, 0, 0], "y"),
        part("g2", "gear-24t", [6, 0, 0], "y"),  # dist=6, need 4 → GAP
    )
    result = compile_and_simulate(a, LIB)
    assert "gear_pairs" not in result, (
        "Gears at wrong distance should NOT produce a gear pair"
    )


def test_gear_pair_wrong_axis_no_mesh():
    """
    Two gears on perpendicular axes (not worm) → no spur contact.
    """
    a = assembly(
        part("g1", "gear-8t",  [0, 0, 0], "x"),
        part("g2", "gear-24t", [4, 0, 0], "y"),  # different axis
    )
    result = compile_and_simulate(a, LIB)
    assert "gear_pairs" not in result


def test_motor_direct_drive():
    """
    Motor + axle + gear, no reduction → output RPM = motor RPM.
    """
    a = assembly(
        part("m1", "motor-m",  [0,  0, 0], "x"),
        part("a1", "axle-3",   [3,  0, 0], "x"),   # on same axle line
        part("g1", "gear-24t", [4,  0, 0], "x"),   # on same axle line
    )
    result = compile_and_simulate(a, LIB)
    assert "motors" in result
    assert "motor_output" in result
    mo = result["motor_output"]
    assert mo["gear_ratio"] == 1.0
    assert abs(mo["output_rpm"] - 380) < 1.0   # motor-m is 380 RPM


def test_motor_3to1_reduction():
    """
    motor-m (380 RPM) → 8T driving 24T → output = 380/3 ≈ 126.7 RPM
    and torque × 3 × 0.85 = 4 × 3 × 0.85 = 10.2 Ncm
    """
    # gear-8t radius=1, gear-24t radius=3, dist=4
    a = assembly(
        part("m1", "motor-m",  [0, 0, 0], "x"),
        part("a1", "axle-5",   [0, 0, 0], "x"),   # same line as motor output
        part("g1", "gear-8t",  [4, 0, 0], "x"),   # on input axle
        part("g2", "gear-24t", [8, 0, 0], "x"),   # 4 studs from g1 = 1+3 ✓
    )
    result = compile_and_simulate(a, LIB)
    assert "gear_pairs" in result
    assert len(result["gear_pairs"]) == 1

    mo = result["motor_output"]
    assert abs(mo["gear_ratio"] - 3.0) < 0.1
    assert abs(mo["output_rpm"]  - 380/3) < 2.0
    assert abs(mo["output_torque_ncm"] - 4 * 3 * 0.85) < 0.5


def test_axle_coupling():
    """
    Axle and gear on the same center line → same angular velocity group.
    """
    a = assembly(
        part("a1", "axle-5",  [0, 0, 0], "x"),
        part("g1", "gear-8t", [2, 0, 0], "x"),  # center on axle line ✓
    )
    result = compile_and_simulate(a, LIB)
    # Both should be in an axle group (no error; coupling detected)
    # With no motor, nothing moves — but also no error
    assert result.get("angular_velocities", {}) == {}


def test_rack_and_pinion_correct():
    """
    8T gear (r=1) with axis='y' above a rack-4 with axis='x'.
    Perpendicular distance from gear center to rack center = 1 stud ✓
    """
    a = assembly(
        part("g1", "gear-8t", [2, 1, 0], "y"),   # center at y=1
        part("r1", "rack-4",  [0, 0, 0], "x"),   # center at y=0, perp dist = 1 ✓
    )
    result = compile_and_simulate(a, LIB)
    assert "rack_pinion" in result
    assert result["rack_pinion"][0]["gear"] == "g1"
    assert result["rack_pinion"][0]["rack"] == "r1"


def test_rack_no_contact_wrong_distance():
    """
    Gear placed 3 studs above rack (r=1, need 1) → no contact.
    """
    a = assembly(
        part("g1", "gear-8t", [2, 3, 0], "y"),   # 3 studs above rack center
        part("r1", "rack-4",  [0, 0, 0], "x"),
    )
    result = compile_and_simulate(a, LIB)
    assert "rack_pinion" not in result


def test_worm_gear_detection():
    """
    Worm gear (r=1, axis='x') meshing with 24T gear (r=3, axis='z').
    Axes must be truly skew (not intersecting).
    Worm along x at y=0,z=0; gear along z at x=0,y=4,z=0.
    Skew line distance = 4 = r_worm(1) + r_gear(3) ✓

    Note: gear axis='y' would make the lines intersect (both in z=0 plane),
    giving distance=0. Must use a third axis.
    """
    a = assembly(
        part("w1", "gear-worm", [0, 0, 0], "x"),
        part("g1", "gear-24t",  [0, 4, 0], "z"),  # axis='z', skew dist = 4 ✓
    )
    result = compile_and_simulate(a, LIB)
    assert "gear_pairs" in result, "Worm-gear contact should be detected"
    pair = result["gear_pairs"][0]
    # Convention: ratio = r_driven/r_driving = r_gear/r_worm = 3/1 = 3.0
    # (same as checker.py: ratio > 1 means speed reduction)
    assert abs(pair["ratio"] - 3.0) < 0.1, f"Expected 3.0, got {pair['ratio']}"


def test_compound_gear_train():
    """
    Two-stage 3:1 compound train → total 9:1.
    Stage 1: 8T (r=1) drives 24T (r=3) on intermediate axle.
    Stage 2: 8T (r=1) on intermediate axle drives 24T (r=3) on output.
    """
    a = assembly(
        # Input axle: 8T input gear
        part("g1", "gear-8t",  [0, 0, 0], "y"),
        # Intermediate axle: 24T driven + 8T driving
        part("g2", "gear-24t", [4, 0, 0], "y"),  # dist from g1 = 4 = 1+3 ✓
        part("g3", "gear-8t",  [4, 0, 0], "y"),  # same axle as g2 (coupled)
        # Output axle: 24T
        part("g4", "gear-24t", [8, 0, 0], "y"),  # dist from g3 = 4 = 1+3 ✓
    )
    result = compile_and_simulate(a, LIB)
    assert "gear_pairs" in result
    # Should detect 2 gear pairs
    assert len(result["gear_pairs"]) == 2


def test_unknown_part_type_skipped():
    """Parts not in library are silently skipped."""
    a = assembly(
        part("x1", "nonexistent-part", [0, 0, 0], "x"),
        part("g1", "gear-8t",          [0, 0, 0], "y"),
    )
    result = compile_and_simulate(a, LIB)   # should not raise


# ── Run directly ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  ✓  {fn.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗  {fn.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
