import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_identity_and_positive():
    # identity permutation to any power remains identity
    p = Permutation(list(range(5)))
    for n in [0, 1, 2, 10, -3]:
        res = p ** n
        assert isinstance(res, Permutation)
        assert res.array_form == [0,1,2,3,4]

    # a 4-cycle: (0 2 3 1) represented by array [2,0,3,1]
    p = Permutation([2,0,3,1])
    # order is 4 so p**4 is identity
    assert p.order() == 4
    r = p ** 4
    assert r.array_form == [0,1,2,3]

    # powers that wrap around: p**1 == p, p**2 should be square
    assert (p ** 1).array_form == p.array_form
    assert (p ** 2).array_form == _af_new(_af_pow(p.array_form, 2)).array_form

def test_pow_negative_and_large():
    # permutation with cycles of different lengths: (0 1)(2 3 4)
    p = Permutation([1,0,3,4,2])
    # compute some negative powers via repeated multiplication check
    inv = p ** -1
    # inv * p should be identity
    iden = (inv * p)
    assert iden.array_form == list(range(p.size))
    # large positive and negative exponents reduce modulo order
    ord_p = p.order()
    assert (p ** (ord_p + 1)).array_form == (p ** 1).array_form
    assert (p ** (-(ord_p + 1))).array_form == (p ** -1).array_form

def test_pow_with_nonint_like_raises_notimplemented_for_Perm():
    p = Permutation([1,0])
    # If exponent is of type Perm we expect NotImplementedError as per code
    with pytest.raises(NotImplementedError):
        _ = p.__pow__(Perm())