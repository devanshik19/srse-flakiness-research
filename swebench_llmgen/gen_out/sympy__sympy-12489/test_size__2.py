import pytest
from sympy.combinatorics.permutations import Cycle

def test_size_empty_cycle():
    # Create an empty Cycle: Cycle() should represent no mapping
    c = Cycle()
    # The size of an empty cycle should be 0
    assert bool(c) is False  # ensure falsy as size uses "if not self"
    assert c.size() == 0

def test_size_singleton_cycle():
    # Create a cycle with a single element mapping 0->0
    c = Cycle(0)
    # For a single element cycle, keys() should be {0} so max(keys)+1 == 1
    assert bool(c) is True
    assert c.size() == 1

def test_size_nonzero_based_cycle():
    # Create a cycle that includes elements up to 3 (e.g., 0->1->2->3->0)
    c = Cycle(0, 1, 2, 3)
    assert c.size() == 4

def test_size_with_missing_lower_indices():
    # Some Cycle constructors can accept arbitrary entries; create one that
    # has entries not starting at 0 (e.g., 2->3->2). Cycle should compute size
    # as max(keys)+1 which will reflect the highest index used.
    c = Cycle(2, 3)
    # Even if 0 and 1 are not present as keys, size should be max(keys)+1 = 3+1=4
    assert c.size() == 4

def test_size_after_copy_and_mutation():
    # Ensure that copy preserves size and that modifying original affects size
    c = Cycle(0, 1, 2)
    cp = c.copy()
    assert cp.size() == c.size() == 3
    # mutate original by creating a new cycle with larger index
    c2 = Cycle(0, 1, 2, 5)
    assert c2.size() == 6

def test_size_consistent_with_list_representation():
    # Use the list(size) method to check internal consistency if available
    c = Cycle(0, 2, 4)
    # size should be max key + 1 => keys are 0,2,4 -> max=4 -> size=5
    assert c.size() == 5
    lst = c.list(c.size())
    # The list representation length should match reported size
    assert len(lst) == c.size()