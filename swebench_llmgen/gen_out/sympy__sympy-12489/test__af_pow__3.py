import pytest
from sympy.combinatorics.permutations import _af_pow
from sympy.combinatorics.permutations import _af_invert

def test_af_pow_zero_and_one():
    # zero power -> identity of appropriate length
    a = [2, 0, 3, 1]
    assert _af_pow(a, 0) == [0, 1, 2, 3]
    # one -> copy of a
    res = _af_pow(a, 1)
    assert res == a
    # ensure it's a copy, not the same object
    assert res is not a

def test_af_pow_small_positive():
    a = [2, 0, 3, 1]  # permutation of 4 with cycle structure (0 2 3 1)
    # powers 2,3,4
    assert _af_pow(a, 2) == [3, 2, 1, 0]  # compute a^2
    assert _af_pow(a, 3) == [1, 0, 3, 2]  # a^3
    assert _af_pow(a, 4) == [0, 1, 2, 3]  # a^4 == identity

def test_af_pow_negative_uses_invert():
    a = [2, 0, 3, 1]
    # check negative uses invert: a^-1 should be inverse mapping
    inv = _af_invert(a)
    # a^-1 equals pow with -1
    assert _af_pow(a, -1) == inv
    # a^-3 equals (a^-1)^3 which is equivalent to a^(order-3) for order 4
    assert _af_pow(a, -3) == _af_pow(inv, 3)

def test_af_pow_large_and_binary_multiplication_paths():
    # Construct a permutation of size 8 with several cycles to exercise binary path
    # Example permutation (0 1 2)(3 4)(5 6 7)
    a = [1, 2, 0, 4, 3, 6, 7, 5]
    # test various n to run different branches (even, divisible by 4, odd)
    # n odd -> will trigger the n&1 branch repeatedly
    assert _af_pow(a, 1) == a
    p2 = _af_pow(a, 2)
    # verify p2 is composition a after itself
    expected_p2 = [a[i] for i in a]
    assert p2 == expected_p2
    # n = 4 should use precomputed quadruple composition when possible in loop
    p4 = _af_pow(a, 4)
    expected_p4 = [a[a[a[a[i]]]] for i in range(len(a))]
    assert p4 == expected_p4
    # larger odd number to exercise mixing of operations
    p13 = _af_pow(a, 13)
    # compare by repeated application to be certain
    def pow_naive(perm, n):
        res = list(range(len(perm)))
        for _ in range(n):
            res = [res[i] for i in perm]
        return res
    assert p13 == pow_naive(a, 13)

def test_af_pow_identity_behavior():
    # identity permutation should always return identity for any power
    id4 = [0,1,2,3]
    for n in [-5, -1, 0, 1, 2, 10]:
        assert _af_pow(id4, n) == id4

def test_af_pow_nontrivial_len_one_and_two():
    # length 1 permutation
    a1 = [0]
    assert _af_pow(a1, 0) == [0]
    assert _af_pow(a1, 5) == [0]
    # length 2 swap
    a2 = [1,0]
    assert _af_pow(a2, 2) == [0,1]
    assert _af_pow(a2, 3) == [1,0]
    assert _af_pow(a2, -1) == [1,0]

def test_af_pow_invalid_types_and_edges():
    # ensure function raises appropriate errors if n is not int-like will be handled by bit ops
    a = [0,1,2]
    with pytest.raises(TypeError):
        _af_pow(a, 2.5)
    # but large integers should work (exercise loops)
    assert _af_pow(a, 100) == _af_pow(a, 100 % 1)  # identity since a is identity here