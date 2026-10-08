import pytest
from sympy import symbols, sqrt, S, Float
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
    # distance should be sqrt(1.5**2 + 2.0**2)
    expected = sqrt(1.5**2 + 2.0**2)
    # result may be a Float or sympy expression; compare numerically
    res = p1.distance(p2)
    assert float(res) == pytest.approx(float(expected))

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    d = p.distance(origin)
    # expect sqrt(x**2 + y**2)
    assert d == sqrt(x**2 + y**2)

def test_distance_mixed_symbolic_numeric():
    x = symbols('x')
    p = Point(x, 3)
    q = Point(0, 4)
    # distance is sqrt(x**2 + (3-4)**2) = sqrt(x**2 + 1)
    assert p.distance(q) == sqrt(x**2 + 1)

def test_distance_with_iterable_other_than_point():
    # The code accepts an iterable (not necessarily a Point) for p
    p = Point(1, 2)
    other = (4, 6)  # tuple
    # distance should be sqrt((1-4)^2 + (2-6)^2) = sqrt(9+16) = 5
    assert p.distance(other) == 5

def test_distance_high_dimension():
    # test 3D points
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 3)
    # distance sqrt((3)^2 + (4)^2 + 0^2) = 5
    assert p1.distance(p2) == 5

def test_distance_zero():
    p = Point(0, 0)
    assert p.distance(p) == 0

def test_distance_type_preservation_symbolic_float():
    # ensure symbolic + Float works and returns sqrt expression with Float inside if needed
    x = symbols('x')
    p = Point(x, Float(2.0))
    q = Point(0, 0)
    d = p.distance(q)
    # Should be sqrt(x**2 + 4.0)
    assert d == sqrt(x**2 + Float(4.0))

def test_distance_errors_on_mismatched_dimensions():
    p1 = Point(1, 2)
    p2 = Point(1, 2, 3)
    # zip will truncate; geometry likely expects same dimension but function will compute
    # Ensure it computes on zipped components (truncated) rather than raising
    # For (1,2) vs (1,2,3) zipped pairs are (1,1),(2,2) -> distance 0
    assert p1.distance(p2) == 0

def test_distance_with_non_iterable_raises():
    p = Point(0, 0)
    with pytest.raises(TypeError):
        # passing a non-iterable/non-Point object should raise when zip tries to iterate
        p.distance(5)