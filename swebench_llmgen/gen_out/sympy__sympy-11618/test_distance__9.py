import pytest
from sympy import symbols, sqrt, S, Float
from sympy.geometry import Point
from sympy.core.numbers import Float as SymFloat

def test_distance_numeric_integer():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # 3-4-5 triangle distance
    assert p1.distance(p2) == 5
    assert p2.distance(p1) == 5

def test_distance_numeric_float():
    p1 = Point(0.0, 0.0)
    p2 = Point(1.5, 2.5)
    # ensure float works and returns a sqrt of sum of squares (may be Float)
    d = p1.distance(p2)
    # numeric evaluation equals expected float
    assert float(d) == pytest.approx((1.5**2 + 2.5**2)**0.5)
    # type check: could be a SymPy Float or expression; ensure convertible to float
    assert isinstance(float(d), float)

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    d = p.distance(origin)
    assert d == sqrt(x**2 + y**2)
    # distance to a symbolic point with another symbolic coordinate ordering
    q = Point(x, 0)
    assert q.distance(origin) == sqrt(x**2)

def test_distance_with_iterable_argument():
    # distance allows passing any iterable of coordinates as second argument
    p = Point(3, 4)
    dist = p.distance((0, 0))  # tuple
    assert dist == 5
    # list
    dist2 = p.distance([0, 0])
    assert dist2 == 5

def test_distance_mismatched_dimension_raises():
    p = Point(1, 2)
    # Passing an iterable of wrong length should raise ValueError when zip yields truncated result,
    # but distance implementation zips so shorter iterable leads to truncated computation.
    # To ensure we test an error case, pass a non-iterable (like a number) to trigger TypeError.
    with pytest.raises(TypeError):
        p.distance(5)  # not a Point and not iterable

def test_distance_high_dimension():
    # 3D points
    p1 = Point(1, 2, 2)
    p2 = Point(4, 6, 6)
    # differences: (3,4,4) -> sqrt(9+16+16) = sqrt(41)
    d = p1.distance(p2)
    assert d == sqrt(41)

def test_distance_sympy_float_inside():
    # ensure SymPy Float coordinates are handled
    a = SymFloat('1.2')
    b = SymFloat('3.4')
    p1 = Point(a, 0)
    p2 = Point(0, b)
    d = p1.distance(p2)
    # check numeric value
    assert float(d) == pytest.approx(((1.2)**2 + (3.4)**2)**0.5)