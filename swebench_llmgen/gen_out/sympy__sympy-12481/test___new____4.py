import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle, Permutation as PermAlias
from sympy.combinatorics.permutations import Permutation as PermClass

def test_new_no_args_creates_empty():
    p = Permutation()
    assert p.array_form == []
    assert p.size == 0
    assert repr(p).startswith("Permutation")

def test_new_single_int_creates_identity():
    p = Permutation(3)
    # identity of length 4: [0,1,2,3]
    assert p.array_form == [0,1,2,3]
    assert p.size == 4

def test_new_array_form_valid():
    p = Permutation([0,2,1])
    assert p.array_form == [0,2,1]
    assert p.size == 3

def test_new_array_form_missing_zero_raises():
    with pytest.raises(ValueError):
        Permutation([2,1])

def test_new_array_form_duplicates_raises():
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_cycle_form_converts_to_array():
    # cycles: (4 5 6)(0 1) -> array form should place elements accordingly
    p = Permutation([[4,5,6],[0,1]])
    # expected array form as in docstring
    assert p.array_form == [1,0,2,3,5,6,4]
    assert p.size == 7

def test_new_cycle_with_size_extends():
    p = Permutation([[4,5,6],[0,1],[19]], size=20)
    assert p.size == 20
    # underlying array_form will be length 20
    assert len(p.array_form) == 20
    # positions beyond 6 should be fixed points
    assert p.array_form[7] == 7
    assert p.array_form[19] == 19

def test_new_cycle_duplicates_raise_specific_message():
    with pytest.raises(ValueError) as exc:
        Permutation([[1,2],[2,3]])
    assert 'repeated elements' in str(exc.value)

def test_new_from_permutation_returns_same_or_copy_with_size_adjust():
    p1 = Permutation([0,1,2,3])
    # passing same size should return the same object (or equal)
    p2 = Permutation(p1, size=4)
    assert p2 == p1
    # requesting different larger size returns adjusted permutation
    p3 = Permutation(p1, size=6)
    assert p3.size == 6
    assert p3.array_form[:4] == p1.array_form
    # extra positions are fixed
    assert p3.array_form[4] == 4
    assert p3.array_form[5] == 5

def test_new_from_cycle_object_and_singleton_cycle():
    # create Cycle via Cycle class: Cycle( (0,1) ) -> convert to permutation
    c = Cycle([0,1])
    p = Permutation(c)
    assert p.array_form[:2] == [1,0]

def test_new_invalid_argument_types_raise():
    # non-sequence unexpected type should be treated as single int handled above,
    # but passing nested mixed types should raise ValueError
    with pytest.raises(ValueError):
        Permutation([ [1,2], 3, [4] ])

def test_new_array_with_size_increases_length_but_keeps_elements():
    p = Permutation([0,2,1], size=5)
    assert p.size == 5
    # original mapping preserved in first 3 entries
    assert p.array_form[:3] == [0,2,1]
    # new positions are fixed points
    assert p.array_form[3] == 3
    assert p.array_form[4] == 4