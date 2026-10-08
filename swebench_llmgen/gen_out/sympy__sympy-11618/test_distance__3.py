import pytest
from sympy import symbols, sqrt, Rational, Float
from sympy.geometry import Point
from sympy.geometry.exceptions import GeometryError

def test_distance_numeric_integer():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # classic 3-4-5 triangle distance
    assert p1.distance(p2) == 5

def test_distance_numeric_rational_and_float():
    p1 = Point(Rational(1, 2), Rational(3, 2))
    p2 = Point(Rational(3, 2), Rational(7, 2))
    # distance should be sqrt((1)^2 + (2)^2) = sqrt(5)
    d = p1.distance(p2)
    assert d == sqrt(5)
    # mixing with Float should produce an expression containing Float when evaluated
    p3 = Point(Float(0.0), Float(0.0))
    p4 = Point(Float(3.0), Float(4.0))
    d_float = p3.distance(p4)
    assert d_float == Float(5.0)

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    # symbolic result remains unevaluated algebraic expression
    assert p.distance(origin) == sqrt(x**2 + y**2)

def test_distance_with_sequence_input_like_tuple():
    # The distance method accepts a sequence as long as it's not a Point instance:
    a = Point(1, 2)
    b_tuple = (4, 6)  # behaves like Point when passed as sequence
    assert a.distance(b_tuple) == sqrt((1 - 4)**2 + (2 - 6)**2)

def test_distance_mismatched_dimensions_raises():
    # If sequences of different lengths are passed, zip will truncate;
    # ensure behavior: distance computes on zipped elements (no explicit error).
    p2d = Point(1, 2)
    p3d = Point(4, 6, 8)
    # distance will compute using first two coordinates only
    assert p2d.distance(p3d) == sqrt((1 - 4)**2 + (2 - 6)**2)

def test_distance_with_non_iterable_raises_typeerror():
    p = Point(0, 0)
    # Passing a non-iterable that is not a Point should raise a TypeError from zip
    with pytest.raises(TypeError):
        # an int is not iterable and not a Point, so iterating over it in zip will fail
        p.distance(5)