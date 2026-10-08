import pytest
from sympy.combinatorics.permutations import Permutation

# Helper to build permutations from array form using Permutation._af_new via public API:
# Permutation can be constructed from list/sequence; ensure behavior matches array form.
# Tests for mul_inv: it computes other * ~self, where ~self is inverse of self.
def test_mul_inv_basic_identity():
    # identity permutation
    p = Permutation(list(range(5)))  # identity on 0..4
    q = Permutation([1, 0, 2, 4, 3])  # simple swap pairs
    # ~p is identity, so mul_inv should return other unchanged
    r = p.mul_inv(q)
    assert isinstance(r, Permutation)
    assert list(r.array_form) == list(q.array_form)

def test_mul_inv_inverse_behaviour():
    # create a nontrivial permutation and its inverse via ~
    p = Permutation([2, 0, 1, 4, 3])  # a 3-cycle on 0,2,1 and swap 3<->4
    q = Permutation([3, 4, 0, 1, 2])  # another permutation
    # compute expected = q * (~p) using public multiplication and invert
    inv_p = ~p
    expected = q * inv_p
    got = p.mul_inv(q)
    assert isinstance(got, Permutation)
    assert list(got.array_form) == list(expected.array_form)

def test_mul_inv_with_self_and_other_same():
    # Test when other is same object as self (aliasing)
    p = Permutation([1, 2, 0])  # 3-cycle
    # other and self are same object
    other = p
    res = p.mul_inv(other)
    # Should be other * ~self = p * ~p = identity
    identity = Permutation(list(range(p.size)))
    assert list(res.array_form) == list(identity.array_form)

def test_mul_inv_various_sizes():
    # test different sizes including size 1 and larger
    for arr in ([0], [1,0], [2,0,1], [3,0,2,1]):
        p = Permutation(arr)
        # choose another permutation of same size: reverse
        other_arr = list(reversed(arr))
        other = Permutation(other_arr)
        res = p.mul_inv(other)
        # verify by computing other * (~p) via public API
        expected = other * (~p)
        assert list(res.array_form) == list(expected.array_form)

def test_mul_inv_non_overlapping():
    # permutations of different internal cycle structures but same size
    p = Permutation([1,2,3,4,0])
    q = Permutation([4,3,2,1,0])
    res = p.mul_inv(q)
    expected = q * (~p)
    assert list(res.array_form) == list(expected.array_form)

# Run pytest main when executed directly (useful if someone runs this file)
if __name__ == "__main__":
    pytest.main([__file__])