import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.permutations import _af_new, _af_rmul, _af_invert

def af_from_list(lst):
    # helper: create a permutation's array form directly using _af_new
    return _af_new(lst)

def test_mul_inv_basic_identity():
    # identity permutation
    p = Permutation(list(range(5)))
    q = Permutation([1, 0, 2, 3, 4])  # simple transposition on first two
    # q * ~p == q because ~p is identity
    res = q.mul_inv(p)
    assert isinstance(res, Permutation)
    assert res.array_form == q.array_form
    # also check when both nontrivial
    p2 = Permutation([2, 0, 1, 4, 3])  # cycle (0 2 1)(3 4)
    # compute expected using array-form ops: a = invert(p2), b = q.array_form
    a = _af_invert(p2._array_form)
    b = q._array_form
    expected_af = _af_rmul(a, b)
    expected = _af_new(expected_af)
    out = q.mul_inv(p2)
    assert out.array_form == expected.array_form

def test_mul_inv_inverse_behavior():
    # Check that mul_inv corresponds to other * inverse(self)
    # Pick permutations of size 6
    p = Permutation([3, 0, 5, 1, 2, 4])
    other = Permutation([1, 2, 3, 4, 5, 0])
    # Compute using provided mul_inv
    out = other.mul_inv(p)
    # Compute explicitly: inverse of p then composition with other
    inv_p = ~p
    explicit = other * inv_p
    assert out == explicit
    # Also verify associativity-like relationship:
    # (other * ~p) * p should equal other
    recomposed = (other.mul_inv(p)) * p
    assert recomposed == other

def test_mul_inv_edge_cases_singleton_and_empty():
    # size 1 permutation (singleton / identity)
    p = Permutation([0])
    other = Permutation([0])
    assert other.mul_inv(p).array_form == [0]
    # size 0 (empty) permutation: Permutation() constructs identity of size 0
    empty = Permutation(())
    # ensure methods work without raising
    out = empty.mul_inv(empty)
    assert out.array_form == []

def test_mul_inv_randomized():
    import random
    for size in (3, 4, 5):
        for _ in range(10):
            arr1 = list(range(size))
            arr2 = list(range(size))
            random.shuffle(arr1)
            random.shuffle(arr2)
            p = Permutation(arr1)
            q = Permutation(arr2)
            out = q.mul_inv(p)
            # verify by constructing inverse and composing
            invp = ~p
            expected = q * invp
            assert out == expected

def test_mul_inv_internal_af_functions_consistency():
    # directly test internal array form pathway used by mul_inv
    a = [2, 0, 1]  # permutation (0 2 1)
    b = [1, 2, 0]  # permutation (0 1 2)
    # create Permutation objects
    P = _af_new(a)
    Q = _af_new(b)
    # use mul_inv
    out = Q.mul_inv(P)
    # compute by array-form ops manually to ensure same
    inv_a = _af_invert(a)
    rmul = _af_rmul(inv_a, b)
    expected = _af_new(rmul)
    assert out.array_form == expected.array_form