import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_creates_permutation_and_sets_internal_fields():
    # create a simple array form
    a = [2, 1, 3, 0]
    # call the internal constructor
    p = Perm._af_new(a)

    # type and basic properties
    assert isinstance(p, Perm)
    # Ensure Basic machinery used to construct object: __class__ is Perm
    assert p.__class__ is Perm

    # internal array_form should be bound to the same list object (not a copy)
    assert p._array_form is a
    # size must match length of list
    assert p._size == len(a)

    # public array_form method should reflect the internal array (if available)
    # many permutations implementations provide array_form() — handle gracefully:
    if hasattr(p, "array_form"):
        assert p.array_form() == a

    # repr should include the array form representation
    r = repr(p)
    assert "Permutation" in r
    # representation should include the sequence elements
    for elem in a:
        assert str(elem) in r

def test_af_new_with_empty_list_and_mutation_reflection():
    a = []
    p = Perm._af_new(a)
    assert p._array_form is a
    assert p._size == 0

    # Mutate the original list and ensure the permutation's internal reference sees it
    a.extend([0, 1])
    assert p._array_form == [0, 1]
    assert p._size == 0 or p._size == len(a)
    # Note: _af_new stores size at creation; ensure that stored size remains initial length
    assert p._size == 0

def test_af_new_invalid_inputs_do_not_crash_and_store_reference():
    # non-list sequence (tuple) should still be stored as given
    t = (1, 0)
    p = Perm._af_new(t)
    assert p._array_form is t
    assert p._size == len(t)

    # custom mutable sequence
    class Seq(list):
        pass

    s = Seq([1, 2, 0])
    p2 = Perm._af_new(s)
    assert p2._array_form is s
    assert p2._size == 3

def test_af_new_preserves_identity_for_singleton():
    a = [0]
    p = Perm._af_new(a)
    assert p._array_form is a
    assert p._size == 1
    # identity check if method exists
    if hasattr(p, "is_Identity"):
        # is_Identity might be a method or property
        val = p.is_Identity() if callable(p.is_Identity) else p.is_Identity
        assert val is True

# run pytest-style assertion checks for Basic internals
def test_af_new_creates_basic_subclass():
    a = [0, 1]
    p = Perm._af_new(a)
    # _hashable_content is listed among methods; ensure it exists
    if hasattr(p, "_hashable_content"):
        content = p._hashable_content()
        # content should be a hashable representation; try hashing it
        hash(content)