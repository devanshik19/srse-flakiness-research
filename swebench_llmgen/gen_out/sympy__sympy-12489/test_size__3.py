import pytest
from sympy.combinatorics.permutations import Cycle

def test_size_empty_cycle():
    # Create an "empty" Cycle. Based on Cycle implementation, calling Cycle()
    # with no arguments should create an empty mapping/list-like object.
    c = Cycle()
    # The size of an empty cycle should be 0
    assert bool(c) is False  # ensure falsy empty
    assert c.size() == 0

def test_size_nonempty_cycle_single_element():
    # Create a cycle with a single element mapping 0->0
    c = Cycle(0)
    # Should be truthy and size == max(keys)+1 == 0+1 == 1
    assert bool(c) is True
    assert c.size() == 1

def test_size_nonempty_cycle_multiple_elements():
    # Create a cycle with elements 0->1->2->0 (Cycle can be constructed from iterable)
    c = Cycle(0, 1, 2)
    # keys are 0,1,2 so size is 3
    assert c.size() == 3

def test_size_non_contiguous_keys():
    # Construct cycle by providing mapping that results in non-contiguous keys.
    # Some Cycle implementations accept tuples of cycles; using a cycle of larger labels
    c = Cycle(2, 4, 3)
    # keys should include 2,4,3 so max is 4 -> size = 5
    assert c.size() == 5

def test_size_after_copy_and_mutation():
    c = Cycle(1, 0)  # keys 1,0 -> size 2
    assert c.size() == 2
    # copy should preserve size
    c2 = c.copy()
    assert c2.size() == 2
    # ensure original unaffected by operations on copy (if __call__ or list exist)
    # Attempt to get list representation and ensure size still the same
    lst = c.list(c.size())
    assert isinstance(lst, list)
    assert c.size() == 2