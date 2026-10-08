import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_basic_and_identity():
    # permutation p: 0->2,1->0,2->3,3->1 (array form [2,0,3,1])
    p = Permutation([2,0,3,1])
    # p has order 4 as in docstring example
    assert p.order() == 4
    # p**4 should be identity of same size
    identity = p**4
    assert isinstance(identity, Permutation)
    assert identity.array_form == list(range(p.size))
    # p**0 is identity
    assert (p**0).array_form == list(range(p.size))
    # p**1 is p itself
    assert (p**1).array_form == p.array_form
    # p**2 is p composed with itself
    p2 = p**2
    # verify by applying permutation twice
    applied_twice = [p.array_form[p.array_form[i]] for i in range(p.size)]
    assert p2.array_form == applied_twice

def test_pow_negative_exponent():
    p = Permutation([2,0,3,1])
    # negative exponent should compute inverse power
    inv = ~p  # inverse
    assert (p**-1).array_form == inv.array_form
    # p**-2 equals (p**2)**-1
    assert (p**-2).array_form == (~(p**2)).array_form

def test_pow_large_exponent_reduces_mod_order():
    # a 3-cycle
    q = Permutation([1,2,0])
    assert q.order() == 3
    # q**(3*k + r) == q**r
    for k in range(0,5):
        for r in range(0,3):
            assert (q**(3*k + r)).array_form == (q**r).array_form

def test_pow_with_zero_length_permutation():
    # permutation of size 0 (empty)
    e = Permutation([])
    # power of empty should be empty
    assert (e**5).array_form == []
    assert (e**0).array_form == []

def test_pow_rejects_perm_power():
    p = Permutation([1,0])
    # The method checks for type(n) == Perm and raises NotImplementedError
    # Construct a Perm instance (internal type) and ensure raising
    # Perm is imported from the module; create a dummy Perm value.
    dummy = Perm(2) if hasattr(Perm, '__call__') else Permutation([0,1])  # fallback
    with pytest.raises(NotImplementedError):
        _ = p.__pow__(dummy)

def test_underlying_af_helpers_consistency():
    # Directly test that _af_pow and _af_new yield same as Permutation.__pow__
    r = [3,0,1,2]  # one 4-cycle: order 4
    perm = Permutation(r)
    for n in range(-5, 6):
        # using class method
        via_pow = perm**n
        # using helpers
        arr = _af_pow(perm.array_form, int(n))
        via_helpers = _af_new(arr)
        assert via_pow.array_form == via_helpers.array_form