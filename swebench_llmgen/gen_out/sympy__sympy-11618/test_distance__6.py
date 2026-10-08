import pytest
from sympy import symbols, sqrt, S, Rational
from sympy.geometry import Point
from sympy.core.numbers import Float

def test_distance_numeric_ints():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # classic 3-4-5 triangle
    assert p1.distance(p2) == 5
    assert p2.distance(p1) == 5

def test_distance_numeric_floats():
    p1 = Point(0.0, 0.0)
    p2 = Point(1.5, 2.5)
    # distance = sqrt(1.5^2 + 2.5^2)
    expected = sqrt(Float('1.5')**2 + Float('2.5')**2)
    # The returned object may be a Float inside a sqrt; compare numeric approximation
    assert float(p1.distance(p2)) == float(expected)

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    expr = p.distance(origin)
    # Should be symbolic sqrt(x**2 + y**2)
    assert expr == sqrt(x**2 + y**2)

def test_distance_with_sequence_like_argument():
    # The method accepts either a Point or a sequence-like of coordinates
    p = Point(2, 3)
    # pass a tuple of coordinates
    assert p.distance((5, 7)) == sqrt((2 - 5)**2 + (3 - 7)**2)
    # pass a list of coordinates
    assert p.distance([2, 3]) == 0

def test_distance_higher_dimension():
    # 3D points
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 3)
    # difference is (3,4,0) -> length 5
    assert p1.distance(p2) == 5

def test_distance_mixed_rationals_and_ints():
    p1 = Point(Rational(1, 2), 0)
    p2 = Point(0, Rational(3, 2))
    # distance = sqrt((1/2)^2 + (3/2)^2) = sqrt(1/4 + 9/4) = sqrt(10/4) = sqrt(5/2)
    assert p1.distance(p2) == sqrt(S(5)/2)

def test_distance_invalid_argument_type():
    p = Point(0, 0)
    # passing an object that is not a Point or iterable should raise an error when zipped lengths mismatch
    class Weird:
        args = (1,)
    w = Weird()
    # Since distance tries to zip self.args with p.args if isinstance(p, Point) else p,
    # passing an object that is iterable but of wrong length will compute with zip (silently truncates).
    # To cause a clearer failure, pass a non-iterable to force a TypeError during iteration.
    with pytest.raises(TypeError):
        p.distance(123)  # integer is not iterable and not a Point

def test_distance_commutes_and_zero():
    p = Point(7, -4)
    # distance to self is zero
    assert p.distance(p) == 0
    # symmetry
    q = Point(-1, 6)
    assert p.distance(q) == q.distance(p)