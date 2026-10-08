import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_creates_permutation_and_binds_array_form():
    # basic usage: create from a list
    a = [2, 1, 3, 0]
    p = Perm._af_new(a)
    # p should be an instance of Basic (Perm extends Basic)
    assert isinstance(p, Basic)
    # and its array form should be the exact list (no copy)
    assert getattr(p, "_array_form") is a
    assert p._array_form == [2, 1, 3, 0]
    # size should be set correctly
    assert p._size == 4
    # repr should mention Permutation and show the array form
    r = repr(p)
    assert r.startswith("Permutation(")
    assert "2" in r and "1" in r and "3" in r and "0" in r

def test_af_new_with_empty_list():
    a = []
    p = Perm._af_new(a)
    assert p._array_form == []
    assert p._size == 0
    # operations expecting array_form length 0 should not raise here
    assert list(getattr(p, "_array_form")) == []

def test_af_new_preserves_mutation_on_original_list():
    a = [1, 0]
    p = Perm._af_new(a)
    # mutate original list and ensure the permutation sees the change
    a[0] = 5
    assert p._array_form[0] == 5

def test_af_new_type_errors_and_invalid_inputs():
    # although _af_new expects a list, passing other sequences should work similarly
    tup = (1, 0, 2)
    p = Perm._af_new(list(tup))
    assert p._array_form == [1, 0, 2]
    assert p._size == 3
    # passing non-sequence (e.g. integer) should raise when trying to get len()
    with pytest.raises(TypeError):
        Perm._af_new(123)  # integers have no len()

def test_multiple_calls_produce_distinct_objects():
    a1 = [0, 1]
    a2 = [1, 0]
    p1 = Perm._af_new(a1)
    p2 = Perm._af_new(a2)
    assert p1 is not p2
    assert p1._array_form is a1
    assert p2._array_form is a2
    assert p1._size == 2
    assert p2._size == 2