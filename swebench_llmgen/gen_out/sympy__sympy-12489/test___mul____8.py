import pytest
from sympy.combinatorics.permutations import Permutation, _af_new

def test_mul_basic():
    # simple permutations as lists
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # product a*b: b(a(i))
    prod = a * b
    assert isinstance(prod, Permutation)
    assert list(prod) == [2, 0, 1]
    # check elementwise definition
    assert [b(a(i)) for i in range(3)] == list(prod)

def test_mul_different_lengths_left_shorter():
    # left shorter than right: [1,0] * [0,2,1] coerced on left
    left = Permutation([1, 0])
    right = Permutation([0, 2, 1])
    prod = left * right
    # left padded to length 3 identity at index 2, then apply right(left(i))
    assert list(prod) == [2, 0, 1]

def test_mul_different_lengths_right_shorter():
    # right shorter than left: [0,2,1] * [1,0]
    left = Permutation([0, 2, 1])
    right = Permutation([1, 0])
    prod = left * right
    # Implementation extends right to match left, then perm = [b[i] for i in a] + b[len(a):]
    # Compute expected: extend right to [1,0,2], then perm = [right[i] for i in left] + []
    assert list(prod) == [1, 2, 0]

def test_mul_with_empty_right():
    # if other.array_form is empty, returns self.array_form
    a = Permutation([2, 0, 1])
    # create a Permutation with empty array_form via _af_new([])
    empty = _af_new([])
    prod = a * empty
    assert list(prod) == list(a)

def test_mul_with_empty_left_behavior_via_rmul_conversion():
    # ensure __mul__ assumes other is Permutation and uses other's array_form.
    # Simulate coercion: calling __rmul__ on left list is handled elsewhere,
    # but we can emulate by creating a Permutation from a list on the left.
    a = Permutation([1, 0, 2])
    # left operand as permutation constructed from a list that is effectively identity on first 2
    left_list_perm = Permutation([0, 1])
    prod = left_list_perm * a
    # Per docstring example: [0,1]*a -> Permutation([1,0,2])
    assert list(prod) == [1, 0, 2]

def test_mul_commutation_not_equal():
    # multiplication is not commutative in general
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    assert list(a * b) != list(b * a)

def test_mul_idempotent_identity():
    # multiplying by identity of appropriate size should return other permutation
    p = Permutation([2, 0, 1])
    id3 = Permutation(list(range(3)))
    assert list(p * id3) == list(id3[p[i]] for i in range(3)) or list(p * id3) == list(p)

def test_mul_returns_new_object():
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    prod = a * b
    # Ensure a and b remain unchanged
    assert list(a) == [1, 0, 2]
    assert list(b) == [0, 2, 1]
    # Ensure product is not the same object as a or b
    assert prod is not a and prod is not b

def test_mul_internal_extension_logic():
    # test internal branch where b is shorter than a, so b.extend is triggered
    a = Permutation([3, 0, 1, 2])
    # b shorter
    b = Permutation([1, 0])
    res = a * b
    # Manually compute expected:
    # b extended to [1,0,2,3]; perm = [b[i] for i in a] + b[len(a):] -> no tail since len(b)==len(a)
    expected = [1, 3, 0, 2]
    assert list(res) == expected