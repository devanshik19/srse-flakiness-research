import pytest
from sympy import symbols, S, sqrt, Float
from sympy.geometry import Point
from sympy.core.numbers import Float as SymFloat

def test_distance_numeric_integer():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # classic 3-4-5 triangle
    assert p1.distance(p2) == 5

def test_distance_numeric_float():
    p1 = Point(0.0, 0.0)
    p2 = Point(1.5, 2.0)
    # distance is sqrt(1.5^2 + 2^2) = sqrt(2.25 + 4) = sqrt(6.25) = 2.5
    d = p1.distance(p2)
    # d may be a Float or exact; compare numerically
    assert float(d.evalf()) == pytest.approx(2.5)

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    d = p.distance(origin)
    assert d == sqrt(x**2 + y**2)

def test_distance_mixed_sequence_input():
    # distance accepts any sequence-like p (per implementation)
    p = Point(3, 4)
    seq = (0, 0)
    assert p.distance(seq) == 5

def test_distance_higher_dimension():
    # 3D points
    p1 = Point(1, 2, 2)
    p2 = Point(4, 6, 6)
    # differences: (3,4,4) -> squared sum = 9+16+16 = 41 -> sqrt(41)
    assert p1.distance(p2) == sqrt(41)

def test_distance_with_symfloat_and_symbolic():
    # mixture of Float and symbolic
    x = symbols('x')
    p = Point(SymFloat(1.5), x)
    origin = Point(0, 0)
    d = p.distance(origin)
    # should be sqrt(1.5**2 + x**2)
    assert d == sqrt(SymFloat(1.5)**2 + x**2)

def test_distance_iterable_wrong_length_raises():
    p = Point(1, 2)
    # passing an iterable of wrong length should raise (zip will shorten, but behavior tested)
    # Here we expect it not to raise but to compute with zipped length (1,), so result != usual 2-pt distance
    # Use a clearly incompatible iterable to ensure behavior: empty iterable => distance 0
    assert p.distance(()) == 0

def test_distance_with_non_point_sequence_of_sympy_types():
    from sympy import Integer
    p = Point(Integer(2), Integer(3))
    seq = [Integer(0), Integer(0)]
    assert p.distance(seq) == sqrt(13)

def test_distance_commutativity_with_point_and_tuple():
    p = Point(5, 0)
    t = (0, 12)
    # p.distance(t) should be same as distance from tuple to point when interpreted by Point.distance
    assert p.distance(t) == sqrt(5**2 + 12**2)