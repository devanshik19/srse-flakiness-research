import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle, Permutation as Perm  # Perm is used internally as type check
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0
    assert isinstance(p, Basic)

def test_new_integer_creates_identity():
    p = Permutation(3)  # creates identity of size 4 (0..3)
    assert p._array_form == [0,1,2,3]
    assert p._size == 4

def test_new_array_form_preserved():
    arr = [0,2,1]
    p = Permutation(arr)
    assert p._array_form == arr
    assert p._size == 3

def test_new_array_missing_zero_raises():
    with pytest.raises(ValueError):
        Permutation([2,1])  # missing 0..2

def test_new_repeated_elements_raises():
    with pytest.raises(ValueError):
        Permutation([0,1,1])  # duplicates in array form

def test_new_cycle_form_converts_to_array():
    # cycle [[4,5,6],[0,1]] should produce array form of example
    p = Permutation([[4,5,6],[0,1]])
    assert p._array_form == [1,0,2,3,5,6,4]
    assert p._size == 7

def test_new_cycle_form_with_size_extends():
    p = Permutation([[1,4],[3,5,2]], size=10)
    assert p._size == 10
    # array_form should have length 10 and extend by identity elements at end
    assert len(p._array_form) == 10
    # first six as in docstring example
    assert p._array_form[:6] == [0,4,3,5,1,2]
    assert p._array_form[6:] == [6,7,8,9]

def test_new_from_perm_returns_copy_or_adjusts_size():
    # create a Perm (Permutation from perm_groups) and pass to constructor
    base = Permutation([0,1,2,3])
    # Passing the same permutation object should return it if size matches
    same = Permutation(base)
    assert same is base
    # Passing with different size should return a new Permutation with extended size
    larger = Permutation(base, size=6)
    assert larger is not base
    assert larger._size == 6
    assert larger._array_form[:4] == [0,1,2,3]
    assert larger._array_form[4:] == [4,5]

def test_new_from_cycle_instance():
    # Create a Cycle via Cycle class and pass it
    c = Cycle(1,2,3)
    p = Permutation(c)
    # cyclic (1 2 3) on default elements should produce array form
    assert isinstance(p, Permutation)
    assert p._size == len(p._array_form)

def test_new_non_sequence_singleton_behavior():
    # passing a non-sequence (int) should create identity 0..n
    p = Permutation(0)
    assert p._array_form == [0]
    p2 = Permutation(1)
    assert p2._array_form == [0,1]

def test_invalid_argument_types_raise():
    # mixed list of sequences and ints triggers error (has_variety)
    with pytest.raises(ValueError):
        Permutation([ [0,1], 2 ])

def test_size_increase_without_truncation():
    # array form shorter than size extends by identity, but cannot truncate
    p = Permutation([0,2,1], size=5)
    assert p._size == 5
    assert p._array_form == [0,2,1,3,4]