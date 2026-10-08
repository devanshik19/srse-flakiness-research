import pytest
from sympy.combinatorics.permutations import _af_pow
from sympy.combinatorics.permutations import _af_invert

def test_af_pow_zero_and_one():
    # zero power returns identity of correct size
    a = [2, 0, 3, 1]
    assert _af_pow(a, 0) == [0, 1, 2, 3]
    # one returns a shallow copy equal to a
    res = _af_pow(a, 1)
    assert res == a and res is not a

def test_af_pow_small_powers():
    a = [2, 0, 3, 1]  # permutation of order 4 (two 2-cycles (0 2)(1 3)? actually order 4)
    # power 2
    p2 = _af_pow(a, 2)
    # manually compute: apply a twice
    manual_p2 = [a[i] for i in a]
    assert p2 == manual_p2
    # power 3
    p3 = _af_pow(a, 3)
    manual_p3 = [a[a[i]] for i in a]
    assert p3 == manual_p3
    # power 4 should be identity
    assert _af_pow(a, 4) == [0, 1, 2, 3]

def test_af_pow_negative_and_invert_consistency():
    # ensure negative powers use invert and match repeated application
    a = [3, 2, 1, 0, 5, 4]  # self-inverse on two 2-cycles and a 2-cycle (0 3)(1 2)(4 5)
    # compute inverse using provided helper to validate internal use
    inv = _af_invert(a)
    assert _af_pow(a, -1) == inv
    # check that a * a^-1 == identity via composition equal to _af_pow(a,0)
    composed = [a[inv[i]] for i in range(len(a))]
    assert composed == _af_pow(a, 0)

def test_af_pow_binary_multiplication_paths():
    # choose a permutation with length 7 to exercise binary multiplication loop
    a = [1, 2, 3, 4, 5, 6, 0]  # 7-cycle (0 1 2 3 4 5 6)
    # test various n to force different branches in the while loop
    # n that is odd and >4
    assert _af_pow(a, 5) == [5, 6, 0, 1, 2, 3, 4]
    # n that is even but not multiple of 4
    assert _af_pow(a, 6) == [6, 0, 1, 2, 3, 4, 5]
    # large n to exercise repeated squaring/quadrupling until zero
    assert _af_pow(a, 14) == _af_pow(a, 14 % 7)  # 7-cycle so exponent mod 7

def test_af_pow_identity_behavior_and_length_zero():
    # empty permutation
    a = []
    assert _af_pow(a, 0) == []
    # length 1 permutation
    a1 = [0]
    assert _af_pow(a1, 10) == [0]
    assert _af_pow(a1, -3) == [0]

def test_af_pow_preserves_permutation_property():
    # For a permutation, result should be a permutation (a rearrangement of range)
    a = [2, 0, 4, 1, 3]
    for n in range(-3, 10):
        res = _af_pow(a, n)
        assert sorted(res) == list(range(len(a)))

def test_af_pow_handles_large_n_efficiency():
    # ensure not blowing up for large n; correctness via modulo of cycle lengths
    a = [1, 0, 3, 4, 2]  # cycles: (0 1) and (2 3 4) -> lcm = 6
    # n large but equivalent to n % 6
    assert _af_pow(a, 1001) == _af_pow(a, 1001 % 6)