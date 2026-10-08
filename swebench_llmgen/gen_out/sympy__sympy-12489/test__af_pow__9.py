import pytest

from sympy.combinatorics.permutations import _af_pow

def test_af_pow_zero():
    # zero power should return identity of appropriate length
    a = [2, 0, 1, 4, 3]
    res = _af_pow(a, 0)
    assert res == list(range(len(a)))

def test_af_pow_one():
    a = [2, 0, 1, 4, 3]
    assert _af_pow(a, 1) == a[:]  # should return a shallow copy

def test_af_pow_two_three_four():
    a = [2, 0, 3, 1]  # a 4-cycle split into two 2-cycles
    # n==2
    expected2 = [a[i] for i in a]
    assert _af_pow(a, 2) == expected2
    # n==3
    expected3 = [a[a[i]] for i in a]
    assert _af_pow(a, 3) == expected3
    # n==4 should be identity for this permutation
    expected4 = [a[a[a[a[i]]]] for i in a] if False else list(range(len(a)))
    assert _af_pow(a, 4) == list(range(len(a)))

def test_af_pow_large_positive():
    # test binary multiplication path with various reductions
    # create a permutation of length 6
    a = [1, 2, 0, 5, 3, 4]  # two 3-cycles (0,1,2) and (3,5,4)
    # compute a^5 by repeated composition directly
    def comp(p, q):
        return [p[i] for i in q]
    # start with identity and apply a 5 times
    cur = list(range(len(a)))
    for _ in range(5):
        cur = comp(a, cur)
    assert _af_pow(a, 5) == cur
    # also check a^6 equals identity (since 3-cycles => order 3)
    assert _af_pow(a, 6) == list(range(len(a)))

def test_af_pow_negative():
    # inverse should be computed for negative powers
    a = [2, 0, 1, 4, 3]
    # compute inverse explicitly
    inv = [0]*len(a)
    for i, v in enumerate(a):
        inv[v] = i
    # a^-1 should equal inverse
    assert _af_pow(a, -1) == inv
    # a^-3 equals (a^-1)^3; compute by composition
    def comp(p, q):
        return [p[i] for i in q]
    inv3 = inv[:]
    for _ in range(2):
        inv3 = comp(inv, inv3)
    assert _af_pow(a, -3) == inv3

def test_af_pow_edge_cases_small_lengths():
    # length 0 permutation
    a0 = []
    assert _af_pow(a0, 0) == []
    # length 1 permutation
    a1 = [0]
    assert _af_pow(a1, 0) == [0]
    assert _af_pow(a1, 10) == [0]
    assert _af_pow(a1, -7) == [0]

def test_af_pow_does_not_mutate_input():
    a = [1, 0, 2]
    a_copy = a[:]
    _ = _af_pow(a, 7)
    assert a == a_copy  # original should remain unchanged