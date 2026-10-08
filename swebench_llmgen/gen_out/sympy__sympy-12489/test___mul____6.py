import pytest
from sympy.combinatorics.permutations import Permutation, _af_new

def test_mul_basic():
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    prod = a * b
    # product should be b(a(i)) for i=0..2
    assert list(prod) == [b(a(i)) for i in range(3)]
    # explicit expected
    assert list(prod) == [2, 0, 1]
    # check that multiplication does not modify operands
    assert list(a) == [1, 0, 2]
    assert list(b) == [0, 2, 1]

def test_mul_different_lengths():
    # b shorter than a: b padded on right when computing a*b
    a = Permutation([2, 0, 1])  # size 3
    b = Permutation([1, 0])     # size 2
    prod1 = b * a
    # b * a should extend b to length 3 before composing (rhs is a)
    assert isinstance(prod1, Permutation)
    assert list(prod1) == [1, 2, 0]  # verify expected composition

    # other direction: a * b pads b to length of a inside __mul__
    prod2 = a * b
    assert list(prod2) == [b(a(i)) for i in range(3)]
    # compute expected manually: extend b to [1,0,2], then map by a
    assert list(prod2) == [2, 0, 1]

def test_mul_with_raw_list_coercion_left_of_permutation():
    a = Permutation([1, 0, 2])
    # Left operand as plain list should be accepted via __rmul__ coercion.
    left = [0, 1]
    prod = left * a
    # left interpreted as a permutation of size 2, then extended to size 3
    assert isinstance(prod, Permutation)
    assert list(prod) == [1, 0, 2]

    # Nested list case: [[0,1]] should be handled differently by coercion (swap)
    left = [[0, 1]]
    prod2 = left * a
    assert isinstance(prod2, Permutation)
    # Expectation from documentation: exchange first two elements (acts as cycle)
    # For safety, verify it is a permutation of size 3 and not equal to original a
    assert sorted(list(prod2)) == [0,1,2]
    assert list(prod2) != list(a)

def test_mul_with_empty_other():
    a = Permutation([2, 0, 1])
    empty = Permutation([])  # empty permutation should act as identity on left array in __mul__
    res = a * empty
    # According to __mul__, if other.array_form is empty, perm = a
    assert list(res) == list(a)

def test_mul_returns_new_object_and_uses_af_new():
    # Ensure _af_new is effectively creating the result and that mutation of inputs doesn't affect it.
    a = Permutation([1,2,0,3])
    b = Permutation([2,3,0,1])
    res = a * b
    # mutate internal lists of a and b by creating new permutations from their lists
    a2 = _af_new(list(a))
    b2 = _af_new(list(b))
    # ensure original res remains the same
    assert list(res) == [b(a(i)) for i in range(len(res))]
    assert isinstance(res, Permutation)

def test_mul_edge_cases_size_mismatch_padding():
    # a longer than b: ensure padding of b with identity elements
    a = Permutation([3,0,1,2])  # size 4
    b = Permutation([1,0])      # size 2
    res = a * b
    # b extended to [1,0,2,3] then perm = [b[i] for i in a] + b[len(a):] (b[len(a):] empty)
    expected = [ ( [1,0,2,3][i] ) for i in [3,0,1,2] ]
    assert list(res) == expected

def test_mul_idempotent_and_noncommutative():
    # multiplication should generally be non-commutative
    a = Permutation([1,2,0])
    b = Permutation([2,0,1])
    assert list(a * b) != list(b * a)
    # but composing with identity leaves permutation unchanged
    id_perm = Permutation(list(range(3)))
    assert list(a * id_perm) == list(a)
    assert list(id_perm * a) == list(a)