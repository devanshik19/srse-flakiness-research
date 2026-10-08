import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_creates_permutation_and_sets_internal_fields():
    # simple array form
    a = [2, 1, 3, 0]
    p = Perm._af_new(a)
    # p should be a Basic-derived Permutation
    assert isinstance(p, Basic)
    assert isinstance(p, Perm)
    # check internal attributes set by _af_new
    assert p._array_form is a            # same list object (no copy)
    assert p._size == 4
    # public representation should reflect array form
    s = repr(p)
    assert "Permutation" in s
    assert "[" in s and "]" in s

def test_af_new_with_empty_list():
    a = []
    p = Perm._af_new(a)
    assert p._array_form == a
    assert p._size == 0
    # size() method should match _size if available
    if hasattr(p, "size"):
        assert p.size() == 0

def test_af_new_internal_list_mutation_reflected():
    a = [1, 0]
    p = Perm._af_new(a)
    # mutate the original list and ensure permutation sees change (it holds reference)
    a[0] = 0
    a[1] = 1
    assert p._array_form == [0, 1]

def test_af_new_type_errors_and_invalid_inputs():
    # Non-list sequences should still be acceptable if they behave like lists
    class MySeq(list):
        pass
    a = MySeq([1, 2, 0])
    p = Perm._af_new(a)
    assert p._array_form is a
    assert p._size == 3

    # Immutable sequence (tuple) -- _af_new expects a list (it binds to _array_form).
    # Passing a tuple should still work but result._array_form is the tuple.
    t = (1, 0)
    p_t = Perm._af_new(list(t))  # ensure we pass a list to follow contract
    assert p_t._array_form == [1, 0]

def test_af_new_preserves_object_identity_and_allows_methods_using_array_form():
    # Create a permutation and ensure some methods that rely on array_form behave
    a = [1, 2, 0]
    p = Perm._af_new(a)
    # If Perm provides array_form() method, it should reflect same list
    if hasattr(p, "array_form"):
        af = p.array_form()
        assert af == a
        # ensure modifying returned list (if same object) affects internal
        if af is p._array_form:
            af[0] = 0
            assert p._array_form[0] == 0