import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle  # Cycle used internally by Permutation
from sympy.core import Basic

def test_new_empty_and_identity_and_single_int():
    # no args -> empty permutation
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0

    # single int -> identity of length a+1
    p2 = Permutation(2)
    assert p2._array_form == [0, 1, 2]
    assert p2._size == 3

def test_new_array_form_accepts_and_rejects():
    # valid array form with 0..n-1 present
    p = Permutation([0, 2, 1])
    assert p._array_form == [0, 2, 1]
    assert p._size == 3

    # missing 0 should raise (array form must contain 0..n-1)
    with pytest.raises(ValueError):
        Permutation([2, 1])

    # duplicated elements in array form should raise
    with pytest.raises(ValueError):
        Permutation([0, 1, 1])

def test_new_cycle_form_construction_and_size_arg():
    # cycle form: list of cycles -> should convert to array form
    p = Permutation([[4, 5, 6], [0, 1]])
    # expected array form determined by example in docstring
    assert p._array_form == [1, 0, 2, 3, 5, 6, 4]
    assert p._size == 7

    # cycle form with explicit size larger than max element -> extend with singletons
    p2 = Permutation([[1, 4], [3, 5, 2]], size=10)
    assert p2._size == 10
    # check that array form was extended to size 10 and matches example
    assert p2._array_form[:6] == [0, 4, 3, 5, 1, 2]
    assert p2._array_form[6:] == [6, 7, 8, 9]

def test_new_with_Permutation_argument_and_size_adjustment():
    p = Permutation([0,1,2,3])
    # passing a Permutation instance with same size returns the same object
    p_same = Permutation(p)
    assert p_same is p

    # passing a Permutation with different size returns a new Permutation with extended size
    p_big = Permutation(p, size=6)
    assert p_big is not p
    assert p_big._size == 6
    assert p_big._array_form[:4] == [0,1,2,3]
    assert p_big._array_form[4:] == [4,5]

def test_new_with_Cycle_argument_conversion():
    # create a Cycle object and pass it to Permutation
    c = Cycle(0,1,2)
    p = Permutation(c)
    # array form should correspond to cycle (0 1 2) -> [1,2,0]
    assert p._array_form[:3] == [1,2,0]
    assert p._size >= 3

def test_new_invalid_argument_types():
    # non-sequence non-int should raise via the not-is_sequence branch: use object
    class Dummy: pass
    with pytest.raises(ValueError):
        Permutation(Dummy())

    # list where elements are mixed sequences and ints should also raise
    with pytest.raises(ValueError):
        # has_variety check: elements not uniformly sequences or ints
        Permutation([ [0,1], 2 ])

def test_new_size_keyword_non_int_casting():
    # size provided as something convertible to int should be accepted
    p = Permutation([0,1], size=5.0)
    assert p._size == 5
    assert p._array_form == [0,1,2,3,4]

def test_new_array_form_extending_with_size_preserves_cycles():
    # ensure that increasing size doesn't truncate or split cycles; extension should append singletons
    base = Permutation([[0,1,2]])
    extended = Permutation(base.array_form, size=6)
    assert extended._size == 6
    # first 3 entries should be the 3-cycle mapping
    assert extended._array_form[0:3] == base._array_form[0:3]
    # appended entries are singletons
    assert extended._array_form[3:] == [3,4,5]

# Extra helper to access array_form property if exists, fallback to _array_form
def _get_array_form(obj):
    af = getattr(obj, "array_form", None)
    if callable(af):
        return af()
    return getattr(obj, "_array_form")

# ensure tests don't rely on a property that might be a method name clash
def test_array_form_accessor_consistent():
    p = Permutation([0,1,2])
    af = _get_array_form(p)
    assert af == [0,1,2]