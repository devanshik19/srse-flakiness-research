import pytest

from sympy.combinatorics.permutations import _af_pow
from sympy.combinatorics.permutations import _af_invert

def test_af_pow_zero():
    # n == 0 should return identity of appropriate length
    a = [2, 0, 3, 1]
    res = _af_pow(a, 0)
    assert res == [0, 1, 2, 3]

def test_af_pow_one():
    a = [2, 0, 3, 1]
    res = _af_pow(a, 1)
    # should return a shallow copy equal to a
    assert res == a and res is not a

def test_af_pow_two_three_four():
    a = [2, 0, 3, 1]
    # n == 2
    res2 = _af_pow(a, 2)
    # apply permutation twice: a[a[i]]
    expected2 = [a[i] for i in a]
    assert res2 == expected2

    # n == 3
    res3 = _af_pow(a, 3)
    expected3 = [a[a[i]] for i in a]
    assert res3 == expected3

    # n == 4
    res4 = _af_pow(a, 4)
    expected4 = [a[a[a[i]]] for i in a]
    assert res4 == expected4

def test_af_pow_large_positive():
    # exercise binary multiplication branch with mixed divisions by 2 and 4
    # choose permutation of length 6
    a = [1, 2, 0, 5, 3, 4]  # cycles: (0 1 2) and (3 5 4)
    # compute powers by repeated composition for comparison
    def compose(p, q):
        return [p[i] for i in q]
    # compute a^7 by repeated multiplication
    pow7 = list(range(len(a)))
    for _ in range(7):
        pow7 = compose(a, pow7)
    res7 = _af_pow(a, 7)
    assert res7 == pow7

    # also test a larger exponent that triggers multiple reductions
    res20 = _af_pow(a, 20)
    pow20 = list(range(len(a)))
    for _ in range(20):
        pow20 = compose(a, pow20)
    assert res20 == pow20

def test_af_pow_negative():
    a = [2, 0, 3, 1]
    # using _af_invert to compute negative power fallback
    # a^{-1} should be invert permutation
    inv = _af_invert(a)
    # a^{-3} == (a^{-1})^3
    res_neg3 = _af_pow(a, -3)
    expected = _af_pow(inv, 3)
    assert res_neg3 == expected

def test_af_pow_identity_behaviour():
    # identity permutation should always return identity
    a = [0,1,2,3,4]
    for n in [-5, -1, 0, 1, 2, 10]:
        res = _af_pow(a, n)
        assert res == a

def test_af_pow_edge_cases_empty_and_singleton():
    # empty permutation
    a0 = []
    assert _af_pow(a0, 0) == []
    # singleton
    a1 = [0]
    assert _af_pow(a1, 0) == [0]
    assert _af_pow(a1, 5) == [0]
    assert _af_pow(a1, -3) == [0]