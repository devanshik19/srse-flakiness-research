import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_identity_and_order():
    # identity permutation power returns identity
    p = Permutation([0,1,2,3])
    assert (p**0).array_form == [0,1,2,3]  # 0th power treated as identity
    assert (p**1).array_form == [0,1,2,3]
    # powers preserve identity
    assert p**10 == p

    # cycle of length 4; order is 4 -> p**4 is identity
    p4 = Permutation([2,0,3,1])  # in cycle notation (0 2)(1 0?) but known to have order 4 in docstring
    assert p4.order() == 4
    idp = p4**4
    assert isinstance(idp, Permutation)
    assert idp.array_form == [0,1,2,3]

def test_pow_positive_negative_and_multiple():
    # 3-cycle
    p = Permutation([1,2,0,3])  # cycle (0 1 2)
    assert p.order() == 3
    # p**2 equals p*p
    p2 = p**2
    assert p2.array_form == [2,0,1,3]
    # p**3 is identity
    assert (p**3).array_form == [0,1,2,3]
    # negative exponent: p**-1 equals inverse (p**(order-1))
    pinv = p**-1
    assert pinv.array_form == p**2 .array_form
    assert (p**-1).array_form == [2,0,1,3]

    # exponent larger than order reduces modulo order
    assert (p**4).array_form == (p**1).array_form
    assert (p**5).array_form == (p**2).array_form

def test_pow_with_zero_length_and_singleton():
    # empty permutation (size 0)
    p_empty = Permutation([])
    assert p_empty.size == 0 or p_empty.array_form == []
    # powers should still be well-defined (empty stays empty)
    assert (p_empty**3).array_form == []
    assert (p_empty**0).array_form == []

    # singleton permutation
    p1 = Permutation([0])
    assert (p1**5).array_form == [0]
    assert (p1**0).array_form == [0]

def test_pow_uses_int_conversion_and_rejects_perm_exponent():
    p = Permutation([1,0])
    # Passing something that is not int but convertible should work
    class IntLike:
        def __int__(self):
            return 2
    r = p**IntLike()
    assert r.array_form == (p*p).array_form

    # If exponent is a Perm instance (Perm), behavior should raise NotImplementedError
    # The implementation checks type(n) == Perm
    with pytest.raises(NotImplementedError):
        _ = p.__pow__(Perm())  # directly call to trigger the specific branch

def test_internal_af_pow_compatibility():
    # Ensure that __pow__ returns same as constructing via internal helpers
    p = Permutation([2,0,1,3])  # 3-cycle on first three elements
    for n in range(-5, 6):
        # ensure int conversion matches and internal _af_pow used
        expected = _af_new(_af_pow(p.array_form, int(n)))
        got = p**n
        assert isinstance(got, Permutation)
        assert got.array_form == expected.array_form