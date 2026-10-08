import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle  # Cycle used for some constructions
from sympy import Basic

def test_empty_constructor_and_size_kw():
    # No args => identity of size 0
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p.size == 0
    assert p.array_form == []

    # size kw provided
    p5 = Permutation(size=5)
    assert p5.size == 5
    assert p5.array_form == list(range(5))

def test_integer_constructor_identity():
    # single integer n -> identity permutation of length n+1
    p = Permutation(3)
    assert p.size == 4
    assert p.array_form == [0, 1, 2, 3]

def test_array_form_valid_and_missing_zero_error():
    # valid array form (contains 0..n-1)
    p = Permutation([0, 2, 1])
    assert p.array_form == [0, 2, 1]
    assert p.size == 3

    # missing zero or incomplete range should raise ValueError
    with pytest.raises(ValueError):
        Permutation([2, 1])  # elements should be 0..2

def test_repeated_elements_in_array_form():
    with pytest.raises(ValueError):
        Permutation([0, 1, 1])  # duplicate element not allowed

def test_cycle_form_conversion_and_size_extension():
    # cycle form given as list of lists
    p = Permutation([[4, 5, 6], [0, 1]])
    # expected array form from docstring example
    assert p.array_form == [1, 0, 2, 3, 5, 6, 4]
    assert p.size == 7

    # cycle form with explicit size larger than max element: should extend with singletons
    p20 = Permutation([[4, 5, 6], [0, 1], [19]], size=20)
    assert p20.size == 20
    # check that positions >=7 up to 19 are singletons (fixed points)
    assert p20.array_form[7:] == list(range(7, 20))

def test_cycle_argument_varieties_and_cycle_obj_and_permutation_obj_handling():
    # If passed a Cycle object, should convert to array form
    c = Cycle()(1, 2, 3)  # creates cycle (1 2 3)
    p = Permutation(c)
    assert isinstance(p, Permutation)
    # p should map 1->2, 2->3, 3->1 and 0->0
    af = p.array_form
    assert af[0] == 0 and af[1] == 2 and af[2] == 3 and af[3] == 1

    # Passing a Permutation instance should return it (or a copy if size differs)
    p_original = Permutation([0, 1, 2])
    p_same = Permutation(p_original)
    # When no size given and sizes equal, should return same object
    assert p_same is p_original

    # If size differs, a new Permutation should be created with extended size
    p_extended = Permutation(p_original, size=5)
    assert p_extended is not p_original
    assert p_extended.size == 5
    assert p_extended.array_form[:3] == [0, 1, 2]
    assert p_extended.array_form[3:] == [3, 4]

def test_non_sequence_singleton_behavior():
    # Non-sequence argument is treated as integer n => identity of length n+1
    p = Permutation(0)  # should produce [0]
    assert isinstance(p, Permutation)
    assert p.array_form == [0]
    assert p.size == 1

def test_bad_argument_types_raise_value_error():
    # list-of-mixed (non-homogeneous) sequences should raise ValueError
    # e.g., mixture of ints and lists => has_variety triggers error
    with pytest.raises(ValueError):
        Permutation([1, [2, 3]])

    # Passing something totally invalid like a dict should raise ValueError
    with pytest.raises(ValueError):
        Permutation({'a': 1})

def test_array_form_extension_with_size_kw():
    # array form shorter than given size should extend with fixed points
    p = Permutation([0, 2, 1], size=6)
    assert p.size == 6
    # original mapping preserved for first 3 elements
    assert p.array_form[:3] == [0, 2, 1]
    # extended tail should be identity points 3,4,5
    assert p.array_form[3:] == [3, 4, 5]