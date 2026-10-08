import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_basic_array_binding_and_size():
    # simple permutation array
    a = [2, 1, 3, 0]
    p = Perm._af_new(a)
    # The returned object should be an instance of Basic and Perm
    assert isinstance(p, Basic)
    assert isinstance(p, Perm)
    # The internal _array_form must be exactly the same list object (bound, not copied)
    assert p._array_form is a
    # Size should be set to length of list
    assert p._size == 4
    # The repr should include the list representation (calls __repr__)
    r = repr(p)
    assert "Permutation" in r
    assert "[2, 1, 3, 0]" in r

def test_af_new_with_empty_and_singleton():
    # empty permutation
    a0 = []
    p0 = Perm._af_new(a0)
    assert p0._array_form is a0
    assert p0._size == 0

    # singleton permutation
    a1 = [0]
    p1 = Perm._af_new(a1)
    assert p1._array_form is a1
    assert p1._size == 1

def test_af_new_mutation_reflects_in_object():
    # ensure that modifying the original list after creation affects the Perm object's _array_form
    a = [1, 0, 2]
    p = Perm._af_new(a)
    assert p._array_form == [1, 0, 2]
    # mutate original list
    a[0] = 2
    a.append(3)
    # object should see changes because it holds the same list reference
    assert p._array_form is a
    assert p._array_form[0] == 2
    assert p._size == 3  # _size was set at creation and should not change with list mutation

def test_af_new_type_contract():
    # Passing a tuple should still bind the attribute (but typical usage expects list)
    # The function as given will set _array_form to the provided sequence; confirm behavior.
    t = (1, 0)
    p = Perm._af_new(list(t))  # convert to list as the docstring expects a list
    assert isinstance(p._array_form, list)
    assert p._array_form == [1, 0]
    assert p._size == 2

def test_af_new_not_copying_identity():
    # Verify that two different lists produce different Perm objects with independent list identity
    a = [2, 0, 1]
    b = [2, 0, 1]
    p1 = Perm._af_new(a)
    p2 = Perm._af_new(b)
    assert p1._array_form is not p2._array_form
    assert p1._array_form == p2._array_form
    # Changing one list should not affect the other's _array_form reference
    a[0] = 99
    assert p1._array_form[0] == 99
    assert p2._array_form[0] == 2