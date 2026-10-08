import pytest
from sympy.combinatorics.permutations import _af_pow
from sympy.combinatorics.permutations import _af_invert

def test_af_pow_zero_identity():
    # zero power -> identity permutation of proper length
    a = [2, 0, 3, 1]
    res = _af_pow(a, 0)
    assert res == [0, 1, 2, 3]

    # different length
    a2 = [1, 0, 2]
    assert _af_pow(a2, 0) == [0, 1, 2]

def test_af_pow_one_and_small_powers():
    a = [2, 0, 3, 1]
    # n == 1 should return a shallow copy equal to a
    r1 = _af_pow(a, 1)
    assert r1 == a and r1 is not a

    # n == 2
    r2 = _af_pow(a, 2)
    # compute expected by composing a with itself
    expected2 = [a[i] for i in a]
    assert r2 == expected2

    # n == 3
    r3 = _af_pow(a, 3)
    expected3 = [a[a[i]] for i in a]
    assert r3 == expected3

    # n == 4
    r4 = _af_pow(a, 4)
    expected4 = [a[a[a[i]]] for i in a]
    assert r4 == expected4

def test_af_pow_negative_uses_invert():
    a = [2, 0, 3, 1]
    # check that negative exponent uses invert via _af_invert
    # compute invert and then positive power
    inv = _af_invert(a)
    # (-1) should equal invert
    assert _af_pow(a, -1) == inv
    # (-2) equals invert squared
    assert _af_pow(a, -2) == _af_pow(inv, 2)

def test_af_pow_binary_multiplication_various():
    # choose a permutation with nontrivial cycles
    a = [1, 2, 0, 4, 5, 3]  # cycle structure: (0 1 2)(3 4 5)
    # test several exponents including large ones to exercise binary loop
    for n in [5, 6, 7, 8, 15, 16, 17, 64, 65]:
        # compute expected by repeated composition
        expected = list(range(len(a)))
        if n >= 0:
            for _ in range(n):
                expected = [expected[i] for i in a]
        else:
            # negative handled via invert
            expected = _af_pow(a, n)
        got = _af_pow(a[:], n)  # pass a copy to ensure _af_pow may modify local a
        assert got == expected

def test_af_pow_edge_cases_singleton_and_empty():
    # single element permutation
    a = [0]
    assert _af_pow(a, 0) == [0]
    assert _af_pow(a, 1) == [0]
    assert _af_pow(a, 10) == [0]
    assert _af_pow(a, -5) == [0]

    # empty permutation (length 0)
    a_empty = []
    assert _af_pow(a_empty, 0) == []
    # for n>0, behavior: len(a)=0 so loop constructs range(0) -> empty list
    assert _af_pow(a_empty, 3) == []
    assert _af_pow(a_empty, -1) == []

def test_af_pow_does_not_mutate_input():
    a = [2, 0, 3, 1]
    a_copy = a[:]
    _ = _af_pow(a, 10)
    assert a == a_copy  # original should be unchanged