import pytest
from sympy.combinatorics.permutations import _af_invert, _af_rmul

def test_af_invert_basic():
    # simple permutation
    A = [1, 2, 0, 3]
    inv = _af_invert(A)
    assert inv == [2, 0, 1, 3]
    # verify that inverse composed with original is identity
    assert _af_rmul(inv, A) == [0, 1, 2, 3]
    assert _af_rmul(A, inv) == [0, 1, 2, 3]

def test_af_invert_identity():
    # identity permutation
    A = [0,1,2,3,4]
    inv = _af_invert(A)
    assert inv == A
    assert _af_rmul(inv, A) == A

def test_af_invert_singleton_and_two_cycle():
    # singleton
    A = [0]
    assert _af_invert(A) == [0]
    # 2-cycle
    A = [1,0]
    assert _af_invert(A) == [1,0]
    assert _af_rmul(A, _af_invert(A)) == [0,1]

def test_af_invert_longer_random():
    # test for several random permutations
    import random
    for n in (1,2,3,5,10):
        # generate random permutation
        perm = list(range(n))
        random.shuffle(perm)
        inv = _af_invert(perm)
        # check that inv is a permutation of 0..n-1
        assert sorted(inv) == list(range(n))
        # check inverse property both ways
        assert _af_rmul(inv, perm) == list(range(n))
        assert _af_rmul(perm, inv) == list(range(n))

def test_af_invert_raises_on_invalid_values():
    # although _af_invert assumes valid permutation values,
    # ensure that out-of-range indices raise IndexError when used
    A = [2, 0]  # invalid for length 2 (2 is out of range)
    with pytest.raises(IndexError):
        _af_invert(A)

def test_af_invert_with_repeated_values():
    # repeated values will cause overwrite; behavior: last wins.
    A = [1,1,0]
    inv = _af_invert(A)
    # inv[1] should be index of last occurrence of 1 (which is 1)
    # inv[0] should be index of 2
    assert inv == [2, 1, 0] or inv[0] == 2