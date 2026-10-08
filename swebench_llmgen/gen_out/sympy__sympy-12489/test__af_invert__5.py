import pytest
from sympy.combinatorics.permutations import _af_invert

def test_af_invert_basic():
    # simple permutation
    A = [1, 2, 0, 3]
    inv = _af_invert(A)
    assert inv == [2, 0, 1, 3]

    # double invert yields original
    assert _af_invert(inv) == A

def test_af_invert_identity():
    # identity permutation should invert to itself
    I = [0, 1, 2, 3, 4]
    assert _af_invert(I) == I

def test_af_invert_longer():
    # a longer permutation
    A = [3, 0, 4, 1, 2]
    inv = _af_invert(A)
    # verify mapping: A[i] = j  <=>  inv[j] = i
    for i, j in enumerate(A):
        assert inv[j] == i
    # check explicit expected inverse
    assert inv == [1, 3, 4, 0, 2]

def test_af_invert_singleton_and_empty():
    # singleton
    assert _af_invert([0]) == [0]
    # empty permutation
    assert _af_invert([]) == []

def test_af_invert_raises_on_invalid_values():
    # Although _af_invert does not explicitly validate, passing invalid values
    # (e.g. out of range indices) will raise an IndexError when used.
    with pytest.raises(IndexError):
        _af_invert([10, 0, 1])

def test_af_invert_handles_duplicates_leading_to_overwrite():
    # If duplicates are present, later entries overwrite earlier ones.
    # This is not a valid permutation, but behavior is deterministic.
    A = [1, 1, 0]
    inv = _af_invert(A)
    # inv[1] should be index of last occurrence of 1 (i.e., 1)
    assert inv == [2, 1, 0]