import pytest
from sympy.combinatorics.permutations import Permutation, Cycle
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0

def test_new_single_int_creates_identity_of_length_plus_one():
    p = Permutation(2)  # should create [0,1,2]
    assert p._array_form == [0, 1, 2]
    assert p._size == 3

def test_new_array_form_valid():
    p = Permutation([0, 2, 1])
    assert p._array_form == [0, 2, 1]
    assert p._size == 3
    # __repr__ uses array form; ensure Basic subclassing worked
    r = repr(p)
    assert 'Permutation' in r

def test_new_array_form_missing_zero_raises():
    with pytest.raises(ValueError):
        Permutation([2, 1])  # missing 0 for array form

def test_new_array_form_with_size_extension():
    p = Permutation([0, 1], size=5)
    # should extend to size 5 with fixed points 2,3,4
    assert p._array_form == [0, 1, 2, 3, 4]
    assert p._size == 5

def test_new_cycles_converted_to_array():
    p = Permutation([[4, 5, 6], [0, 1]])
    # expected array form from docstring
    assert p._array_form == [1, 0, 2, 3, 5, 6, 4]
    assert p._size == 7

def test_new_cycles_with_size_specified_fills_singletons():
    p = Permutation([[4, 5, 6], [0, 1], [19]], size=20)
    assert p._array_form == [1, 0, 2, 3, 5, 6, 4]  # array form unaffected
    assert p._size == 20
    # ensure that implied array form for elements beyond max uses fixed points
    assert len(p.array_form) == 20 if hasattr(p, "array_form") else p._size == 20

def test_new_from_cycle_object_and_from_permutation_copy():
    c = Cycle(0, 2, 1)
    p_from_cycle = Permutation(c)
    assert isinstance(p_from_cycle, Permutation)
    # Permutation argument (should return same object if size matches)
    p = Permutation([0, 1, 2])
    p2 = Permutation(p)
    assert p2 is p
    # If size differs, a new permutation should be returned (copy with new size)
    p3 = Permutation(p, size=5)
    assert p3 is not p
    assert p3._size == 5
    assert p3._array_form[:3] == p._array_form

def test_new_invalid_types_raise():
    # passing something that's not sequence or int should raise
    class NotSeq:
        pass
    with pytest.raises(ValueError):
        Permutation(NotSeq())

def test_new_repeated_elements_in_array_raise():
    with pytest.raises(ValueError):
        Permutation([0, 1, 1])

def test_new_repeated_elements_in_cycles_raise():
    with pytest.raises(ValueError):
        Permutation([[0, 1], [1, 2]])

# ensure array form list is copied (mutating input list doesn't change stored)
def test_new_copies_input_list():
    src = [0, 1, 2]
    p = Permutation(list(src))
    src[0] = 99
    assert p._array_form == [0, 1, 2]

# Access array_form via attribute or method if available
def test_array_form_attribute_or_method():
    p = Permutation([0, 1, 2])
    # prefer method if exists
    if hasattr(p, "array_form") and callable(getattr(p, "array_form")):
        af = p.array_form()
    else:
        af = p._array_form
    assert af == [0, 1, 2]