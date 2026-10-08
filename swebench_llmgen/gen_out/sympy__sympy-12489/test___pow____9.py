import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_identity_and_basic_cycles():
    # identity permutation to any power stays identity
    p = Permutation(list(range(5)))
    assert (p ** 0).array_form == [0,1,2,3,4]
    assert (p ** 1).array_form == [0,1,2,3,4]
    assert (p ** 10).array_form == [0,1,2,3,4]

    # 4-cycle (0 2 3 1) represented by array_form [2,0,3,1]
    p = Permutation([2,0,3,1])
    # order is 4
    assert p.order() == 4
    # p**4 should be identity
    assert (p ** 4).array_form == [0,1,2,3]
    # p**0 identity
    assert (p ** 0).array_form == [0,1,2,3]
    # p**1 equals p
    assert (p ** 1).array_form == [2,0,3,1]
    # p**2 square of permutation
    assert (p ** 2).array_form == _af_pow([2,0,3,1], 2)
    # negative powers work by repeated application (p**-1 is inverse)
    inv = p**-1
    # product of p and its inverse is identity
    assert (p*inv).array_form == [0,1,2,3]

def test_pow_with_zero_and_large_n():
    # small nontrivial permutation
    p = Permutation([1,2,0,4,3])
    # p**0 identity
    assert (p ** 0).array_form == [0,1,2,3,4]
    # large power reduces modulo order
    ord_p = p.order()
    # p**(ord_p) == identity
    assert (p ** ord_p).array_form == [0,1,2,3,4]
    # p**(ord_p + 3) equals p**3
    assert (p ** (ord_p + 3)).array_form == (p ** 3).array_form

def test_pow_typeerror_on_perm_object():
    p = Permutation([1,0])
    # When exponent is of type Perm, __pow__ should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        _ = p.__pow__(Perm([0,1]))