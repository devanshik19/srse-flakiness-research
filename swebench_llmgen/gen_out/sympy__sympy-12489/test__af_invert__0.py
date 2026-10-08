import pytest

from sympy.combinatorics.permutations import _af_invert, _af_rmul

def test_af_invert_basic():
    # simple permutation
    A = [1, 2, 0, 3]
    invA = _af_invert(A)
    assert invA == [2, 0, 1, 3]
    # check that inverting twice yields original
    assert _af_invert(invA) == A
    # check that multiplying A by its inverse yields identity
    assert _af_rmul(A, invA) == [0, 1, 2, 3]
    assert _af_rmul(invA, A) == [0, 1, 2, 3]

def test_af_invert_identity_and_singleton():
    # identity permutation
    I = [0, 1, 2, 3, 4]
    assert _af_invert(I) == I
    # singleton permutation
    S = [0]
    assert _af_invert(S) == [0]

def test_af_invert_random_permutations():
    import random
    # test several random permutations of varying sizes
    for n in range(1, 8):
        for _ in range(20):
            perm = list(range(n))
            random.shuffle(perm)
            inv = _af_invert(perm)
            # compose should give identity
            assert _af_rmul(perm, inv) == list(range(n))
            assert _af_rmul(inv, perm) == list(range(n))
            # double invert returns original
            assert _af_invert(inv) == perm

def test_af_invert_invalid_input_raises_index_error():
    # If permutation contains an out-of-range value, assignment will raise IndexError
    bad = [0, 2]  # for length 2, value 2 is out of range
    with pytest.raises(IndexError):
        _af_invert(bad)

def test_af_invert_non_integer_values():
    # Non-integer values used as indices should raise TypeError when used as list index
    bad = [0, 1.5]
    with pytest.raises(TypeError):
        _af_invert(bad)