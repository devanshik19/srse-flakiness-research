import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.combinatorics.permutations import _af_new, _af_pow

def test_pow_identity_and_order():
    # identity permutation power
    p = Permutation([0, 1, 2, 3])
    # power 0 -> identity
    assert (p ** 0).array_form == [0,1,2,3]
    # power 1 -> itself
    assert (p ** 1).array_form == [0,1,2,3]
    # positive power
    assert (p ** 5).array_form == [0,1,2,3]
    # negative powers (inverse) still identity
    assert (p ** -1).array_form == [0,1,2,3]

def test_pow_cycle():
    # a 4-cycle: (0 2 3 1) in array form [2,0,3,1]
    p = Permutation([2,0,3,1])
    # order is 4
    assert p.order() == 4
    # p^1
    assert (p ** 1).array_form == [2,0,3,1]
    # p^2
    assert (p ** 2).array_form == _af_pow(p.array_form, 2)
    # p^3
    assert (p ** 3).array_form == _af_pow(p.array_form, 3)
    # p^4 -> identity
    assert (p ** 4).array_form == [0,1,2,3]
    # p^5 == p
    assert (p ** 5).array_form == p.array_form
    # negative exponent e.g., p^-1 equals inverse permutation
    inv = p.__invert__()
    assert (p ** -1).array_form == inv.array_form
    # large exponent (multiple of order) returns identity
    assert (p ** (4 * 10)).array_form == [0,1,2,3]

def test_pow_uses_int_conversion_and_raises_on_Perm_type():
    p = Permutation([1,0])
    # Provide something convertible to int (like boolean)
    assert (p ** True).array_form == (p ** 1).array_form
    # Providing a custom object convertible via int() should work
    class C:
        def __int__(self):
            return 2
    assert (p ** C()).array_form == (p ** 2).array_form
    # But providing a Perm instance should raise the NotImplementedError as in code
    # Perm is a class imported from the module; constructing one to trigger the branch
    perm_obj = Perm()
    with pytest.raises(NotImplementedError):
        _ = p.__pow__(perm_obj)

def test_af_pow_helper_consistency():
    # ensure _af_pow works consistently with repeated application of array form
    arr = [2,0,3,1]
    for n in range(-6, 7):
        # compare Permutation power against applying _af_pow then _af_new
        try:
            p = Permutation(arr)
            expected = _af_new(_af_pow(p.array_form, int(n)))
            assert (p ** n).array_form == expected.array_form
        except Exception as exc:
            # ensure any exception is not from int conversion for these tests
            raise

# Run tests if executed as script (useful for local runs)
if __name__ == "__main__":
    pytest.main([__file__])