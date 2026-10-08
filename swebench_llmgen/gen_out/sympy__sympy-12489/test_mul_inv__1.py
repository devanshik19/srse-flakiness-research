import pytest
from sympy.combinatorics.permutations import Permutation

def test_mul_inv_basic():
    # Test that mul_inv computes other * ~self
    # We'll construct permutations via list() which gives array_form in SymPy
    # Permutation accepts sequence to create permutation
    p = Permutation(2, 0, 1)   # cycle (0 2 1)
    q = Permutation(1, 2, 0)   # cycle (0 1 2)
    # ~p is inverse of p
    inv_p = ~p
    # mul_inv should return other * ~self
    res = p.mul_inv(q)
    expected = q * inv_p
    assert isinstance(res, Permutation)
    assert res == expected
    # also verify array forms match
    assert res.array_form == expected.array_form

def test_mul_inv_identity_and_self():
    # Identity permutation test: mul_inv with identity should give other * ~self
    id_perm = Permutation(list(range(4)))  # identity of size 4
    p = Permutation(1, 0, 3, 2)  # product of two transpositions
    # id * ~p = ~p
    res = p.mul_inv(id_perm)
    assert res == id_perm * ~p
    assert res == ~p

    # other equals self
    other = p
    res2 = p.mul_inv(other)
    assert res2 == other * ~p

def test_mul_inv_different_sizes_raises_or_handles():
    # If permutations of different sizes are used, SymPy may raise or try to adapt.
    # We'll check behavior: create two permutations of different sizes and ensure no crash.
    p = Permutation(0, 1, 2)       # size 3
    q = Permutation(0, 1, 2, 3)    # size 4
    # Depending on implementation, mul_inv may produce a permutation object or raise ValueError.
    try:
        res = p.mul_inv(q)
    except ValueError:
        pytest.skip("Different-size permutations raise ValueError in this SymPy build")
    else:
        # If it returns a permutation, ensure result equals q * ~p (using Python operator)
        assert res == q * ~p

def test_mul_inv_corner_cases():
    # Test with single-element (singleton) permutation
    p = Permutation(0)
    q = Permutation(0)
    res = p.mul_inv(q)
    assert res == q * ~p
    # Test with larger random permutation consistency: mul_inv vs explicit computation
    import random
    size = 6
    base = list(range(size))
    a_list = base[:]
    random.shuffle(a_list)
    b_list = base[:]
    random.shuffle(b_list)
    p = Permutation(*a_list)
    q = Permutation(*b_list)
    res = p.mul_inv(q)
    assert res == q * ~p