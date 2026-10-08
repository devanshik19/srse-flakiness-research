# test_cycle_size.py
from __future__ import print_function, division
import pytest

# Import the Cycle class from sympy
from sympy.combinatorics.permutations import Cycle

def test_size_empty_cycle():
    # Create an empty cycle by calling Cycle() with no arguments
    c = Cycle()
    # The Cycle should be falsy (so "if not self" triggers) and size() == 0
    assert bool(c) is False
    assert c.size() == 0

def test_size_singleton_cycle():
    # Create a cycle with one element (0)
    c = Cycle(0)
    assert bool(c) is True
    # keys() will be {0} so max(keys)+1 == 1
    assert c.size() == 1

def test_size_nonzero_min_key():
    # Create a cycle that maps 2->3->2 (a 2-cycle starting at 2)
    # Constructed via Cycle(2,3)
    c = Cycle(2, 3)
    assert c.size() == 4  # max key is 3, so 3+1 == 4

def test_size_after_copy_and_mutation():
    c = Cycle(1, 4, 2)
    original_size = c.size()
    # Make a copy and ensure size preserved
    c_copy = c.copy()
    assert c_copy.size() == original_size
    # Ensure original remains unchanged
    assert c.size() == original_size

def test_size_with_iter_and_list_consistency():
    c = Cycle(0, 2, 1)
    # list(size) should produce a list representation; ensure size() is consistent
    lst = c.list(c.size())
    assert isinstance(lst, list)
    assert c.size() == max(c.keys()) + 1

def test_size_boundary_behaviour():
    # Large keys to ensure size returns max+1
    c = Cycle(10, 20, 5)
    assert c.size() == 21  # max key is 20 -> 21
    # Adding a mapping to highest index via __call__ if available should not error
    # but we test size invariance for original object
    assert c.size() == 21