import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_identity_and_order():
    # identity permutation power yields identity
    p = Permutation([0,1,2,3])
    assert (p**0).array_form == [0,1,2,3]
    assert (p**1).array_form == [0,1,2,3]
    assert (p**5).array_form == [0,1,2,3]

    # nontrivial permutation with order 4
    q = Permutation([2,0,3,1])  # cycles: (0 2 3 1) order 4
    assert q.order() == 4
    # raising to powers modulo order
    assert (q**0).array_form == [0,1,2,3]
    assert (q**1).array_form == [2,0,3,1]
    assert (q**2).array_form == [3,2,1,0]  # check expected mapping
    assert (q**3).array_form == [1,3,0,2]
    # 4 should return identity
    assert (q**4).array_form == [0,1,2,3]
    # larger power reduces mod order
    assert (q**8).array_form == [0,1,2,3]
    assert (q**9).array_form == (q**1).array_form

def test_pow_negative_and_large():
    # negative powers should use Python int conversion and produce inverse behaviour
    p = Permutation([1,2,0,4,3])  # cycles: (0 1 2) (3 4)
    inv = p**-1
    # multiply p and its inverse gives identity
    assert (p * inv).array_form == [0,1,2,3,4]
    assert (inv * p).array_form == [0,1,2,3,4]

    # large negative exponent equivalence: p**-4 == p**(-4 mod order)
    ord_p = p.order()
    assert (p**(-4)).array_form == (p**(-4 % ord_p)).array_form

def test_pow_uses_int_conversion_and_typeerror_for_Perm():
    p = Permutation([1,0])  # simple transposition

    class DummyIntLike:
        def __int__(self):
            return 3

    # object convertible to int should work
    nlike = DummyIntLike()
    res = p ** nlike
    assert res.array_form == (p**3).array_form

    # If argument is of type sympy.combinatorics.permutations.Perm, NotImplementedError
    # The focal code checks "if type(n) == Perm:"
    # Ensure passing an instance of Perm raises the NotImplementedError
    with pytest.raises(NotImplementedError):
        _ = p ** Perm(1)  # Perm is imported; constructing a Perm instance triggers the branch

def test_af_pow_independence_and__af_new_integration():
    # Directly test that __pow__ delegates to _af_pow and _af_new by comparing results
    base = [2,0,1]  # permutation in array form
    # pow via helper functions
    for e in [0,1,2,3,5]:
        expected = _af_new(_af_pow(base, e)).array_form
        perm = Permutation(base)
        result = (perm ** e).array_form
        assert result == expected

def test_pow_with_zero_length_and_singleton():
    # zero-length permutation doesn't exist in Permutation constructor typically,
    # but a permutation of size 1 should behave correctly
    p1 = Permutation([0])
    assert (p1**0).array_form == [0]
    assert (p1**10).array_form == [0]
    assert (p1**-3).array_form == [0]