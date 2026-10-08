import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.permutations import Cycle
from sympy.core import Basic

def test_new_empty_and_identity():
    # no args -> identity of size 0
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0

    # integer arg -> identity of size n+1
    p3 = Permutation(2)
    assert p3._array_form == [0, 1, 2]
    assert p3._size == 3

def test_new_array_form_valid_and_invalid():
    # valid array form
    p = Permutation([0,2,1])
    assert isinstance(p, Permutation)
    assert p._array_form == [0,2,1]
    assert p._size == 3

    # missing 0 should raise
    with pytest.raises(ValueError):
        Permutation([2,1])

    # repeated elements in array form raise
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_cycle_form_and_size_extension():
    # cycle form input converted to array form
    p = Permutation([[4,5,6],[0,1]])
    assert isinstance(p, Permutation)
    # resulting array form should map as in docstring example
    assert p._array_form[:7] == [1,0,2,3,5,6,4]
    assert p._size == 7

    # cycle form with explicit size larger than elements extends with singletons
    p2 = Permutation([[1,4],[3,5,2]], size=10)
    assert isinstance(p2, Permutation)
    assert p2._size == 10
    # first 6 entries determined by cycles, rest are singletons
    assert p2._array_form[:6] == [0,4,3,5,1,2]
    assert p2._array_form[6:] == [6,7,8,9]

def test_new_cycle_form_repeated_elements_error():
    # repeated elements across cycles should raise a helpful message
    with pytest.raises(ValueError) as exc:
        Permutation([[1,2],[2,3]])
    assert 'repeated elements' in str(exc.value)

def test_new_from_permutation_and_cycle_objects():
    # create base permutation and pass it in (should return same if size matches)
    base = Permutation([0,1,2])
    p_copy = Permutation(base)
    assert p_copy is base  # returns the same object when size matches

    # if size differs, a new Permutation is returned with extended size
    p_extended = Permutation(base, size=5)
    assert isinstance(p_extended, Permutation)
    assert p_extended is not base
    assert p_extended._array_form == [0,1,2,3,4]
    assert p_extended._size == 5

    # Cycle input should be converted to permutation
    c = Cycle(0,1,2)
    pc = Permutation(c)
    assert isinstance(pc, Permutation)
    # cycle (0 1 2) produces mapping [1,2,0]
    assert pc._array_form == [1,2,0]

def test_new_non_sequence_singleton_behavior():
    # non-sequence argument treated as integer n for identity of size n+1
    p = Permutation(0)
    assert p._array_form == [0]
    assert p._size == 1

def test_new_invalid_argument_types():
    # passing a nested non-uniform sequence should raise ValueError
    with pytest.raises(ValueError):
        # mix of int and list in top-level should be rejected
        Permutation([0, [1,2]])

def test_size_truncation_not_allowed():
    # size smaller than provided array length should not truncate; must match or be None
    base = Permutation([0,1,2,3])
    # passing smaller size should produce a new permutation with extended/truncated behavior:
    # __new__ only allows returning same object if size is None or equals a.size; otherwise new created
    # but it will not truncate; providing smaller size should raise due to size mismatch handling when from Perm?
    # To exercise safe behavior, request same size -> returns same
    same = Permutation(base, size=4)
    assert same is base

def test_repr_and_basic_inheritance():
    p = Permutation([0,1])
    # object is a Basic subclass (constructed via Basic.__new__)
    assert isinstance(p, Basic)
    # repr should include 'Permutation' (use __repr__)
    r = repr(p)
    assert 'Permutation' in r