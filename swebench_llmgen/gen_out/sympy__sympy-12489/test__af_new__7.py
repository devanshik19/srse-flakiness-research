import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_basic_properties():
    # basic list -> Perm object
    a = [2, 1, 3, 0]
    p = Perm._af_new(a)
    # check type and underlying array form binding
    assert isinstance(p, Basic)
    assert isinstance(p, Perm)
    assert hasattr(p, "_array_form")
    assert p._array_form is a  # must be same list reference
    # size should match length
    assert p._size == len(a)
    # repr contains Array-form like content
    r = repr(p)
    assert "Permutation" in r
    # array_form() should return the same list when available
    # Some Perm implementations expose array_form method; call if present.
    if hasattr(p, "array_form"):
        af = p.array_form()
        assert af == a
        # ensure not a different mutated list
        assert af is a or af == a

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

def test_af_new_mutation_reflects():
    # ensure that modifying original list reflects inside Perm object
    a = [1, 0, 2]
    p = Perm._af_new(a)
    assert p._array_form[0] == 1
    a[0] = 5
    # since _array_form is the same object, change should be visible
    assert p._array_form[0] == 5

def test_af_new_not_copying_input():
    # create a list and create Perm; then verify identity and that we can
    # rely on reference semantics (no defensive copy)
    original = [3, 2, 1, 0]
    p = Perm._af_new(original)
    assert p._array_form is original
    # verify size remains consistent after mutation
    original.append(4)
    assert p._size == 4  # size captured at creation, should not auto-update
    # but array form reference reflects appended element
    assert p._array_form[-1] == 4

def test_af_new_invalid_types_do_not_break_contract():
    # while the method expects a list, test that passing other sequences
    # still binds and sets size accordingly (size is len(perm))
    tup = (2, 0, 1)
    p = Perm._af_new(list(tup))
    assert p._array_form == list(tup)
    assert p._size == 3

    # passing an empty tuple wrapped as list
    p2 = Perm._af_new([])
    assert p2._size == 0

# If Perm._af_new is intended as internal, ensure it exists and is callable
def test_af_new_callable_exists():
    assert hasattr(Perm, "_af_new")
    assert callable(getattr(Perm, "_af_new"))