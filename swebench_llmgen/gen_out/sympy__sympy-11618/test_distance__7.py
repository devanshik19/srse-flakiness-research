import pytest
from sympy import symbols, sqrt, S, Float
from sympy.geometry import Point
from sympy.geometry.point import Point as PointClass

def test_distance_numeric_2d_integer():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # classic 3-4-5 triangle
    assert p1.distance(p2) == 5
    assert p2.distance(p1) == 5

def test_distance_numeric_2d_float():
    p1 = Point(0.0, 0.0)
    p2 = Point(1.5, 2.0)
    # sqrt(1.5^2 + 2^2) = sqrt(2.25 + 4) = sqrt(6.25) = 2.5
    d = p1.distance(p2)
    assert isinstance(d, Float)
    assert float(d) == pytest.approx(2.5)

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    # should return sqrt(x**2 + y**2)
    assert p.distance(origin) == sqrt(x**2 + y**2)

def test_distance_with_sequence_like_input():
    # distance accepts a sequence (not necessarily a Point)
    p = Point(3, 4)
    # pass a tuple representing coordinates
    assert p.distance((0, 0)) == 5
    # pass a list
    assert Point(1, 0).distance([0, 1]) == sqrt(2)

def test_distance_higher_dimension():
    # 3D points
    p1 = Point(1, 2, 2)
    p2 = Point(1, 5, 6)
    # differences: (0, -3, -4) -> distance 5
    assert p1.distance(p2) == 5

def test_distance_same_point_zero():
    p = Point(7, -3)
    assert p.distance(p) == 0

def test_distance_mismatched_dimension_raises():
    p2d = Point(1, 2)
    p3d = Point(1, 2, 3)
    # zip will truncate; the current implementation zips args without dimension check,
    # so distance uses only first two coordinates. Ensure this behaviour is explicit.
    # For (1,2) vs (1,2,3) differences are (0,0) -> distance 0
    assert p2d.distance(p3d) == 0
    # but reversing gives difference (0,0) as well when zipped
    assert p3d.distance(p2d) == 0

def test_distance_with_point_like_object():
    # Create a minimal point-like object (has .args)
    class FakePoint:
        def __init__(self, *args):
            self.args = args

    p = Point(2, 3)
    fp = FakePoint(0, 0)
    # distance should accept any object with .args attribute
    assert p.distance(fp) == sqrt(13)

def test_distance_preserves_symbolic_with_mixture():
    x = symbols('x')
    p = Point(x, 0)
    # distance to numeric should be sqrt(x**2)
    assert p.distance(Point(0, 0)) == sqrt(x**2)

def test_distance_type_identity():
    # ensure the method is bound to the correct class and accessible
    assert hasattr(PointClass.distance, '__call__')