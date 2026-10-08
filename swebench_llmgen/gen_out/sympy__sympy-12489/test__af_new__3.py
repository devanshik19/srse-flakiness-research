import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_creates_permutation_and_sets_internal_fields():
    # basic array form
    a = [2, 1, 3, 0]
    p = Perm._af_new(a)

    # p should be an instance of Basic subclass (Permutation)
    assert isinstance(p, Basic)
    assert isinstance(p, Perm)

    # _array_form must be the exact list object passed (no copy)
    assert p._array_form is a
    assert p._array_form == [2, 1, 3, 0]

    # size must match length of list
    assert p._size == 4
    assert p.size() == 4

    # __repr__ should reflect array form (repr may vary but must include array_form)
    r = repr(p)
    assert "Permutation" in r
    assert "2" in r and "1" in r and "3" in r and "0" in r

def test_af_new_with_empty_and_singleton():
    # empty permutation
    a_empty = []
    p_empty = Perm._af_new(a_empty)
    assert p_empty._array_form is a_empty
    assert p_empty._size == 0
    assert p_empty.size() == 0

    # singleton permutation
    a_one = [0]
    p_one = Perm._af_new(a_one)
    assert p_one._array_form is a_one
    assert p_one._size == 1
    assert p_one.size() == 1

def test_af_new_with_mutation_of_original_list_reflects_in_object():
    a = [1, 0, 2]
    p = Perm._af_new(a)
    # mutate original list and ensure p._array_form sees the change (intentional internal binding)
    a[0] = 42
    assert p._array_form[0] == 42
    # restore for further checks
    a[0] = 1
    assert p._array_form == [1,0,2]

def test_af_new_is_internal_only_behavior():
    # Confirm that creating via _af_new bypasses validation that might occur in __new__
    # For example, provide values that are out of typical permutation range but ensure object is still created
    bad = [10, -1, 5]
    p_bad = Perm._af_new(bad)
    assert p_bad._array_form is bad
    assert p_bad._size == 3
    # Accessing some methods that rely on proper permutation may raise, but construction must succeed
    # Ensure that array_form() returns the same list
    assert p_bad.array_form() == bad