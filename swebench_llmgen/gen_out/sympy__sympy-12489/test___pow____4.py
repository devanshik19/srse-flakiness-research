import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_positive_and_identity():
    # permutation p = (0->2,1->0,2->3,3->1) in array form [2,0,3,1]
    p = Permutation([2, 0, 3, 1])
    # order is 4, so p**4 should be identity
    assert p.order() == 4
    iden = p ** 4
    # identity array form should map i->i
    assert iden.array_form == list(range(p.size))
    # p**1 is p
    assert (p ** 1).array_form == p.array_form
    # p**0 is identity
    assert (p ** 0).array_form == list(range(p.size))
    # p**2 equals composing p with itself
    p2 = p * p
    assert (p ** 2).array_form == p2.array_form

def test_pow_negative_exponent():
    # negative exponent should use inverse powers
    p = Permutation([2, 0, 3, 1])
    inv = ~p
    # p**-1 should equal inverse
    assert (p ** -1).array_form == inv.array_form
    # p**-4 also identity
    assert (p ** -4).array_form == list(range(p.size))

def test_pow_large_exponent_reduces_mod_order():
    p = Permutation([1, 2, 0, 4, 3])  # has a 3-cycle (0 1 2) and a 2-cycle (3 4) => order lcm(3,2)=6
    assert p.order() == 6
    # exponent larger than order: 6 + 3 should be same as 3
    assert (p ** 9).array_form == (p ** 3).array_form
    # exponent negative large: -7 == -1 mod 6
    assert (p ** -7).array_form == (p ** -1).array_form

def test_pow_raises_on_Perm_type():
    # the implementation explicitly checks for Perm and raises NotImplementedError
    p = Permutation([1, 0])
    # construct a Perm instance; use Perm exported from module
    with pytest.raises(NotImplementedError):
        _ = p.__pow__(Perm(1))

def test_internal_af_pow_compatibility():
    # verify that __pow__ uses _af_pow via _af_new by checking consistency
    p = Permutation([2, 0, 3, 1])
    for n in [-5, -1, 0, 1, 2, 5]:
        res_method = (p ** n).array_form
        # compute using the internal array form functions directly
        expected = _af_new(_af_pow(p.array_form, int(n))).array_form
        assert res_method == expected