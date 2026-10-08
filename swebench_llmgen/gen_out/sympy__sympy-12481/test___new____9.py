# test_permutation_new.py
from __future__ import print_function, division
import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle
from sympy.combinatorics.permutations import Permutation as Perm  # alias used in source
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Basic)
    assert p._array_form == []
    assert p._size == 0
    assert repr(p).startswith("Permutation(")

def test_new_integer_creates_identity():
    p = Permutation(3)  # should create [0,1,2,3]
    assert p._array_form == [0,1,2,3]
    assert p._size == 4

def test_new_array_form_valid():
    p = Permutation([0,2,1])
    assert p._array_form == [0,2,1]
    assert p._size == 3

def test_new_array_form_missing_zero_raises():
    with pytest.raises(ValueError):
        Permutation([2,1])  # missing 0 in array form

def test_new_repeated_elements_array_raises():
    with pytest.raises(ValueError):
        Permutation([0,1,1])  # duplicate

def test_new_cycle_form_expands_and_size_arg():
    # Cycle form given as list of cycles
    p = Permutation([[4,5,6],[0,1]])
    assert p._array_form == [1,0,2,3,5,6,4]
    assert p._size == 7

    # with explicit size larger than cycles -> size extends with singletons
    p2 = Permutation([[1,4],[3,5,2]], size=10)
    assert p2._size == 10
    assert p2._array_form[:6] == [0,4,3,5,1,2]
    assert p2._array_form[6:] == [6,7,8,9]

def test_new_cycle_with_singleton_specified_size():
    # Cycle form with explicit singleton to indicate size
    p = Permutation([[4,5,6],[0,1],[19]])
    assert p._size == 20
    assert p._array_form[:7] == [1,0,2,3,5,6,4]

def test_new_from_permutation_same_size_returns_same_object():
    p = Permutation([0,1,2])
    q = Permutation(p)  # no size specified -> should return p itself
    assert q is p

def test_new_from_permutation_different_size_returns_new():
    p = Permutation([0,1,2])
    q = Permutation(p, size=5)
    assert q is not p
    assert q._size == 5
    # array should have been extended
    assert q._array_form == [0,1,2,3,4]

def test_new_from_cycle_object_and_from_cycle_class():
    # Using Cycle instance (from sympy.combinatorics.perm_groups.Cycle)
    c = Cycle(1,2,3)
    p = Permutation(c)
    # check it's a permutation object and valid array form
    assert isinstance(p, Permutation)
    assert set(p._array_form) == set(range(len(p._array_form)))

def test_new_non_sequence_interpreted_as_integer():
    # non-sequence (like int) should produce identity of that size
    p = Permutation(2)  # will create [0,1,2]
    assert p._array_form == [0,1,2]

def test_new_invalid_argument_type_raises():
    # Passing a mixed list (not allowed) or nested non-uniform should raise
    with pytest.raises(ValueError):
        # has_variety true when elements are sequences and non-sequences mixed
        Permutation([ [1,2], 3 ])

def test_new_duplicate_in_cycles_raises():
    with pytest.raises(ValueError):
        # duplicate across cycles should raise and message references Cycle
        Permutation([[0,1],[1,2]])

def test_size_increase_does_not_truncate_or_change_mapping():
    p = Permutation([1,0,2])  # size 3
    q = Permutation(p, size=6)
    assert q._size == 6
    # original mapping preserved for indices < original size
    assert q._array_form[0:3] == [1,0,2]
    # new tail are singletons
    assert q._array_form[3:] == [3,4,5]