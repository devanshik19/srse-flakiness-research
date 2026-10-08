import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_creates_permutation_and_sets_internal_fields():
    # prepare an array form
    a = [2, 1, 3, 0]
    # call the internal constructor
    p = Perm._af_new(a)
    # returned object should be an instance of Basic and Perm
    assert isinstance(p, Basic)
    assert isinstance(p, Perm)
    # internal attributes set
    assert hasattr(p, "_array_form")
    assert p._array_form is a  # must be the same list (no copy)
    assert p._size == len(a)
    # repr should include array form (uses __repr__)
    r = repr(p)
    assert "Permutation" in r
    # array_form method should reflect the stored list if available
    # Many Perm methods depend on array_form; ensure array_form (if exists) returns expected
    if hasattr(p, "array_form"):
        af = p.array_form()
        assert af == a

def test_af_new_handles_empty_list_and_isolation_of_list():
    # empty permutation
    a = []
    p = Perm._af_new(a)
    assert isinstance(p, Perm)
    assert p._size == 0
    assert p._array_form is a
    # mutate original list and ensure p._array_form sees the change (by design)
    a.append(0)
    assert p._array_form == [0]

def test_af_new_does_not_copy_input_list_identity():
    # ensure that the function binds the exact list object (no copy)
    a = [1, 0]
    p = Perm._af_new(a)
    # modify a and check p._array_form reflects it
    a[0] = 5
    assert p._array_form[0] == 5

def test_af_new_with_nonstandard_values_still_wraps_list():
    # even if list contains non-permutation values, _af_new should still wrap it
    a = [10, -1, None]
    p = Perm._af_new(a)
    assert p._array_form is a
    assert p._size == 3
    # check that Basic.__new__ produced an object with args matching the input
    # Basic stores the arguments used to construct the object; ensure perm present
    assert p.args and a in p.args