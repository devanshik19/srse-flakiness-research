import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle  # Cycle used in Permutation constructor
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0
    assert repr(p).startswith("Permutation(")

def test_new_integer_creates_identity():
    p = Permutation(3)  # should create range(0..3)
    assert p._array_form == [0,1,2,3]
    assert p._size == 4

def test_new_array_form_valid():
    p = Permutation([0,2,1])
    assert p._array_form == [0,2,1]
    assert p._size == 3

def test_new_array_form_missing_zero_raises():
    with pytest.raises(ValueError):
        Permutation([2,1])  # missing 0

def test_new_array_with_duplicates_raises():
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_cyclic_form_conversion_and_size_extension():
    # cyclic input as list of lists
    p = Permutation([[4,5,6],[0,1]])
    assert isinstance(p, Permutation)
    # array form should map cycles to array up to max element 6
    assert p._size == 7
    # verify it's a permutation (contains 0..6)
    assert set(p._array_form) == set(range(7))
    # providing explicit larger size fills singletons
    p2 = Permutation([[4,5,6],[0,1],[19]], size=20)
    assert p2._size == 20
    assert len(p2._array_form) == 20
    assert set(range(20)) == set(p2._array_form)

def test_new_cycle_objects_and_permutation_copy_behaviour():
    # using Cycle instance
    c = Cycle(0,1,2)
    p_from_cycle = Permutation(c)
    assert isinstance(p_from_cycle, Permutation)
    # using a Permutation instance returns same if size matches
    p = Permutation([0,1,2])
    p2 = Permutation(p)
    assert p2 is p
    # if size differs, returns a new Permutation with adjusted size
    p3 = Permutation(p, size=5)
    assert isinstance(p3, Permutation)
    assert p3 is not p
    assert p3._size == 5
    assert p3._array_form[:3] == p._array_form

def test_new_non_sequence_single_integer_creates_identity():
    # passing a non-sequence numeric should create range(0..n)
    p = Permutation(0)  # identity of size 1
    assert p._array_form == [0]
    assert p._size == 1

def test_new_invalid_argument_types_raise():
    # nested mixed types (variety) should raise
    with pytest.raises(ValueError):
        # has_variety will detect mixture of sequences and non-sequences
        Permutation([ [1,2], 3 ])
    with pytest.raises(ValueError):
        # completely invalid type
        Permutation(object())

def test_new_cycle_with_repeated_elements_raises():
    with pytest.raises(ValueError):
        Permutation([[1,2],[2,3]])

def test_new_array_with_repeated_elements_raises_message():
    with pytest.raises(ValueError) as exc:
        Permutation([0,1,1])
    assert "repeated elements" in str(exc.value)

def test_new_size_extension_with_array_form():
    p = Permutation([0,1,2], size=6)
    assert p._size == 6
    assert p._array_form == [0,1,2,3,4,5]

# ensure repr/Basic integration does not error for constructed objects
def test_basic_new_integration():
    p = Permutation([0,1,2])
    # Basic.__new__ used in constructor; the object should be instance of Basic
    assert isinstance(p, Basic)