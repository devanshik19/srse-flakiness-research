import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle  # Cycle used for some constructions
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0

def test_new_integer_n_creates_identity():
    p = Permutation(3)
    assert isinstance(p, Permutation)
    # identity of size 4: range(0, 4)
    assert p._array_form == [0, 1, 2, 3]
    assert p._size == 4

def test_new_array_form_keeps_array():
    p = Permutation([0, 2, 1])
    assert p._array_form == [0, 2, 1]
    assert p._size == 3
    assert isinstance(p, Permutation)

def test_new_array_form_missing_zero_raises():
    with pytest.raises(ValueError):
        Permutation([2, 1])  # missing 0 for array form should error

def test_new_repeated_elements_in_array_raises():
    with pytest.raises(ValueError):
        Permutation([0, 1, 1])

def test_new_cycle_list_converts_to_array():
    p = Permutation([[4, 5, 6], [0, 1]])
    # array form expected from docstring
    assert p._array_form == [1, 0, 2, 3, 5, 6, 4]
    assert p._size == 7

def test_new_cycle_with_size_extends_singletons():
    p = Permutation([[4,5,6],[0,1],[19]], size=20)
    assert p._array_form == [1,0,2,3,5,6,4]  # array portion
    assert p._size == 20
    # ensure the internal array_form (list) is extended to size
    assert len(p._array_form) == 20
    # positions 7..19 should be fixed points (i -> i)
    for i in range(7, 20):
        assert p._array_form[i] == i

def test_new_cycle_with_repeated_elements_raises():
    with pytest.raises(ValueError):
        # repeated '1' across cycles
        Permutation([[1,2,1]])

def test_new_sequence_of_sequences_invalid_raises():
    # mixing nested sequences but not valid cycle structure should raise
    with pytest.raises(ValueError):
        Permutation([[1, 2], 3])  # has_variety True -> ok flag False -> ValueError

def test_new_from_permutation_returns_same_object_or_copy():
    p1 = Permutation([0,1,2])
    # passing Permutation instance returns same if size matches
    p2 = Permutation(p1)
    assert p2 is p1
    # requesting different size returns a new object with extended size
    p3 = Permutation(p1, size=5)
    assert p3 is not p1
    assert isinstance(p3, Permutation)
    assert p3._size == 5
    assert p3._array_form[:3] == [0,1,2]
    # extended part are fixed points
    assert p3._array_form[3] == 3 and p3._array_form[4] == 4

def test_new_from_cycle_object_and_cycle_args():
    c = Cycle(0,1,2)
    p_from_cycle = Permutation(c)
    # Cycle(0,1,2) should produce appropriate array form
    assert isinstance(p_from_cycle, Permutation)
    # also constructing via multiple args treated as Cycle: Permutation(0,1) -> Cycle(0,1)
    p_from_args = Permutation(0,1)
    assert isinstance(p_from_args, Permutation)
    # check that a basic swap Permutation(0,1) yields [1,0]
    assert p_from_args._array_form == [1,0]

def test_new_with_size_extends_array_form_but_not_truncate():
    p = Permutation([0,1,2], size=6)
    assert p._size == 6
    # array_form extended with fixed points
    assert p._array_form == [0,1,2,3,4,5]

def test_new_non_sequence_singleton_behaviour():
    # passing a non-sequence (e.g., int) returns identity of range(a+1)
    p = Permutation(0)
    assert p._array_form == [0]
    p = Permutation(1)
    assert p._array_form == [0,1]

def test_new_bad_argument_type_raises():
    class Dummy:
        def __iter__(self):
            return iter([1,1,2])  # causes has_dups
    # But since it's a sequence, it will be processed and duplicated check raises
    with pytest.raises(ValueError):
        Permutation(Dummy())

# ensure Permutation instances are Basic subclass instances as created via Basic.__new__
def test_new_returns_basic_subclass():
    p = Permutation([0,1])
    assert isinstance(p, Basic)