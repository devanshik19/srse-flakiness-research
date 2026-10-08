import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_positive_and_identity():
    # permutation p = [2,0,3,1] has order 4
    p = Permutation([2, 0, 3, 1])
    assert p.order() == 4
    # p**4 should be the identity of same size
    id4 = p**4
    assert isinstance(id4, Permutation)
    assert id4.array_form == [0, 1, 2, 3]
    # powering by 0 gives identity
    assert p**0 == Permutation(list(range(p.size())))
    # powering by 1 returns same permutation
    assert p**1 == p

def test_pow_negative_and_large():
    # create a 3-cycle (0 1 2)
    q = Permutation([1, 2, 0])
    assert q.order() == 3
    # q**2 is q squared (cycle squared)
    q2 = q**2
    assert q2.array_form == [2, 0, 1]
    # q**-1 should equal q**2 because order is 3
    q_inv = q**-1
    assert q_inv.array_form == q2.array_form
    # big exponent reduces modulo order
    q_big = q**(2 + 3 * 10)  # equivalent to q**2
    assert q_big.array_form == q2.array_form

def test_pow_using_internal_af_helpers():
    # ensure that __pow__ uses array-form helpers consistently
    r = Permutation([3, 0, 1, 2])  # a 4-cycle (0 3 2 1) depending on form
    # compare results from public __pow__ and direct helpers
    for n in range(-6, 7):
        from_public = r**n
        # compute using helpers directly to confirm parity
        arr_powered = _af_pow(r.array_form, int(n))
        from_helper = _af_new(arr_powered)
        assert from_public.array_form == from_helper.array_form

def test_pow_typeerror_on_Perm():
    # Perm is an internal type used for permutation powers in sympy;
    # passing an instance of Perm should raise the NotImplementedError per code.
    p = Permutation([0, 1, 2])
    # create a Perm-like object; using Perm from module to trigger branch
    with pytest.raises(NotImplementedError):
        _ = p.__pow__(Perm(1))  # directly call to avoid int conversion path

def test_pow_preserves_size():
    # ensure powers keep permutation size (array_form length)
    s = Permutation([2, 3, 0, 1, 4])  # includes a fixed point 4
    for n in [0, 1, 2, 5, -3, 10]:
        res = s**n
        assert isinstance(res, Permutation)
        assert len(res.array_form) == s.size()