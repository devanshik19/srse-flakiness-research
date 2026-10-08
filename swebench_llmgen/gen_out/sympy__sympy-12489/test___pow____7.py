import pytest
from sympy.combinatorics.permutations import Permutation, Perm

def test_pow_positive_exponent_identity():
    # identity permutation to any power should be identity
    p = Permutation(list(range(5)))
    res = p ** 3
    assert isinstance(res, Permutation)
    assert res.array_form == list(range(5))
    # zero power -> identity
    res0 = p ** 0
    assert res0.array_form == list(range(5))

def test_pow_zero_and_one():
    p = Permutation([2, 0, 1, 4, 3])  # a permutation with cycles (0 2 1)(3 4)
    # power 1 returns same permutation
    assert (p ** 1).array_form == p.array_form
    # power 0 returns identity of same size
    idt = p ** 0
    assert idt.array_form == list(range(p.size))

def test_pow_multiple_and_negative_exponent():
    # construct a 4-cycle: (0 1 2 3)
    p = Permutation([1,2,3,0])
    # p^2 should be (0 2)(1 3)
    expected_p2 = Permutation([2,3,0,1])
    assert (p ** 2).array_form == expected_p2.array_form
    # p^4 should be identity
    assert (p ** 4).array_form == list(range(4))
    # negative exponent: p^-1 is inverse
    pinv = Permutation([3,0,1,2])  # inverse of p
    assert (p ** -1).array_form == pinv.array_form
    # p^-2 equals (p^2)^-1 which for this permutation equals p^2 because order 4
    assert (p ** -2).array_form == (p ** 2).array_form

def test_pow_large_exponent_reduces_mod_order():
    # permutation order 3: (0 1 2)
    p = Permutation([1,2,0])
    # exponent larger than order; should reduce modulo order
    assert (p ** 10).array_form == (p ** (10 % 3)).array_form
    assert (p ** 10).array_form == (p ** 1).array_form

def test_pow_typeerror_for_Perm_instance():
    # If a Perm instance is passed, __pow__ raises NotImplementedError as implemented
    p = Permutation([1,0])
    with pytest.raises(NotImplementedError):
        _ = p ** Perm(1)

def test_pow_with_nonint_castable():
    # Test that floats or objects castable to int are accepted (int(n) used)
    p = Permutation([1,0,2])
    assert (p ** 2.0).array_form == (p ** 2).array_form
    class ILikeInt:
        def __int__(self):
            return 3
    # (p)**3 should work
    assert (p ** ILikeInt()).array_form == (p ** 3).array_form