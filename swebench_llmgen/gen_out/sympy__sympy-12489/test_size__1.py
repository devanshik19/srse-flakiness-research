import pytest
from sympy.combinatorics.permutations import Cycle

def test_size_empty_cycle():
    # An empty Cycle should evaluate to False and size() -> 0
    c = Cycle()
    # Ensure boolean of empty cycle is False
    assert not c
    assert c.size() == 0

def test_size_singleton_cycle():
    # A cycle with one element (0) should have size 1
    c = Cycle(0)
    assert c.size() == 1

def test_size_nonzero_elements():
    # A cycle created with element 3 should size to max key + 1 = 4
    c = Cycle(3)
    assert c.size() == 4

def test_size_multiple_elements():
    # Create a cycle with multiple elements; ensure size is max + 1
    c = Cycle(1, 5, 2)
    assert c.size() == 6  # max is 5 -> 5 + 1 = 6

def test_size_after_copy_and_mutation():
    # Ensure copy preserves size and that original and copy are independent
    c = Cycle(2, 4)
    c_copy = c.copy()
    assert c.size() == c_copy.size() == 5
    # mutating the copy via list() should not affect original's size
    lst = c_copy.list(5)
    # list(...) returns mapping or sequence; ensure size unchanged
    assert c.size() == 5
    assert c_copy.size() == 5

def test_size_with_call_and_iter_and_repr_str_consistency():
    # Ensure methods that may be used elsewhere do not alter size
    c = Cycle(0, 2, 4)
    before = c.size()
    # __call__ may return mapping; just call to ensure no side-effects
    _ = c(6)
    # iterate over cycle
    _ = list(iter(c))
    # string representations should not change size
    _ = repr(c)
    _ = str(c)
    assert c.size() == before

def test_size_edge_cases_large_index():
    # Very large index should produce correct size without overflow
    large = 1000
    c = Cycle(large)
    assert c.size() == large + 1

# Run tests if executed as a script
if __name__ == "__main__":
    pytest.main([__file__])