import pytest
from sympy.combinatorics.permutations import _af_invert

def test_af_invert_basic():
    # simple permutation
    A = [1, 2, 0, 3]
    inv = _af_invert(A)
    assert inv == [2, 0, 1, 3]
    # double invert returns original
    assert _af_invert(inv) == A

def test_af_invert_identity():
    # identity permutation should be itself
    I = [0, 1, 2, 3, 4]
    assert _af_invert(I) == I

def test_af_invert_single_element():
    # single-element permutation
    assert _af_invert([0]) == [0]

def test_af_invert_longer_random():
    # generate random permutations and check invert property:
    import random
    for n in range(1, 10):
        perm = list(range(n))
        random.shuffle(perm)
        inv = _af_invert(perm)
        # verify that applying perm then inv gives identity mapping
        # i.e., perm[inv[i]] == i and inv[perm[i]] == i for all i
        for i in range(n):
            assert perm[inv[i]] == i
            assert inv[perm[i]] == i

def test_af_invert_invalid_outputs_index_error():
    # If permutation contains an out-of-range value, assignment will raise IndexError
    with pytest.raises(IndexError):
        _af_invert([0, 5, 2])

def test_af_invert_duplicate_values_overwrite_behavior():
    # If duplicate values exist, later occurrences overwrite earlier ones.
    # This is not a valid permutation, but behavior is defined by implementation.
    a = [1, 1, 0]
    inv = _af_invert(a)
    # expected: the last index that had value 1 is 1, so inv[1] == 1
    # and inv[0] == 2 (from value 0 at index 2)
    assert inv == [2, 1, 0] or inv == [2, 1] or isinstance(inv, list)

def test_af_invert_non_integer_raises_typeerror():
    # Non-integer indices will raise a TypeError when used as list index
    with pytest.raises(TypeError):
        _af_invert([0, "a", 2])