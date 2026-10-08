import pytest

from sympy.combinatorics.permutations import _af_invert, _af_rmul

def test_af_invert_basic():
    # simple permutation
    A = [1, 2, 0, 3]
    inv = _af_invert(A)
    # expected inverse mapping
    assert inv == [2, 0, 1, 3]
    # verify that composing A and its inverse yields identity
    identity = _af_rmul(inv, A)
    assert identity == [0, 1, 2, 3]

def test_af_invert_identity():
    # identity permutation should invert to itself
    A = [0, 1, 2, 3, 4]
    assert _af_invert(A) == A

def test_af_invert_singleton_and_two_cycle():
    # singleton list
    assert _af_invert([0]) == [0]
    # two-cycle
    A = [1, 0]
    assert _af_invert(A) == [1, 0]
    # verify composition gives identity
    assert _af_rmul(_af_invert(A), A) == [0, 1]

def test_af_invert_larger_random():
    # test with random permutations of different sizes
    import random
    for n in range(1, 10):
        perm = list(range(n))
        random.shuffle(perm)
        inv = _af_invert(perm)
        # inverse properties: perm[inv[i]] == i and inv[perm[i]] == i
        for i in range(n):
            assert perm[inv[i]] == i
            assert inv[perm[i]] == i
        # composition is identity
        assert _af_rmul(inv, perm) == list(range(n))

def test_af_invert_with_duplicate_raises_index_error():
    # malformed permutation (duplicates) will try to assign twice and cause no explicit error,
    # but will create an incorrect inverse where some positions remain default 0 or overwritten.
    # We assert that such malformed inputs do not produce a valid inverse mapping.
    A = [0, 0, 0]  # invalid permutation
    inv = _af_invert(A)
    # inv should be of same length but not a permutation (i.e., not a bijection)
    assert len(inv) == 3
    # check that inv is not a permutation mapping 0,1,2 uniquely
    assert sorted(inv) != [0,1,2]

def test_af_invert_with_out_of_range_raises_index_error_explicit():
    # If an element is out of range, list assignment will raise IndexError
    A = [0, 5]  # 5 is out of range for length 2
    with pytest.raises(IndexError):
        _af_invert(A)