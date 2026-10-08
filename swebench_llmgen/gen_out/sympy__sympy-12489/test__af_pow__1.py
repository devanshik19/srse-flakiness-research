import pytest
from sympy.combinatorics.permutations import _af_pow, _af_invert

def test_af_pow_zero():
    a = [2,0,3,1]
    # n == 0 should return identity of same length
    res = _af_pow(a, 0)
    assert res == [0,1,2,3]

def test_af_pow_one_two_three_four():
    a = [2,0,3,1]
    # n == 1 returns copy
    res1 = _af_pow(a, 1)
    assert res1 == a and res1 is not a  # copy, not same object

    # n == 2 uses specific branch
    res2 = _af_pow(a, 2)
    # compute expected by applying permutation twice
    expected2 = [a[i] for i in a]
    assert res2 == expected2

    # n == 3 branch
    res3 = _af_pow(a, 3)
    expected3 = [a[a[i]] for i in a]
    assert res3 == expected3

    # n == 4 branch
    res4 = _af_pow(a, 4)
    expected4 = [a[a[a[i]]] for i in a]
    assert res4 == expected4

def test_af_pow_negative_uses_invert():
    # check negative n uses invert
    a = [2,0,3,1]
    inv = _af_invert(a)
    # _af_pow(a, -1) should equal invert
    assert _af_pow(a, -1) == inv
    # and -2 should be invert squared
    assert _af_pow(a, -2) == _af_pow(inv, 2)

def test_af_pow_large_n_binary_multiplication():
    # choose a permutation with cycle structure to exercise binary loop
    # permutation: (0 1 2 3 4) five-cycle
    a = [1,2,3,4,0]
    # power 7 should be same as power 7 mod 5 = 2
    res7 = _af_pow(a, 7)
    res2 = _af_pow(a, 2)
    assert res7 == res2

    # larger power that triggers the n%4 == 0 branch eventually
    res20 = _af_pow(a, 20)
    # 20 mod 5 == 0 so should be identity
    assert res20 == [0,1,2,3,4]

def test_af_pow_identity_perm():
    # identity permutation stays identity for any n
    a = [0,1,2,3]
    for n in [-5, -1, 0, 1, 2, 10]:
        res = _af_pow(a, n)
        assert res == [0,1,2,3]

def test_af_pow_dtype_and_length_preserved():
    # ensure returned list has same length and contains ints 0..len-1
    a = [2,0,1,4,3]
    res = _af_pow(a, 3)
    assert isinstance(res, list)
    assert len(res) == len(a)
    assert set(res) == set(range(len(a)))

def test_af_pow_nontrivial_branching():
    # create permutation to force mix of n&1, n%4 cases
    a = [2,3,0,1,6,4,5]  # cycles (0 2)(1 3)(4 6 5)
    # pick n that will go through several loop iterations
    n = 13
    res = _af_pow(a, n)
    # verify by repeated composition
    expected = list(range(len(a)))
    # apply permutation n times
    for _ in range(n):
        expected = [expected[i] for i in a]
    assert res == expected