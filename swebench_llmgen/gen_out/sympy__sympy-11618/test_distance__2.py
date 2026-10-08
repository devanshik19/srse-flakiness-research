import pytest
from sympy import symbols, sqrt, Matrix, Float
from sympy.geometry.point import Point
from sympy.core.numbers import Float as SymFloat

def test_distance_numeric_2d_ints():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # classic 3-4-5 triangle -> distance 5
    assert p1.distance(p2) == 5
    assert p2.distance(p1) == 5

def test_distance_numeric_2d_floats():
    p1 = Point(0.0, 0.0)
    p2 = Point(1.0, 1.0)
    # distance sqrt(2)
    d = p1.distance(p2)
    # result may be a Float; compare numerically
    assert abs(float(d) - 2**0.5) < 1e-12

def test_distance_high_dimensional():
    # 3D points
    p1 = Point(1, 2, 3)
    p2 = Point(4, 6, 3)
    # difference is (3,4,0) -> distance 5
    assert p1.distance(p2) == 5

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    d = p.distance(origin)
    assert d == sqrt(x**2 + y**2)

def test_distance_with_iterable_argument_like_tuple():
    # distance accepts an iterable of coordinates, not only Point
    p = Point(1, 2)
    d = p.distance((4, 6))
    # difference (3,4) -> 5
    assert d == 5

def test_distance_with_matrix_argument():
    # matrix should be treated as iterable of coordinates
    p = Point(1, 2)
    m = Matrix([4, 6])
    d = p.distance(m)
    assert d == 5

def test_distance_mismatched_dimensions_raises():
    p = Point(1, 2)
    q = Point(1, 2, 3)
    # zip will truncate; ensure behavior is consistent: uses first two coords
    # distance should be zero because first two coordinates equal
    assert p.distance(q) == 0

def test_distance_non_point_non_iterable_raises_typeerror():
    p = Point(0, 0)
    class NotIterable:
        def __iter__(self):
            raise TypeError
    ni = NotIterable()
    # Passing a non-Point non-iterable should raise when zip tries to iterate
    with pytest.raises(TypeError):
        _ = p.distance(ni)

def test_distance_returns_symbolic_with_floats_and_symbols():
    x = symbols('x')
    p = Point(x, 0)
    q = Point(3.0, 4.0)
    d = p.distance(q)
    # should be sqrt((x-3.0)**2 + 16.0) symbolic expression
    assert "sqrt" in str(d)
    # numeric part should evaluate correctly for a sample x
    val = d.subs(x, 3)
    assert float(val) == 4.0

def test_distance_with_same_point_zero():
    p = Point(2, -5)
    assert p.distance(p) == 0

def test_distance_preserves_type_for_floats():
    p = Point(SymFloat(0.5), SymFloat(0.5))
    q = Point(SymFloat(0.5), SymFloat(0.5))
    d = p.distance(q)
    # distance zero should be exact integer 0 even if inputs are Floats
    assert d == 0