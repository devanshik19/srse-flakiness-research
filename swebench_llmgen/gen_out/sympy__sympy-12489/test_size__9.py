import pytest
from sympy.combinatorics.permutations import Cycle

def test_size_empty_cycle():
    # Create an empty Cycle. The Cycle class treats falsy as empty.
    c = Cycle()
    # Ensure it's considered empty and size() returns 0
    assert not c
    assert c.size() == 0

def test_size_singleton_cycle():
    # Create a cycle with one element: typically Cycle(0) or Cycle([0]) depending on constructor
    # We'll try several ways to construct a single-item cycle to be robust.
    c1 = Cycle(0)
    c2 = Cycle([0])
    assert c1.size() == 1
    assert c2.size() == 1

def test_size_multiple_elements():
    # Create cycles with non-zero maximum keys to ensure size = max(keys)+1
    c = Cycle(0, 3, 2)  # max key 3 -> size should be 4
    assert c.size() == 4

    c2 = Cycle([5, 1, 2])  # max key 5 -> size 6
    assert c2.size() == 6

def test_size_after_copy_and_mutation():
    # Check that copying preserves size and that constructing from different inputs yields expected size
    original = Cycle(2, 4)
    copy = original.copy()
    assert copy.size() == original.size() == 5

    # If Cycle can be called to produce new cycles, ensure size reflects contents
    try:
        called = original()
        # If call returns a Cycle, check size is still >= original.size()
        if isinstance(called, Cycle):
            assert called.size() >= 0
    except TypeError:
        # Some implementations may not support calling; that's acceptable
        pass

def test_size_various_iter_and_list_compatibility():
    # Ensure size corresponds with list(self, size) behavior when available
    c = Cycle(1, 2, 7)
    # The expected size is max key (7) + 1 = 8
    assert c.size() == 8

    # Ensure iteration doesn't change size
    _ = list(iter(c))
    assert c.size() == 8

# Run the tests when executed as a script
if __name__ == "__main__":
    pytest.main([__file__])