import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_creates_permutation_and_sets_internal_fields():
    # Create a simple array form
    a = [2, 1, 3, 0]
    # Use the internal constructor
    p = Perm._af_new(a)

    # Check type and representation basics
    assert isinstance(p, Perm)
    # The Basic parent class is used in creation; ensure the instance is a Basic
    assert isinstance(p, Basic)

    # The array form should be stored as-is (no copy)
    # Modifying original list should reflect in the object's _array_form
    assert p._array_form is a
    assert p._array_form == [2, 1, 3, 0]

    # Size should be set correctly
    assert p._size == 4
    # public size method should agree if available
    if hasattr(p, 'size'):
        assert p.size() == 4

    # The object should be reproducible via repr containing "Permutation"
    r = repr(p)
    assert "Permutation" in r

def test_af_new_with_empty_list():
    a = []
    p = Perm._af_new(a)
    assert isinstance(p, Perm)
    assert p._array_form is a
    assert p._size == 0
    # size() if present should return 0
    if hasattr(p, 'size'):
        assert p.size() == 0

def test_af_new_with_singleton_and_mutation_effects():
    a = [0]
    p = Perm._af_new(a)
    assert p._array_form == [0]
    # mutate original list and ensure internal array_form sees the change (intent from docstring)
    a[0] = 5
    assert p._array_form[0] == 5
    # size should reflect length (still 1)
    assert p._size == 1

def test_af_new_input_types_and_errors():
    # Non-sequence input (e.g. integer) should still be stored but size derived via len will raise
    with pytest.raises(TypeError):
        # Passing an int will cause len(perm) inside _af_new to raise TypeError
        Perm._af_new(123)

    # Passing a tuple should work (tuple is a sequence)
    t = (1, 0)
    p = Perm._af_new(list(t))  # convert to list because docstring expects list bound
    assert p._array_form == [1, 0]
    assert p._size == 2