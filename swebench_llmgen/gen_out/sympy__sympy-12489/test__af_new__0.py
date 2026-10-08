import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_basic_array_binding_and_size():
    # simple permutation list
    a = [2, 1, 3, 0]
    p = Perm._af_new(a)
    # instance type should be Basic subclass (Permutation uses Basic.__new__)
    assert isinstance(p, Basic)
    # _array_form should be exactly the same list object (no copy)
    assert p._array_form is a
    # size should match length of list
    assert p._size == 4
    # repr should include array form representation
    s = repr(p)
    assert "Permutation" in s
    # array_form method should return a list equal to the underlying list
    assert p.array_form() == a

def test_af_new_empty_and_mutation_effects():
    # empty permutation list should be supported
    a = []
    p = Perm._af_new(a)
    assert p._size == 0
    assert p._array_form is a
    assert p.array_form() == []

    # mutation of the original list should reflect in the permutation object
    a2 = [1, 0]
    p2 = Perm._af_new(a2)
    assert p2.array_form() == [1, 0]
    # mutate a2 and ensure p2 sees the change (binds same object)
    a2[0] = 0
    a2[1] = 1
    assert p2._array_form == [0, 1]
    assert p2.array_form() == [0, 1]

def test_af_new_non_integer_entries_and_size_consistency():
    # even if entries are non-standard (not validated here), _af_new should accept list
    a = ["a", None, 3.14]
    p = Perm._af_new(a)
    assert p._array_form is a
    assert p._size == 3
    assert p.array_form() == ["a", None, 3.14]

def test_af_new_immutable_behavior_on_returned_list():
    # array_form() should not necessarily return a copy; confirm it's the same object
    a = [2, 0, 1]
    p = Perm._af_new(a)
    returned = p.array_form()
    # If array_form returns the internal list (likely), mutations should reflect.
    # We accept either behavior but ensure consistency between _array_form and array_form()
    assert returned == p._array_form
    # Mutate returned (if mutable) and ensure _array_form matches
    returned[0] = 99
    assert p._array_form[0] == 99

def test_af_new_with_large_list_performance_attributes():
    # create a larger permutation list and ensure size is set correctly
    n = 100
    a = list(range(n))[::-1]
    p = Perm._af_new(a)
    assert p._size == n
    assert p._array_form is a
    # basic operations that rely on size should not raise
    assert p.size() == n
    # ensure repr works for larger one as well
    assert "Permutation" in repr(p)