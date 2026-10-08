import pytest
from sympy.combinatorics.permutations import _af_pow
from sympy.combinatorics.permutations import _af_invert

def test_af_pow_zero_length():
    # empty permutation
    a = []
    assert _af_pow(a, 0) == []  # identity on empty set

    # single element
    a = [0]
    assert _af_pow(a, 0) == [0]
    assert _af_pow(a, 1) == [0]
    assert _af_pow(a, 2) == [0]
    assert _af_pow(a, -3) == [0]  # negative power uses invert but stays same

def test_af_pow_small_powers():
    # permutation of 4 elements: cycle structure (0 2 3 1) meaning mapping:
    # 0->2,1->0,2->3,3->1
    a = [2, 0, 3, 1]
    # n == 0 -> identity
    assert _af_pow(a, 0) == [0,1,2,3]
    # n == 1 -> same
    assert _af_pow(a, 1) == a[:]
    # n == 2 -> apply twice
    expected2 = [a[i] for i in a]
    assert _af_pow(a, 2) == expected2
    # n == 3 -> apply thrice
    expected3 = [a[a[i]] for i in a]
    assert _af_pow(a, 3) == expected3
    # n == 4 -> should be identity for a 4-cycle
    assert _af_pow(a, 4) == [0,1,2,3]

def test_af_pow_negative_and_large():
    a = [2, 0, 3, 1]
    # negative power: _af_invert should be used
    inv = _af_invert(a)
    # ensure invert works as expected
    assert [inv[inv[i]] for i in range(len(a))] == a  # inv^2 = a for this permutation
    # negative exponent equivalent to positive via invert
    assert _af_pow(a, -1) == _af_pow(inv, 1)
    assert _af_pow(a, -4) == _af_pow(inv, 4)

    # larger power uses binary multiplication loop paths:
    # choose n that will cause the %4 and %2 branches to be used
    a2 = [1,2,3,0,5,4]  # contains a 4-cycle (0-1-2-3) and a 2-cycle (4-5)
    # compute power by repeated application for correctness
    def apply_power(arr, n):
        res = list(range(len(arr)))
        for _ in range(n):
            res = [res[i] for i in arr]
        return res

    for n in [5, 6, 7, 8, 9, 10, 16, 20, 23]:
        assert _af_pow(a2, n) == apply_power(a2, n)

def test_af_pow_identity_cases_and_types():
    # identity permutation remains identity for any power
    id4 = [0,1,2,3]
    for n in [-5, -1, 0, 1, 2, 10]:
        assert _af_pow(id4, n) == id4

    # ensure original array is not modified
    a = [2,0,3,1]
    a_copy = a[:]
    _ = _af_pow(a, 5)
    assert a == a_copy

def test_af_pow_invalid_behaviour():
    # non-integer n should raise TypeError when used in bit operations
    a = [0,1,2]
    with pytest.raises(TypeError):
        _af_pow(a, 2.5)