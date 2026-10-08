import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Permutation as PermutationAlias  # just in case
from sympy.combinatorics.permutations import Cycle
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Basic)
    assert p._array_form == []
    assert p._size == 0
    assert repr(p).startswith("Permutation")

def test_new_integer_creates_identity():
    p = Permutation(3)
    # identity on 0..3
    assert p._array_form == [0,1,2,3]
    assert p._size == 4

def test_new_array_form_preserved_and_missing_zero_error():
    # valid array form with zero present
    p = Permutation([0,2,1])
    assert p._array_form == [0,2,1]
    assert p._size == 3

    # missing 0 should raise
    with pytest.raises(ValueError):
        Permutation([2,1])

def test_new_repeated_elements_error():
    with pytest.raises(ValueError):
        Permutation([0,1,1,2])

def test_new_cycle_form_converted_to_array_and_size_extension():
    # cycles given as list of lists
    p = Permutation([[4,5,6],[0,1]])
    # array form should have entries 0..6
    assert p._array_form == [1,0,2,3,5,6,4]
    assert p._size == 7

    # providing explicit size larger than max fills singletons
    p2 = Permutation([[1,4],[3,5,2]], size=10)
    assert p2._size == 10
    # array form extended to size 10 with fixed points at end
    assert p2._array_form[6:] == [6,7,8,9]
    assert p2._array_form[:6] == [0,4,3,5,1,2]

def test_new_cycle_singleton_size_increases():
    # cycle notation with singleton indicating size
    p = Permutation([[19],[4,5,6],[0,1]])
    assert p._size == 20
    # underlying array form should be same as earlier example for those elements
    assert p._array_form[:7] == [1,0,2,3,5,6,4]

def test_new_accepts_cycle_object_and_permutation_object_and_size_adjust():
    c = Cycle(0,1,2)
    # Cycle -> converted to array form
    p_from_cycle = Permutation(c)
    assert isinstance(p_from_cycle, Permutation)
    # Permutation passed back unchanged if size matches
    p = Permutation([0,1,2])
    p2 = Permutation(p)
    assert p2 is p
    # but if size differs, a new Permutation is returned with adjusted size
    p3 = Permutation(p, size=5)
    assert p3 is not p
    assert p3._size == 5
    assert p3._array_form[:3] == [0,1,2]
    assert p3._array_form[3:] == [3,4]

def test_new_non_sequence_argument_interpreted_as_integer():
    # passing a non-sequence like object (int) should create identity
    p = Permutation(0)
    assert p._array_form == [0]
    assert p._size == 1

def test_new_invalid_argument_types_raise():
    # a nested mix of sequence and non-sequence triggers ValueError
    with pytest.raises(ValueError):
        # has_variety true: mixture of sequences and ints
        Permutation([ [0,1], 2 ])

def test_new_cycle_with_duplicates_in_cycle_ok_but_array_form_no_dups():
    # duplicates in cycle definition should produce repeated elements which is invalid
    with pytest.raises(ValueError):
        Permutation([[0,1,1]])

def test_new_size_extension_with_array_form_preserves_points():
    p = Permutation([0,1,2], size=6)
    assert p._size == 6
    assert p._array_form == [0,1,2,3,4,5]

# run pytest when executed directly (convenience)
if __name__ == "__main__":
    pytest.main([__file__])