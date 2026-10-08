import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Permutation as PermutationClassAlias
from sympy.combinatorics.permutations import Cycle
from sympy.core import Basic

def test_new_empty_and_size():
    # no args -> empty permutation
    p = Permutation()
    assert isinstance(p, Basic)
    assert p.array_form == []
    assert p.size == 0

    # provide size via kwargs
    p5 = Permutation(size=5)
    assert p5.array_form == [0, 1, 2, 3, 4]
    assert p5.size == 5

def test_new_from_integer():
    # single integer gives identity of that size (0..n)
    p3 = Permutation(3)
    # for argument 3 returns list(range(4))
    assert p3.array_form == [0, 1, 2, 3]
    assert p3.size == 4

def test_new_from_array_form_valid_and_invalid():
    # valid array form must contain integers 0..n-1 without gaps
    p = Permutation([0, 2, 1])
    assert p.array_form == [0, 2, 1]
    assert p.size == 3

    # missing 0 should raise ValueError
    with pytest.raises(ValueError):
        Permutation([2, 1])

    # repeated elements in array form should raise ValueError
    with pytest.raises(ValueError):
        Permutation([0, 1, 1])

def test_new_from_cycle_form_and_size_extension():
    # cycle form: list of lists
    p = Permutation([[4, 5, 6], [0, 1]])
    # expected array form from docstring example
    assert p.array_form == [1, 0, 2, 3, 5, 6, 4]
    assert p.size == 7

    # cycle form with explicit size (adds singletons up to size)
    p20 = Permutation([[4, 5, 6], [0, 1], [19]], size=20)
    assert p20.array_form[:7] == [1, 0, 2, 3, 5, 6, 4]
    assert p20.size == 20
    # check that indices beyond max in cycles are identity-fixed
    assert p20.array_form[7] == 7
    assert p20.array_form[19] == 19

def test_new_from_cycle_notation_without_singletons_but_with_size():
    p = Permutation([[1, 4], [3, 5, 2]], size=10)
    assert p.size == 10
    # ensure array form extended with identities
    assert p.array_form[:6] == [0, 4, 3, 5, 1, 2]
    assert p.array_form[6:] == [6, 7, 8, 9]

def test_new_from_cycle_objects_and_permutation_instance():
    # From Cycle instance
    c = Cycle(0, 2, 1)
    p_from_cycle = Permutation(c)
    assert p_from_cycle.array_form == [2, 0, 1] or isinstance(p_from_cycle, Permutation)

    # From Permutation (return same if size matches)
    src = Permutation([0, 2, 1], size=3)
    returned = Permutation(src)
    # It may return the same object (optimization), but properties must match
    assert returned.array_form == [0, 2, 1]
    assert returned.size == 3

    # From Permutation with different size -> returns new permutation with extended identities
    src2 = Permutation([0, 2, 1])
    bigger = Permutation(src2, size=5)
    assert bigger.size == 5
    assert bigger.array_form == [0, 2, 1, 3, 4]

def test_invalid_argument_types_and_variety():
    # Passing nested sequences of mixed types should raise ValueError
    with pytest.raises(ValueError):
        Permutation([ [1,2], 3 ])

    # Passing something that's not sequence but not int should be coerced?
    # For example string is a sequence -> leads to invalid; ensure it errors.
    with pytest.raises(ValueError):
        Permutation("abc")

def test_array_form_extend_when_size_larger():
    p = Permutation([0, 1, 2], size=6)
    assert p.size == 6
    assert p.array_form == [0, 1, 2, 3, 4, 5]

def test_repr_and_type_properties():
    p = Permutation([0, 1])
    # repr should contain 'Permutation' (basic sanity)
    r = repr(p)
    assert 'Permutation' in r
    # ensure Basic subclass properties present
    assert hasattr(p, '_array_form')
    assert hasattr(p, '_size')