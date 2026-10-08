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
    # identity permutation
    I = [0, 1, 2, 3, 4]
    assert _af_invert(I) == I

def test_af_invert_singleton_and_empty():
    # singleton
    assert _af_invert([0]) == [0]
    # empty permutation
    assert _af_invert([]) == []

def test_af_invert_large_random():
    # test on random permutations of various sizes
    import random
    for n in (2, 5, 10, 50):
        perm = list(range(n))
        random.shuffle(perm)
        inv = _af_invert(perm)
        # verify that applying inv to perm gives identity mapping:
        # inv[perm[i]] == i for all i
        for i, p in enumerate(perm):
            assert inv[p] == i
        # verify double invert returns original permutation
        assert _af_invert(inv) == perm

def test_af_invert_invalid_values_raises_index_error():
    # if permutation contains an out-of-range value, indexing will raise
    with pytest.raises(IndexError):
        _af_invert([0, 2])  # length 2 but contains 2 -> out of range

def test_af_invert_with_repeated_values_overwrites_last():
    # behavior with duplicates: later index overwrites earlier
    # this is not a valid permutation, but function will write last occurrence
    a = [1, 1, 0]
    inv = _af_invert(a)
    # positions: a[0]=1 -> inv[1]=0; a[1]=1 -> inv[1]=1 (overwritten); a[2]=0 -> inv[0]=2
    assert inv == [2, 1, 0][:len(inv)]  # len(inv)=3