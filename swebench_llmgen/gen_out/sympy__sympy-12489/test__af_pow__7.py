import pytest

# Import the focal function and the invert helper from the same module
from sympy.combinatorics.permutations import _af_pow, _af_invert

def test_af_pow_zero_power_returns_identity():
    a = [2, 0, 3, 1]
    res = _af_pow(a, 0)
    assert res == [0, 1, 2, 3]

def test_af_pow_one_returns_copy_not_same_object():
    a = [2, 0, 3, 1]
    res = _af_pow(a, 1)
    assert res == a
    assert res is not a  # should be a shallow copy

def test_af_pow_two_and_three_and_four():
    a = [2, 0, 3, 1]
    # manual compute
    two = [a[i] for i in a]
    three = [a[a[i]] for i in a]
    four = [a[a[a[i]]] for i in a]
    assert _af_pow(a, 2) == two
    assert _af_pow(a, 3) == three
    assert _af_pow(a, 4) == four

def test_af_pow_negative_uses_invert():
    a = [2, 0, 3, 1]
    inv = _af_invert(a)
    # a^(-1) should be same as applying invert once
    assert _af_pow(a, -1) == inv
    # a^(-2) equals invert squared
    assert _af_pow(a, -2) == _af_pow(inv, 2)

def test_af_pow_large_exponent_binary_multiplication():
    # use a permutation with cycle structure (0 2)(1 3 4)
    a = [2, 3, 0, 4, 1]  # mapping: 0->2,1->3,2->0,3->4,4->1
    # compute powers by repeated application for verification
    def apply_pow(arr, n):
        res = list(range(len(arr)))
        for _ in range(n):
            res = [res[i] for i in arr]
        return res

    # test several exponents including large ones, odd/even/multiples of 4
    for n in [5, 6, 7, 8, 15, 16, 63, 64]:
        assert _af_pow(a, n) == apply_pow(a, n)

def test_af_pow_identity_permutation():
    a = [0,1,2,3,4]
    # any power should be identity
    for n in [-10, -1, 0, 1, 2, 10, 100]:
        assert _af_pow(a, n) == a

def test_af_pow_singleton_permutation():
    a = [0]
    for n in range(-3, 5):
        assert _af_pow(a, n) == [0]

def test_af_pow_works_with_nontrivial_length_and_various_mods():
    # permutation: single 5-cycle
    a = [1,2,3,4,0]
    # order is 5, so powers cycle every 5
    for n in range(0, 12):
        expected = [(i + n) % 5 for i in range(5)]
        assert _af_pow(a, n) == expected
    # negative powers should correspond appropriately
    assert _af_pow(a, -1) == _af_pow(a, 4)
    assert _af_pow(a, -2) == _af_pow(a, 3)

def test_af_pow_large_n_efficiency_behavior_small_checks():
    # verify that algorithm produces correct result for a random permutation
    # (not exhaustive, just correctness for a larger size)
    a = list(range(20))
    # create a simple shuffle permutation
    a = [ (i*3 + 7) % 20 for i in range(20) ]
    # verify some random exponents including large
    for n in [0,1,2,3,4,5,20,21,40,123]:
        # compute by repeated application
        res = list(range(len(a)))
        for _ in range(n if n>=0 else -n):
            if n >= 0:
                res = [res[i] for i in a]
            else:
                res = [res[i] for i in _af_invert(a)]
        assert _af_pow(a, n) == res