import pytest

from sympy.combinatorics.permutations import _af_invert


def test_af_invert_basic():
    # basic permutation
    A = [1, 2, 0, 3]
    inv = _af_invert(A)
    assert inv == [2, 0, 1, 3]

    # verify that inverting twice yields original
    assert _af_invert(inv) == A


def test_af_invert_identity_and_singleton():
    # identity permutation
    I = [0, 1, 2, 3, 4]
    assert _af_invert(I) == I

    # singleton list
    assert _af_invert([0]) == [0]


def test_af_invert_long_random_permutations():
    import random
    # test several random permutations of varying sizes
    for n in [2, 3, 5, 10]:
        for _ in range(10):
            perm = list(range(n))
            random.shuffle(perm)
            inv = _af_invert(perm)
            # verify length preserved
            assert len(inv) == n
            # composing perm with its inverse should yield identity:
            composed = [perm[inv[i]] for i in range(n)]
            assert composed == list(range(n))
            # and inverse composed with perm is identity too
            composed2 = [inv[perm[i]] for i in range(n)]
            assert composed2 == list(range(n))
            # double-inversion returns original
            assert _af_invert(inv) == perm


def test_af_invert_raises_on_invalid_values():
    # Although _af_invert assumes a valid permutation, check behavior with bad inputs
    # If values are out of range, an IndexError will be raised when used as index.
    with pytest.raises(IndexError):
        _af_invert([0, 5, 1])  # 5 is out of range for length 3

    # Non-integer values used as indices should raise a TypeError
    with pytest.raises(TypeError):
        _af_invert([0, "1", 2])


def test_af_invert_with_duplicates_overwrites_positions():
    # If duplicates present, later entries overwrite earlier ones.
    # This is not a valid permutation but checks function behavior deterministically.
    a = [1, 1, 0]
    inv = _af_invert(a)
    # For a[0]=1 and a[1]=1, inv[1] will be set to 1 (the later index)
    assert inv == [2, 1, 0][: len(a)]  # result expected [2,1,0] but truncated to length a