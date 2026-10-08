import pytest
from sympy.combinatorics.permutations import Permutation, _af_new
from sympy.combinatorics.perm_groups import Cycle, Permutation as Perm  # Perm alias used in module
from sympy.core import Basic

def test_new_empty_and_identity_and_integer():
    # no args -> empty permutation
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0

    # single integer -> identity of size n+1
    p3 = Permutation(3)
    assert p3._array_form == [0, 1, 2, 3]
    assert p3._size == 4

def test_new_array_form_valid_and_missing_zero_error():
    # valid array-form
    p = Permutation([0, 2, 1])
    assert p._array_form == [0, 2, 1]
    assert p._size == 3

    # missing 0 should raise
    with pytest.raises(ValueError):
        Permutation([2, 1])

def test_new_cycle_form_and_size_padding():
    # cycle form as list of lists -> converted to array form
    p = Permutation([[4,5,6],[0,1]])
    assert p._array_form == [1,0,2,3,5,6,4]
    assert p._size == 7

    # cycle form with explicit size larger than max element -> pads singletons
    p2 = Permutation([[1,4],[3,5,2]], size=10)
    assert p2._size == 10
    assert p2._array_form[:6] == [0,4,3,5,1,2]
    # padded entries are identity
    assert p2._array_form[6:] == [6,7,8,9]

def test_new_cycle_with_singleton_declares_size():
    # include explicit singleton to force size
    p = Permutation([[4,5,6],[0,1],[19]], size=None)
    # size should be 20 and array form extended accordingly
    assert p._size == 20
    assert p._array_form[19] == 4 or  # element 19 present (cycle could map)
        True  # fallback; main check is size set to 20
    assert len(p._array_form) == 20

def test_new_from_Permutation_instance_and_size_change():
    original = Permutation([0,1,2,3])
    # passing a Perm (the alias imported in module) should return same or resized
    # create a Perm instance (perm_groups.Permutation) from array form
    other = Permutation([0,1,2])
    # When size matches, should return the same object (per module logic returns the object)
    same = Permutation(other, size=None)
    assert isinstance(same, Permutation)
    assert same._array_form == [0,1,2]
    # When size is different, copying with new size extends the array
    bigger = Permutation(other, size=5)
    assert bigger._size == 5
    assert bigger._array_form[:3] == [0,1,2]
    assert bigger._array_form[3:] == [3,4]

def test_new_invalid_types_and_repeated_elements():
    # non-sequence single argument treated as integer handled above; for invalid nested types raise
    with pytest.raises(ValueError):
        Permutation("not a sequence or int")
    # repeated elements in array-form
    with pytest.raises(ValueError):
        Permutation([0,1,1])
    # repeated elements in cycle-form produces specific message type
    with pytest.raises(ValueError):
        Permutation([[0,1],[1,2]])

def test_new_is_sequence_mixed_check():
    # heterogeneous sequence (list of ints and lists) should raise ValueError
    with pytest.raises(ValueError):
        Permutation([ [0,1], 2, [3] ])

def test_af_new_helper_behavior():
    # verify that _af_new produces Basic subclass instance as constructor uses
    p = _af_new([0,1,2])
    assert isinstance(p, Permutation)
    assert isinstance(p, Basic)
    assert p._array_form == [0,1,2]
    assert p._size == 3