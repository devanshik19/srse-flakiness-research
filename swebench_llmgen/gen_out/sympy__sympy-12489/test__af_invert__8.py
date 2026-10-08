import pytest

from sympy.combinatorics.permutations import _af_invert


def test_af_invert_basic():
    # simple permutation
    A = [1, 2, 0, 3]
    inv = _af_invert(A)
    assert inv == [2, 0, 1, 3]
    # invert again yields original
    assert _af_invert(inv) == A

def test_af_invert_identity():
    # identity permutation should invert to itself
    I = [0, 1, 2, 3, 4]
    assert _af_invert(I) == I

def test_af_invert_singleton():
    # single-element permutation
    assert _af_invert([0]) == [0]

def test_af_invert_longer_random():
    # test on a random permutation of length 10
    import random
    n = 10
    perm = list(range(n))
    random.seed(0)
    random.shuffle(perm)
    inv = _af_invert(perm)
    # composing perm and inv should give identity: perm[inv[i]] == i
    identity = [perm[inv[i]] for i in range(n)]
    assert identity == list(range(n))
    # and inv[perm[i]] == i
    identity2 = [inv[perm[i]] for i in range(n)]
    assert identity2 == list(range(n))

def test_af_invert_invalid_values_index_error():
    # If permutation contains an out-of-range value, the function will raise IndexError
    A = [1, 5, 0]  # 5 is out of range for length 3
    with pytest.raises(IndexError):
        _af_invert(A)

def test_af_invert_non_integer_values_type_error():
    # Non-integer values used as indices should raise a TypeError
    A = [1, "a", 0]
    with pytest.raises(TypeError):
        _af_invert(A)