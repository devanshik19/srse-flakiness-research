import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle, Permutation as Perm  # Perm type used in constructor checks
from sympy.combinatorics.permutations import Permutation as PermutationClass
from sympy.core import Basic

def test_new_empty_and_size():
    # no args -> identity of size 0
    p = Permutation()
    assert isinstance(p, Basic)
    assert p._array_form == []
    assert p._size == 0
    # size keyword
    p5 = Permutation(size=5)
    assert p5._array_form == [0,1,2,3,4]
    assert p5._size == 5

def test_new_integer_argument_identity():
    # single integer n -> identity of size n+1
    p = Permutation(3)
    assert p._array_form == [0,1,2,3]
    assert p._size == 4

def test_new_array_form_valid_and_invalid():
    # valid array form must contain 0..n-1
    p = Permutation([0,2,1])
    assert p._array_form == [0,2,1]
    assert p._size == 3

    # missing zero or missing entries -> ValueError
    with pytest.raises(ValueError):
        Permutation([2,1])  # missing 0 for array of size 2

    # duplicate entries in array form -> ValueError
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_cycle_form_and_size_extension():
    # cycle form as list of lists
    p = Permutation([[4,5,6],[0,1]])
    # expected array form as in docstring example
    assert p._array_form == [1,0,2,3,5,6,4]
    assert p._size == 7

    # cycle form with explicit size larger than max element
    p20 = Permutation([[4,5,6],[0,1],[19]], size=20)
    assert p20._array_form[:7] == [1,0,2,3,5,6,4]
    assert p20._size == 20
    # ensure singletons filled out up to size
    assert len(p20._array_form) == 20
    assert set(range(20)) == set(p20._array_form)

def test_new_cycle_input_without_singletons_but_size_given():
    # cycles given without singletons, but size expands to include missing points
    p = Permutation([[1,4],[3,5,2]], size=10)
    assert p._size == 10
    # array_form should include fixed points 0,6..9
    assert p._array_form[0] == 0
    assert p._array_form[6:] == [6,7,8,9]

def test_new_from_perm_and_cycle_objects():
    # Using a Cycle object should convert to array form
    c = Cycle( (0,1,2) )
    p_from_cycle = Permutation(c)
    # Cycle(0,1,2) maps 0->1,1->2,2->0
    assert p_from_cycle._array_form[0:3] == [1,2,0]

    # Using a Perm (Permutation from perm_groups) returns copy or same depending on size
    # Build a Perm (from perm_groups) via array form
    base = Perm([1,0,2])
    # same size -> returns the same Perm object (per code returns a)
    p_same = Permutation(base)
    assert p_same is base
    # different size -> returns a new SymPy PermutationClass object with requested size
    p_resized = Permutation(base, size=5)
    assert isinstance(p_resized, PermutationClass)
    assert p_resized._size == 5
    assert p_resized._array_form[:3] == base.array_form

def test_invalid_argument_types():
    # Non-sequence should be handled (integer handled above).
    # Passing mixed sequence types (list containing a list and int) should raise
    with pytest.raises(ValueError):
        Permutation([ [0,1], 2 ])  # has_variety true -> ok flag False -> ValueError

    # Passing multiple args (treated as cycle args) should convert to Cycle
    # e.g., Permutation(1,2) should interpret as Cycle(1,2)
    p = Permutation(1,2)
    # 1,2 as a cycle means mapping 1->2,2->1 so with implicit 0 included identity for 0
    assert isinstance(p, PermutationClass)
    assert p._array_form[0] == 0
    # Check that applying cycle (1 2) gives swapped entries
    assert p._array_form[1] == 2 and p._array_form[2] == 1

def test_size_extension_does_not_truncate():
    # array form shorter than requested size -> extend with fixed points
    p = Permutation([0,2,1], size=6)
    assert p._size == 6
    assert p._array_form[3:] == [3,4,5]

def test_bad_arguments_raise():
    # Non-list and non-integer should raise when it's a non-sequence object
    class Dummy: pass
    # Dummy instance is neither Perm nor Cycle nor sequence -> treated as non-sequence int path and will try range(a+1)
    # but that will fail because Dummy not convertible to int; ensure TypeError or ValueError raised
    with pytest.raises(Exception):
        Permutation(Dummy())