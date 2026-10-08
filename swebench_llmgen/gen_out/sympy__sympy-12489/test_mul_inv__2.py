import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.permutations import _af_new, _af_rmul, _af_invert

def af_from_list(lst):
    # helper to create a Permutation from array form using internal helper
    return _af_new(list(lst))

def test_mul_inv_identity():
    # identity permutation of size 5
    p = Permutation(list(range(5)))
    q = Permutation(list(range(5)))
    # q * ~p == q since p is identity
    res = p.mul_inv(q)
    assert isinstance(res, Permutation)
    assert res.array_form == q.array_form

def test_mul_inv_basic():
    # p = (0 1 2) in array form means p maps 0->1,1->2,2->0, rest fixed
    p = af_from_list([1,2,0,3])
    # other = (0 2) swap 0 and 2
    other = af_from_list([2,1,0,3])
    # compute other * ~p manually using array forms and the helpers to ensure consistency
    # use the internal functions to compute expected
    a = _af_invert(p._array_form)
    b = other._array_form
    expected_af = _af_rmul(a, b)
    expected = _af_new(expected_af)
    result = p.mul_inv(other)
    assert result.array_form == expected.array_form

def test_mul_inv_self_inverse():
    # p is an involution: swap 0 and 1
    p = af_from_list([1,0,2])
    # other arbitrary
    other = af_from_list([2,0,1])
    # since p == p^{-1}, mul_inv should equal p.mul_inv(other) = other * p^{-1} = other * p
    res1 = p.mul_inv(other)
    # compute other * p using normal multiplication
    res2 = other * p
    assert res1.array_form == res2.array_form

def test_mul_inv_size_mismatch_raises():
    # p of size 3, other of size 4 -> operations still operate on internal array forms,
    # ensure that behavior is consistent (may pad/truncate). Here we assert it does not raise.
    p = af_from_list([1,2,0])
    other = af_from_list([1,0,2,3])
    # Should not raise
    res = p.mul_inv(other)
    assert isinstance(res, Permutation)

def test_mul_inv_commutation_property():
    # Check that (other * ~p) * p == other when sizes align
    p = af_from_list([1,2,0])
    other = af_from_list([2,0,1])
    mid = p.mul_inv(other)
    final = mid * p
    # final should equal other
    assert final.array_form == other.array_form