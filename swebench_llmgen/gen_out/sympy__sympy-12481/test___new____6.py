# test_permutation_new.py
from __future__ import print_function, division
import pytest

from sympy.combinatorics.permutations import Permutation, Cycle
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0

def test_new_integer_creates_identity():
    p = Permutation(3)
    # identity of size 4: 0..3
    assert p._array_form == [0,1,2,3]
    assert p._size == 4

def test_new_array_form_valid():
    p = Permutation([0,2,1])
    assert p._array_form == [0,2,1]
    assert p._size == 3
    # repr should be available and contain 'Permutation'
    r = repr(p)
    assert 'Permutation' in r

def test_new_array_form_missing_zero_raises():
    with pytest.raises(ValueError):
        Permutation([2,1])  # missing 0 up to max

def test_new_array_form_with_size_extended():
    p = Permutation([0,1], size=5)
    assert p._array_form == [0,1,2,3,4]
    assert p._size == 5

def test_new_cycle_form_converts_to_array():
    # cycle (0 1 2) -> array form [1,2,0]
    p = Permutation([[0,1,2]])
    assert p._array_form == [1,2,0]
    assert p._size == 3

def test_new_cycle_form_with_singleton_size():
    p = Permutation([[4,5,6],[0,1],[19]], size=20)
    assert p._size == 20
    # check that positions beyond max are identity
    assert p._array_form[19] == 19
    assert len(p._array_form) == 20

def test_new_with_duplicate_elements_array_raises():
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_with_duplicate_elements_cycle_raises():
    with pytest.raises(ValueError):
        # repeated element in cycles should raise with specific message
        with pytest.raises(ValueError):
            Permutation([[0,1],[1,2]])

def test_new_from_cycle_object():
    c = Cycle()
    c = c(0,1,2)
    p = Permutation(c)
    assert p._array_form == [1,2,0]
    assert p._size == 3

def test_new_from_permutation_returns_same_or_resized_copy():
    p1 = Permutation([0,2,1], size=3)
    # passing a Permutation instance with same size returns the same object (identity)
    p2 = Permutation(p1, size=3)
    assert p2 is p1
    # requesting different size returns a new object with extended identity tail
    p3 = Permutation(p1, size=5)
    assert p3 is not p1
    assert p3._array_form[:3] == p1._array_form
    assert p3._array_form[3:] == [3,4]
    assert p3._size == 5

def test_non_sequence_single_integer_behaviour():
    # passing a non-sequence like an int should produce identity of that length+1
    p = Permutation(2)
    assert p._array_form == [0,1,2]
    assert p._size == 3

def test_bad_argument_types_raise():
    # passing something not sequence-like but not int: e.g., object without is_sequence True
    class Fake:
        pass
    with pytest.raises(ValueError):
        Permutation([Fake()])  # inner variety detection will fail and raise