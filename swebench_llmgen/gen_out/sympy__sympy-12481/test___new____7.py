# test_permutation_new.py
from __future__ import print_function, division
import pytest

from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.permutations import Cycle
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0

def test_new_integer_arg_creates_identity():
    p = Permutation(3)  # should create identity on 0..3
    assert isinstance(p, Permutation)
    assert p._array_form == [0,1,2,3]
    assert p._size == 4

def test_new_array_form_valid():
    p = Permutation([0,2,1])
    assert p._array_form == [0,2,1]
    assert p._size == 3
    # repr should include the array form (uses __repr__), ensure no error
    r = repr(p)
    assert "Permutation" in r

def test_new_array_form_missing_zero_raises():
    with pytest.raises(ValueError):
        Permutation([2,1])  # missing 0 for array form

def test_new_array_form_with_size_extension():
    p = Permutation([0,1], size=4)
    # array form extended with singletons 2,3
    assert p._array_form == [0,1,2,3]
    assert p._size == 4

def test_new_cycle_form_converted_to_array():
    p = Permutation([[4,5,6],[0,1]])
    # expected array form as in docstring example
    assert p._array_form == [1,0,2,3,5,6,4]
    assert p._size == 7

def test_new_cycle_form_with_size_argument():
    p = Permutation([[4,5,6],[0,1],[19]], size=20)
    assert p._array_form == [1,0,2,3,5,6,4]  # cycles fill up to max element; size stored separately
    assert p._size == 20

def test_new_cycle_input_missing_singletons_but_size_provided():
    p = Permutation([[1,4],[3,5,2]], size=10)
    assert p._size == 10
    # array_form should be extended to include singletons up to size
    assert p._array_form[:6] == [0,4,3,5,1,2]
    assert p._array_form[6:] == [6,7,8,9]

def test_new_with_repeated_elements_in_array_raises():
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_with_repeated_elements_in_cycles_raises():
    with pytest.raises(ValueError):
        Permutation([[0,1],[1,2]])

def test_new_from_Permutation_returns_same_or_resized_copy():
    p = Permutation([0,1,2])
    # same size returns same object (per implementation returns the same instance)
    p2 = Permutation(p)
    assert p2 is p
    # different size returns a new Permutation with extended size
    p3 = Permutation(p, size=5)
    assert p3 is not p
    assert isinstance(p3, Permutation)
    assert p3._size == 5
    assert p3._array_form[:3] == [0,1,2]
    assert p3._array_form[3:] == [3,4]

def test_new_from_Cycle_object():
    c = Cycle(0,1,2)
    p = Permutation(c)
    # Cycle(0,1,2) should map to array form [1,2,0]
    assert isinstance(p, Permutation)
    assert p._array_form == [1,2,0]

def test_bad_argument_types_raise():
    # Passing an unsupported type like a dict should raise ValueError
    with pytest.raises(ValueError):
        Permutation({1:2})

def test_sequence_of_sequences_detected_as_cycles():
    # ensure that a list-of-lists is treated as cycle input
    p = Permutation([[2,3],[0,1]])
    assert isinstance(p, Permutation)
    # verify array form is a permutation of 0..3
    assert set(p._array_form) == {0,1,2,3}

def test_size_argument_cast_to_int_and_honored():
    p = Permutation([0,1], size=4.0)
    assert p._size == 4
    assert p._array_form == [0,1,2,3]

# Run these tests if the module is executed directly (useful for debugging)
if __name__ == "__main__":
    import pytest as _pytest
    _pytest.main([__file__])