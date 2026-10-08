import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.core import Basic

def test_af_new_basic_array_form_and_size():
    # simple permutation array
    a = [2, 1, 3, 0]
    p = Perm._af_new(a)
    # check that returned object is an instance of Perm (Basic subclass)
    assert isinstance(p, Basic)
    assert isinstance(p, Perm)
    # internal attributes set correctly
    assert hasattr(p, "_array_form")
    assert p._array_form is a  # must hold reference to same list
    assert p._size == 4
    # representation contains the array form
    s = repr(p)
    assert "Permutation" in s
    assert "2" in s and "1" in s and "3" in s and "0" in s

def test_af_new_empty_list():
    # empty permutation
    a = []
    p = Perm._af_new(a)
    assert p._array_form is a
    assert p._size == 0
    # ensure methods that rely on size behave reasonably
    assert p.size() == 0

def test_af_new_mutation_of_original_list_reflected_in_object():
    # since array form is bound without copying, modifications to original list
    # should be visible via the permutation's _array_form attribute
    a = [1, 0, 2]
    p = Perm._af_new(a)
    assert p._array_form[0] == 1
    a[0] = 99
    assert p._array_form[0] == 99

def test_af_new_raises_on_non_sequence_input():
    # _af_new expects a sequence (list). Passing non-sequence types should still
    # create the object but size should reflect len() if supported or raise TypeError.
    class DummyNoLen:
        pass

    dummy = DummyNoLen()
    with pytest.raises(TypeError):
        # len(dummy) will raise, so _af_new should propagate that
        Perm._af_new(dummy)

def test_af_new_independence_of_cyclic_cached_fields():
    # ensure that cached cyclic forms (if any) are independent initially
    a = [0, 1, 2]
    p = Perm._af_new(a)
    # these optional cached attributes should not be set by _af_new
    assert getattr(p, "_cyclic_form", None) is None
    assert getattr(p, "_cycle_structure", None) is None
    # calling methods that compute them will set them; verify they compute consistently
    cyc = p.cyclic_form()
    assert isinstance(cyc, list)
    assert p._cyclic_form == cyc
    # cycle structure should be available after call
    cs = p.cycle_structure()
    assert isinstance(cs, tuple)
    assert p._cycle_structure == cs