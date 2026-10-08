import pytest
from sympy.combinatorics.permutations import _af_pow, _af_invert

def test_af_pow_zero_and_one():
    # identity for power 0
    a = [2, 0, 3, 1]
    res0 = _af_pow(a, 0)
    assert res0 == [0, 1, 2, 3]
    # n == 1 returns a copy, not the same object
    res1 = _af_pow(a, 1)
    assert res1 == a and res1 is not a

def test_af_pow_small_powers():
    a = [2, 0, 3, 1]  # permutation composed of two 2-cycles (0 2)(1 0?) actually example permutation
    # check n == 2,3,4 explicit behavior
    res2 = _af_pow(a, 2)
    # compute expected by composing a with itself
    expected2 = [a[i] for i in a]
    assert res2 == expected2

    res3 = _af_pow(a, 3)
    expected3 = [a[a[i]] for i in a]
    assert res3 == expected3

    res4 = _af_pow(a, 4)
    expected4 = [a[a[a[i]]] for i in a]
    assert res4 == expected4

def test_af_pow_negative_uses_invert():
    a = [2, 0, 3, 1]
    # compute inverse using provided helper and compare _af_pow with negative exponent
    inv = _af_invert(a)
    # _af_pow(a, -1) should equal inverse
    assert _af_pow(a, -1) == inv
    # check that -2 equals applying inverse twice
    assert _af_pow(a, -2) == _af_pow(inv, 2)

def test_af_pow_large_exponent_binary_multiplication():
    # Use a permutation of length 6 with a 6-cycle to ensure nontrivial binary exponentiation
    a = [1, 2, 3, 4, 5, 0]  # 6-cycle (0 1 2 3 4 5)
    # raising to 6 should give identity
    assert _af_pow(a, 6) == list(range(6))
    # raising to 7 == a
    assert _af_pow(a, 7) == a
    # test a larger exponent that exercises the loop: e.g., 25
    res25 = _af_pow(a, 25)
    # For 6-cycle, exponent mod 6 matters: 25 mod 6 = 1 => should equal a
    assert res25 == a

def test_af_pow_edge_cases():
    # empty permutation
    a = []
    assert _af_pow(a, 0) == []
    # single element permutation
    a1 = [0]
    assert _af_pow(a1, 100) == [0]
    assert _af_pow(a1, -5) == [0]

def test_af_pow_does_not_mutate_arguments():
    a = [2, 0, 3, 1]
    a_copy = list(a)
    _af_pow(a, 5)
    assert a == a_copy  # original list unchanged