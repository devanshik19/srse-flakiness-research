import pytest
from sympy.combinatorics.permutations import _af_invert, _af_rmul

def test_af_invert_basic():
    # simple permutation
    A = [1, 2, 0, 3]
    inv = _af_invert(A)
    assert inv == [2, 0, 1, 3]
    # composing inverse with original yields identity via _af_rmul
    ident = _af_rmul(inv, A)
    assert ident == [0, 1, 2, 3]

def test_af_invert_identity():
    # identity permutation should invert to itself
    A = [0, 1, 2, 3, 4]
    assert _af_invert(A) == A

def test_af_invert_singleton():
    # single-element permutation
    A = [0]
    assert _af_invert(A) == [0]

def test_af_invert_two_cycle():
    # 2-cycle swap
    A = [1, 0]
    assert _af_invert(A) == [1, 0]
    # composing gives identity
    assert _af_rmul(_af_invert(A), A) == [0, 1]

def test_af_invert_long_random():
    # test random permutations for correctness: inverse composed equals identity
    import random
    for n in (1, 2, 3, 5, 10):
        lst = list(range(n))
        for _ in range(5):
            random.shuffle(lst)
            A = list(lst)
            inv = _af_invert(A)
            # check that inv is a permutation of same elements
            assert sorted(inv) == list(range(n))
            # check that composing inv and A gives identity
            ident = _af_rmul(inv, A)
            assert ident == list(range(n))

def test_af_invert_raises_on_invalid_input():
    # The function assumes a valid permutation; behavior on invalid input:
    # If elements are out of range, it will raise IndexError when assigning.
    with pytest.raises(IndexError):
        _af_invert([0, 2])  # 2 is out of range for length 2
    # If there are duplicates, it will overwrite entries producing wrong permutation,
    # but should not raise. Check result is not a valid permutation mapping.
    A = [0, 0, 2]
    inv = _af_invert(A)
    # inv length matches, but will have one position not set properly (duplicate causes overwrite)
    assert len(inv) == 3
    # The overwritten position leads to missing value in inverse mapping
    assert sorted(inv) != [0, 1, 2]