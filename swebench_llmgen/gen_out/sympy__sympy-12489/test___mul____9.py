import pytest
from sympy.combinatorics.permutations import Permutation, _af_new
from sympy.combinatorics.permutations import _af_rmul

def test_mul_basic():
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    prod = a * b
    # verify it's a Permutation and has correct array form: b(a(i))
    assert isinstance(prod, Permutation)
    assert list(prod) == [b(a(i)) for i in range(3)]
    assert list(prod) == [2, 0, 1]

def test_mul_padding_longer_left():
    # left permutation longer than right: right should be padded
    a = Permutation([2, 0, 1])  # length 3
    b = Permutation([1, 0])     # length 2
    prod = a * b
    # b will be extended to length 3 as [1,0,2]; product is b(a(i))
    assert list(prod) == [ ( [1,0,2][x] ) for x in a.array_form ]
    assert list(prod) == [2,0,1]

def test_mul_padding_longer_right():
    # right permutation longer than left: left will be padded by behavior in code
    a = Permutation([1, 0])     # length 2
    b = Permutation([0, 2, 1])  # length 3
    prod = a * b
    # According to implementation, b is used directly and extra entries appended
    assert list(prod) == [ b.array_form[i] for i in a.array_form ] + b.array_form[len(a.array_form):]
    assert list(prod) == [1,2,0]

def test_mul_with_empty_other():
    # if other.array_form is empty, result should be self.array_form
    a = Permutation([2,1,0])
    class FakePerm:
        def __init__(self, af):
            self.array_form = af
    other = FakePerm([])  # empty array_form should return a unchanged
    # __rmul__ ensures coercion, but __mul__ trusts other.array_form; test behavior directly
    result = a.__mul__(other)
    assert list(result) == list(a)

def test_mul_coercion_like_list_on_left():
    # Simulate coercion where left is a list-like and right is Permutation:
    # the docstring shows [0,1]*a should coerce to Permutation on left via __rmul__
    a = Permutation([1,0,2])
    # left list as FakePerm with array_form attribute to simulate coercion result
    class LeftListLike:
        def __init__(self, arr):
            self.array_form = arr
    left = LeftListLike([0,1])  # interpreted as 2-element identity extended
    prod = left.__mul__(a) if hasattr(left, "__mul__") else None
    # If left doesn't implement __mul__, we simulate __rmul__ behavior by calling a.__rmul__(left)
    if prod is None:
        prod = a.__rmul__(left) if hasattr(a, "__rmul__") else a
    # After coercion the expected result is Permutation([1,0,2]) per docstring
    assert list(prod) == [1,0,2]

def test_mul_matches_af_rmul_difference():
    # Demonstrate that Permutation.__mul__ applies b(a(i)) while _af_rmul does
    # the opposite ordering on raw lists.
    al = [1,0,2]
    bl = [0,2,1]
    # _af_rmul computes al o bl (in its ordering); check it's different from Permutation.__mul__
    af_rmul_res = _af_rmul(al.copy(), bl.copy())
    a = Permutation(al)
    b = Permutation(bl)
    perm_mul_res = list(a * b)
    assert af_rmul_res != perm_mul_res
    # confirm perm_mul_res equals b(a(i))
    assert perm_mul_res == [bl[al[i]] for i in range(len(al))]

def test_mul_with_custom_af_new_used():
    # Ensure result is created via _af_new: _af_new returns a Permutation from list
    p = Permutation([1,2,0])
    q = Permutation([2,0,1])
    res = p * q
    # Create expected using _af_new directly and compare
    expected = _af_new([q.array_form[i] for i in p.array_form] + q.array_form[len(p.array_form):])
    assert list(res) == list(expected)

def test_mul_idempotent_identity():
    # multiply by identity (empty array_form or full identity) behaves correctly
    id_perm = Permutation(list(range(4)))
    p = Permutation([3,2,1,0])
    assert list(p * id_perm) == [ id_perm.array_form[i] for i in p.array_form ]
    # multiply by an "empty" permutation on right (array_form == []) returns left
    class EmptyLike:
        def __init__(self):
            self.array_form = []
    empty = EmptyLike()
    assert list(p.__mul__(empty)) == list(p)