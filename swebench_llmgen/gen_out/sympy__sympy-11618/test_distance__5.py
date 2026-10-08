import pytest
from sympy import symbols, sqrt, S, Float
from sympy.geometry.point import Point

def test_distance_numeric_2d():
    p1 = Point(1, 1)
    p2 = Point(4, 5)
    # 3-4-5 right triangle -> distance 5
    assert p1.distance(p2) == 5
    # symmetry
    assert p2.distance(p1) == 5
    # distance to self is zero
    assert p1.distance(p1) == 0

def test_distance_numeric_3d():
    p1 = Point(0, 0, 0)
    p2 = Point(1, 2, 2)
    # sqrt(1 + 4 + 4) = sqrt(9) = 3
    assert p1.distance(p2) == 3
    assert p2.distance(p1) == 3

def test_distance_with_iterable_argument():
    p = Point(2, -1)
    # passing a tuple should be accepted by the implementation
    assert p.distance((2, -1)) == 0
    # different point as iterable
    assert p.distance([5, 3]) == sqrt((2 - 5)**2 + (-1 - 3)**2)

def test_distance_symbolic():
    x, y = symbols('x y')
    p = Point(x, y)
    origin = Point(0, 0)
    # symbolic distance remains as sqrt(x**2 + y**2)
    expr = p.distance(origin)
    assert expr == sqrt(x**2 + y**2)
    # symbolic with one numeric coordinate
    p2 = Point(x, 3)
    res = p2.distance(Point(0, 0))
    assert res == sqrt(x**2 + 9)

def test_distance_mixed_float_and_int():
    p1 = Point(0, 0)
    p2 = Point(Float(0.0), 3)
    # ensure floats propagate correctly
    d = p1.distance(p2)
    assert isinstance(d, Float) or d == 3
    assert float(d) == 3.0

def test_distance_wrong_dimension_or_type():
    p = Point(1, 2)
    # if iterable of different length, zip will truncate; test that behavior:
    # distance between (1,2) and (1,) -> sqrt((1-1)**2 + (2-? missing)**2) -> only first coord used -> 0
    assert p.distance((1,)) == 0
    # but passing a non-Point non-iterable should raise TypeError when trying to iterate
    with pytest.raises(TypeError):
        _ = p.distance(5)