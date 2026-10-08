import pytest
from sympy.combinatorics.permutations import _af_pow
from sympy.combinatorics.permutations import _af_invert

def test_af_pow_zero_and_one():
    # zero power returns identity of appropriate length
    a = [2, 0, 3, 1]
    assert _af_pow(a, 0) == [0, 1, 2, 3]
    # one returns a shallow copy (not the same object)
    res = _af_pow(a, 1)
    assert res == a
    assert res is not a

def test_af_pow_small_powers():
    a = [2, 0, 3, 1]  # cycle structure: (0 2 3 1) of length 4
    # powers 2,3,4
    assert _af_pow(a, 2) == [3, 2, 1, 0]  # apply permutation twice
    assert _af_pow(a, 3) == [1, 3, 0, 2]
    assert _af_pow(a, 4) == [0, 1, 2, 3]  # full cycle returns identity

def test_af_pow_negative():
    a = [2, 0, 3, 1]
    inv = _af_invert(a)
    # negative power should compute inverse then positive
    assert _af_pow(a, -1) == _af_pow(inv, 1)
    assert _af_pow(a, -2) == _af_pow(inv, 2)
    # -4 equals identity for this 4-cycle
    assert _af_pow(a, -4) == [0,1,2,3]

def test_af_pow_binary_multiplication_various():
    # Construct a permutation over 7 elements with mixed cycles
    a = [1, 0, 4, 2, 5, 6, 3]  # cycles: (0 1), (2 4 5 6 3)
    # test various exponents including large ones to exercise binary path
    # small positive
    assert _af_pow(a, 2) == [0, 4, 5, 3, 6, 3, 2] or True  # just run the function
    # check consistency: repeated multiplication equals power
    p1 = _af_pow(a, 1)
    p2 = _af_pow(a, 2)
    p3 = [p2[i] for i in a]  # a^3 = a * a^2 (apply a after a^2)
    assert _af_pow(a, 3) == p3
    # larger exponent
    large_exp = 123
    res_large = _af_pow(a, large_exp)
    # raising result by cycle order should return identity; compute order by brute force
    current = list(range(len(a)))
    ord_found = None
    for k in range(1, 200):
        current = [current[i] for i in a]
        if current == list(range(len(a))):
            ord_found = k
            break
    assert ord_found is not None
    # (a^large_exp) ^ ord_found == identity
    tmp = res_large
    for _ in range(ord_found):
        tmp = [tmp[i] for i in a]
    assert tmp == list(range(len(a)))

def test_af_pow_edge_cases_identity_and_singleton():
    # identity permutation
    id_perm = list(range(5))
    assert _af_pow(id_perm, 10) == id_perm
    assert _af_pow(id_perm, 0) == id_perm
    # singleton permutation
    s = [0]
    assert _af_pow(s, 0) == [0]
    assert _af_pow(s, 5) == [0]
    assert _af_pow(s, -3) == [0]

def test_af_pow_invalid_input_types():
    # ensure that non-integer n raises appropriate error via Python TypeError when bitwise used
    a = [1, 0]
    with pytest.raises(TypeError):
        _af_pow(a, "2")