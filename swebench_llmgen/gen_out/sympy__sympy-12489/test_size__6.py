import pytest

# Import the Cycle class from sympy combinatorics permutations module
from sympy.combinatorics.permutations import Cycle

def test_size_empty_cycle():
    # An empty Cycle should have falsy value and size 0
    c = Cycle()  # default empty
    assert not c  # ensures __bool__ or __len__ falsy
    assert c.size() == 0

def test_size_singleton_cycle():
    # Create a cycle of size 1: mapping 0->0
    # The Cycle initializer accepts a list of images (callable signature in module)
    c = Cycle([0])
    assert c.size() == 1
    # ensure iterating over keys works and max(keys)+1 equals 1
    # also ensure calling list() or copy doesn't change size
    assert c.copy().size() == 1
    assert list(c)  # iterator yields something for a non-empty cycle

def test_size_nonzero_based_keys():
    # Construct a Cycle whose underlying mapping might have keys not starting at 0.
    # For example mapping 2->0, 0->2, 1->1 would have keys {0,1,2} -> size 3.
    # Build via list where index is key and value is image.
    mapping = [2, 1, 0]
    c = Cycle(mapping)
    assert c.size() == 3

def test_size_sparse_indices():
    # If Cycle supports missing indices it should reflect max(key)+1
    # Build a cycle where max key is 5: e.g., indices 0..5 with some images
    mapping = [1, 0, 3, 2, 5, 4]
    c = Cycle(mapping)
    assert c.size() == 6

def test_size_after_mutation_via_list_constructor():
    # Ensure that list(self, size) or similar doesn't affect size() here.
    # Create a small cycle and confirm size remains consistent.
    c = Cycle([1, 2, 0])
    original_size = c.size()
    # If list method exists, ensure invoking it doesn't change size (no exception)
    if hasattr(c, 'list'):
        # some implementations require a size argument; try calling defensively
        try:
            _ = c.list(original_size)
        except TypeError:
            # if signature differs, just call without argument
            _ = c.list()
    assert c.size() == original_size

def test_size_on_copy_and_repr_str():
    c = Cycle([1, 0])
    assert c.copy().size() == c.size()
    # repr and str shouldn't affect size
    _ = repr(c)
    _ = str(c)
    assert c.size() == 2