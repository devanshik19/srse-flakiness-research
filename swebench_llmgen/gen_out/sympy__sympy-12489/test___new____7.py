import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.permutations import Cycle
from sympy.core import Basic

def test_new_empty_and_identity():
    # No args -> empty permutation
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0

    # Single int -> identity of size n+1
    p = Permutation(3)
    assert p._array_form == [0, 1, 2, 3]
    assert p._size == 4

def test_new_array_form_valid_and_invalid():
    # valid array form starting at 0 up to n-1
    p = Permutation([0, 2, 1])
    assert p._array_form == [0, 2, 1]
    assert p._size == 3

    # missing 0 should raise
    with pytest.raises(ValueError):
        Permutation([2, 1])

    # duplicated entries in array form should raise
    with pytest.raises(ValueError):
        Permutation([0, 1, 1])

def test_new_cycle_form_and_size_extension():
    # cycle form: list of lists
    p = Permutation([[4, 5, 6], [0, 1]])
    # cycle [[4,5,6]] maps 4->5,5->6,6->4; [0,1] swaps 0 and1
    assert isinstance(p, Permutation)
    assert p._array_form[0:7] == [1,0,2,3,5,6,4]
    assert p._size == 7

    # cycle with explicit size larger than max element fills singletons
    p = Permutation([[4,5,6],[0,1],[19]], size=20)
    assert p._size == 20
    # positions beyond max cycle should be identity
    assert p._array_form[7:] == list(range(7,20))

def test_new_cycle_notation_without_singletons_and_size_param():
    # when cycles don't include 0..n-1, providing size fills in missing singletons
    p = Permutation([[1,4],[3,5,2]], size=10)
    assert p._size == 10
    # check that array_form has identity entries 0,6..9 in appropriate spots
    assert p._array_form[0] == 0
    assert p._array_form[6:] == [6,7,8,9]
    # verify mapping for the cycle parts
    # cycle [1,4] means 1->4 and 4->1
    assert p._array_form[1] == 4
    assert p._array_form[4] == 1

def test_new_from_permutation_and_cycle_objects():
    # Passing an existing Permutation returns it (or a copy if size differs)
    a = Permutation([0,2,1],)
    b = Permutation(a)
    # if same size, should return the same object (per code returns a)
    assert b is a

    # if size differs, returns a new Permutation with adjusted size
    c = Permutation(a, size=5)
    assert c is not a
    assert c._size == 5
    assert c._array_form[:3] == a._array_form
    assert c._array_form[3:] == [3,4]

    # Passing a Cycle instance should convert to array form
    cyc = Cycle()
    cyc = cyc(0,1,2)
    p = Permutation(cyc)
    assert isinstance(p, Permutation)
    # cycle (0,1,2) -> mapping 0->1,1->2,2->0
    assert p._array_form[:3] == [1,2,0]

def test_new_invalid_argument_types():
    # Non-sequence like string should be treated as scalar -> identity up to that int
    p = Permutation(2)  # scalar handled earlier, but ensure no error for int-like
    assert p._array_form == [0,1,2]

    # Passing a nested mixed sequence should raise ValueError
    with pytest.raises(ValueError):
        # has_variety will detect inner variance (e.g., mix of ints and lists)
        Permutation([1, [2]])

    # Passing something completely invalid should raise ValueError
    with pytest.raises(ValueError):
        Permutation(object())

def test_new_extending_size_from_array_form():
    # When given array form and size larger than array, extend with identity tail
    p = Permutation([0,1,2], size=6)
    assert p._size == 6
    assert p._array_form == [0,1,2,3,4,5]

def test_repr_and_basic_new_compatibility():
    # Ensure that object is a Basic subclass and repr contains 'Permutation'
    p = Permutation([0,1])
    assert isinstance(p, Basic)
    r = repr(p)
    assert 'Permutation' in r