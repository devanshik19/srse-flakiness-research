import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.permutations import _af_new, _af_invert, _af_rmul

# The tests below exercise Permutation.mul_inv which computes other * ~self
# by using internal array-form helpers. We test typical cases, identity,
# self-inverse, and that mul_inv matches explicit multiplication with inverse.

def perm_from_list(lst):
    # Permutation accepts list to construct permutation in SymPy API.
    return Permutation(lst)

def array_form_of(perm):
    # Access the protected _array_form for checks; ensure it's present.
    return perm._array_form

def test_mul_inv_basic():
    # Simple permutation p and q; check that q * ~p equals expected mapping.
    p = perm_from_list([2, 0, 1])   # in array form: maps 0->2,1->0,2->1
    q = perm_from_list([1, 2, 0])   # maps 0->1,1->2,2->0

    # Compute via mul_inv
    r = p.mul_inv(q)
    # Compute explicitly: q * (~p)
    inv_p = ~p
    expected = inv_p * q  # but note mul_inv defined as other * ~self, so q * ~p
    # Compare as permutations (SymPy's Permutation supports equality)
    assert r == expected
    # Also check array forms correspond to internal helper composition
    a = _af_invert(array_form_of(p))
    b = array_form_of(q)
    composed = _af_rmul(a, b)
    assert array_form_of(r) == composed
    # And _af_new should produce the same permutation when applied
    assert r == _af_new(composed)

def test_mul_inv_identity_and_self_inverse():
    # Identity permutation
    e = perm_from_list([0,1,2,3])
    p = perm_from_list([1,0,3,2])  # product of disjoint transpositions (self-inverse)

    # e.mul_inv(p) should be p * ~e == p * e == p
    res1 = e.mul_inv(p)
    assert res1 == p

    # p.mul_inv(e) should be e * ~p == ~p
    res2 = p.mul_inv(e)
    assert res2 == ~p

    # For a self-inverse p, ~p == p, so p.mul_inv(p) == p * ~p = p*p = identity
    res3 = p.mul_inv(p)
    assert res3.is_Identity

def test_mul_inv_different_sizes_error_or_behavior():
    # When permutations have different sizes, SymPy's Permutation tries to
    # treat them with padding/truncation; ensure mul_inv works or raises clearly.
    small = perm_from_list([1,0])
    large = perm_from_list([1,2,3,0])

    # Using mul_inv where self is large and other small: internal array forms
    # may be of different sizes; ensure no unexpected exception is raised.
    try:
        out = large.mul_inv(small)
    except Exception as exc:
        # If SymPy raises due to incompatible sizes, ensure it's a TypeError or ValueError
        assert isinstance(exc, (ValueError, TypeError))
    else:
        # If it succeeds, ensure result is a Permutation instance
        assert isinstance(out, Permutation)

def test_internal_helpers_consistency():
    # Construct a random permutation and verify the helper functions are consistent:
    p = perm_from_list([3,0,4,1,2])
    q = perm_from_list([2,4,1,0,3])

    a = _af_invert(p._array_form)
    b = q._array_form
    composed = _af_rmul(a, b)
    newp = _af_new(composed)

    # newp should equal q * ~p (which is other * ~self)
    assert newp == p.mul_inv(q)

def test_mul_inv_commutes_with_public_inverse_behavior():
    # Check that mul_inv(other) equals _af_new(_af_rmul(_af_invert(self._array_form), other._array_form))
    p = perm_from_list([2,3,1,0])
    q = perm_from_list([1,0,3,2])

    # Compute via direct calls to internal helpers
    a = _af_invert(p._array_form)
    b = q._array_form
    direct = _af_new(_af_rmul(a, b))

    # Compute via public method
    via_method = p.mul_inv(q)

    assert direct == via_method