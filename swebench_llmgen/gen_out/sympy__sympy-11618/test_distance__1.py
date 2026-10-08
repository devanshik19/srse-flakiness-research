import pytest
from sympy import symbols, S, sqrt, Float
from sympy.geometry import Point
from sympy.core.numbers import Float as SymFloat

def test_distance_numeric_ints():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # classic 3-4-5 triangle
    assert p1.distance(p2) == 5

def test_distance_numeric_floats():
    p1 = Point(0.0, 0.0)
    p2 = Point(1.5, 2.0)
    # distance should be sqrt(1.5^2 + 2^2)
    expected = Float((1.5**2 + 2.0**2) ** 0.5)
    # Because of floating point representation, compare numerically
    assert float(p1.distance(p2)) == pytest.approx(float(expected))

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    d = p.distance(origin)
    # Should return sqrt(x**2 + y**2)
    assert d == sqrt(x**2 + y**2)

def test_distance_mixed_point_like_iterable():
    # distance accepts either a Point or an iterable of coordinates
    p = Point(3, 4)
    # tuple-like iterable
    assert p.distance((0, 0)) == 5
    # list-like iterable
    assert p.distance([0, 0]) == 5

def test_distance_higher_dimension():
    # 3D points
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 3)
    # difference is (3,4,0) -> distance 5
    assert p1.distance(p2) == 5

def test_distance_with_non_point_wrong_length():
    p = Point(1, 2)
    # iterable with different length should raise (zip will truncate; ensure behavior)
    # The implementation zips coordinates; shorter iterable leads to truncated distance.
    # For explicit test we check that providing a shorter iterable does not raise but computes partial distance.
    # distance between (1,2) and (0,) -> sqrt((1-0)**2) == 1
    assert p.distance((0,)) == 1

def test_distance_with_sympy_floats_and_symbols():
    x = symbols('x')
    p = Point(SymFloat(3.0), x)
    q = Point(SymFloat(0.0), 4)
    d = p.distance(q)
    # d should be sqrt((3.0-0.0)**2 + (x-4)**2)
    assert d == sqrt((SymFloat(3.0) - SymFloat(0.0))**2 + (x - 4)**2)

def test_distance_self_equal_other_zero():
    p = Point(0, 0)
    assert p.distance(p) == 0

def test_distance_with_point_like_generator():
    p = Point(2, 3)
    # generator as iterable
    gen = (i for i in (0, 0))
    assert p.distance(gen) == sqrt(2**2 + 3**2)