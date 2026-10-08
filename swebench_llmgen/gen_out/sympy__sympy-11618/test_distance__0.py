import pytest
from sympy import symbols, sqrt, Float, N
from sympy.geometry import Point
from sympy.core.numbers import Float as SymFloat

def test_distance_numeric_ints():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # integer coordinates, exact distance 5
    assert p1.distance(p2) == 5
    # symmetric
    assert p2.distance(p1) == 5
    # zero distance to itself
    assert p1.distance(p1) == 0

def test_distance_numeric_floats():
    p1 = Point(0.0, 0.0)
    p2 = Point(1.5, -2.5)
    # distance returns a Float or expression that numerically equals expected value
    d = p1.distance(p2)
    assert float(N(d)) == pytest.approx(((1.5**2) + (-2.5**2))**0.5)

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    d = p.distance(origin)
    # should be sqrt(x**2 + y**2)
    assert d == sqrt(x**2 + y**2)

def test_distance_with_iterable_like_point():
    # distance accepts an iterable (not necessarily a Point instance)
    p = Point(3, 4)
    # provide tuple directly
    d = p.distance((0, 0))
    assert d == 5
    # provide list
    d2 = p.distance([3, 0])
    assert float(N(d2)) == pytest.approx(4.0)

def test_distance_higher_dimension():
    # Points in 3D
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 3)
    # difference only in first two coords: sqrt((3)^2 + (4)^2) = 5
    assert p1.distance(p2) == 5

def test_distance_mismatched_dimension_raises():
    p2d = Point(1, 2)
    p3d = Point(1, 2, 3)
    # When providing a Point of different dimension, zip will truncate; ensure behavior:
    # distance should compute over min dimension; check that it's not equal to full 3D distance.
    # For p2d.distance(p3d) only first two coordinates considered: (0,0) -> distance 0
    assert p2d.distance(p3d) == 0
    # But p3d.distance(p2d) also only uses first two coords, so result should be 0 as well here
    assert p3d.distance(p2d) == 0

def test_distance_with_symbolic_and_numeric_mixture():
    x = symbols('x')
    p = Point(x, 4)
    q = Point(3, 0)
    d = p.distance(q)
    # sqrt((x-3)**2 + (4-0)**2)
    assert d == sqrt((x - 3)**2 + 16)

def test_distance_non_point_iterable_length_mismatch():
    # If an iterable with fewer coordinates is provided, zip truncates;
    # verify behavior explicitly.
    p = Point(5, 12)
    # provide only x coordinate; distance computed using only x difference: |5-2| = 3 -> sqrt(9)=3
    d = p.distance([2])
    assert d == 3

def test_distance_dtype_preservation():
    # ensure Float coordinates yield Float-ish results
    p = Point(SymFloat(0.1), SymFloat(0.2))
    q = Point(SymFloat(0.4), SymFloat(0.6))
    d = p.distance(q)
    # numeric evaluation should match expected
    assert float(N(d)) == pytest.approx(((0.3**2 + 0.4**2) ** 0.5))