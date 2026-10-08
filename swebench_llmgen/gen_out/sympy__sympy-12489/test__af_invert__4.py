import pytest
from sympy.combinatorics.permutations import _af_invert

def test_af_invert_basic():
    # simple permutation: positions 0->1,1->2,2->0,3->3
    A = [1, 2, 0, 3]
    inv = _af_invert(A)
    assert inv == [2, 0, 1, 3]
    # double invert returns original
    assert _af_invert(inv) == A

def test_af_invert_identity():
    # identity permutation should invert to itself
    I = [0, 1, 2, 3, 4]
    assert _af_invert(I) == I

def test_af_invert_singleton():
    # single element
    assert _af_invert([0]) == [0]

def test_af_invert_two_cycle():
    # 2-cycle
    A = [1, 0]
    assert _af_invert(A) == [1, 0]

def test_af_invert_longer_random():
    # test for a random permutation of length n
    import random
    n = 20
    A = list(range(n))
    random.shuffle(A)
    inv = _af_invert(A)
    # check that inv[A[i]] == i for all i
    for i, ai in enumerate(A):
        assert inv[ai] == i
    # and that composing A and inv yields identity
    composed = [A[inv[i]] for i in range(n)]
    assert composed == list(range(n))

def test_af_invert_invalid_values_raises_index_error():
    # if permutation contains out-of-range value, function will raise IndexError
    with pytest.raises(IndexError):
        _af_invert([2, 0])  # length 2 but contains 2 -> index error when assigning

def test_af_invert_duplicate_values_overwrites():
    # If duplicates present, last occurrence wins (function will overwrite entries)
    # This is not a valid permutation but tests function behavior deterministically.
    A = [1, 1, 0]
    inv = _af_invert(A)
    # inv[1] should be index of last occurrence of 1, which is 1
    assert inv[1] == 1
    # inv[0] should be index of 0
    assert inv[0] == 2
    # length preserved
    assert len(inv) == len(A)