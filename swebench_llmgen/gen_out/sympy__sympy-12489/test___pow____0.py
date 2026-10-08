import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_identity_and_positive_power():
    # identity permutation to any power is identity
    p_id = Permutation(list(range(5)))
    assert (p_id ** 0).array_form == p_id.array_form
    assert (p_id ** 1).array_form == p_id.array_form
    assert (p_id ** 5).array_form == p_id.array_form

    # a 4-cycle; verify powers produce expected array_forms
    p = Permutation([2, 0, 3, 1])  # cycles (0 2 3 1) maybe
    # p.order() is 4
    assert p.order() == 4
    # p**0 => identity
    assert (p ** 0).array_form == list(range(4))
    # p**1 => same
    assert (p ** 1).array_form == p.array_form
    # p**2
    expected_p2 = _af_new(_af_pow(p.array_form, 2)).array_form
    assert (p ** 2).array_form == expected_p2
    # p**4 => identity
    assert (p ** 4).array_form == list(range(4))
    # p**5 => same as p**1 (since 5 mod 4 ==1)
    assert (p ** 5).array_form == p.array_form

def test_pow_negative_and_large_exponent():
    # permutation with disjoint cycles: (0 1)(2 3 4)
    p = Permutation([1,0,3,4,2])
    # order is lcm(2,3)=6
    assert p.order() == 6
    # negative exponent should work (via pow with negative n)
    inv = p ** -1
    # inv is multiplicative inverse: p * inv == identity
    assert (p * inv).array_form == list(range(5))
    assert (inv * p).array_form == list(range(5))
    # large exponent reduces modulo order
    assert (p ** 7).array_form == (p ** 1).array_form  # 7 mod 6 ==1
    assert (p ** -5).array_form == (p ** 1).array_form  # -5 mod 6 ==1

def test_pow_with_non_integer_convertible():
    p = Permutation([2,0,1])
    # __pow__ casts n via int(n) so floats convertible to int work
    assert (p ** 2.0).array_form == (p ** 2).array_form
    # booleans convert to int as well
    assert (p ** True).array_form == (p ** 1).array_form
    assert (p ** False).array_form == (p ** 0).array_form

def test_pow_raises_on_perm_exponent():
    p = Permutation([1,0])
    # Passing a Perm instance should raise NotImplementedError according to code
    with pytest.raises(NotImplementedError):
        _ = p ** Perm()  # type: ignore

def test_pow_works_via_internal_helpers():
    # directly use internal _af_pow and _af_new to ensure compatibility
    arr = [2, 0, 1, 3]
    # power 3
    arr_pow3 = _af_new(_af_pow(arr, 3)).array_form
    p = Permutation(arr)
    assert (p ** 3).array_form == arr_pow3