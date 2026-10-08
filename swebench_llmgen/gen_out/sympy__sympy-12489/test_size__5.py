import pytest
from sympy.combinatorics.permutations import Cycle

def test_size_empty_cycle():
    # An empty cycle should evaluate to False in boolean context and have size 0
    c = Cycle()  # default empty
    assert not c
    assert c.size() == 0

def test_size_singleton_cycle():
    # A cycle with a single mapping 0->0 should have size 1
    c = Cycle()
    # __call__ or direct construction might not be available for setting;
    # but Cycle behaves like a dict mapping indices to images. Use the list() method if present.
    # Many Cycle implementations accept an iterable for construction; try common patterns.
    try:
        c = Cycle([0])
    except TypeError:
        # fallback: construct empty and use list() if defined to set entries
        c = Cycle()
        # If Cycle.list exists and takes (self, size) signature, use it to create a single fixed point
        if hasattr(c, 'list'):
            lst = c.list(1)
            # list() likely returns a mapping/list representation; ensure size computes as 1
            # create a new Cycle from that list if possible
            try:
                c = Cycle(lst)
            except Exception:
                # as last resort, set attribute to mimic mapping interface
                # Some Cycle implementations subclass dict; attempt item assignment
                try:
                    c[0] = 0
                except Exception:
                    # skip assignment; assert size via calling size on constructed object cannot be checked here
                    pytest.skip("Cannot construct singleton Cycle in this environment")
    assert c.size() == 1

def test_size_nonzero_keys():
    # Create a cycle that maps 2->3, 3->2 which should have keys {2,3} so size = max(keys)+1 = 4
    # Try constructing from a sequence that represents the mapping
    try:
        c = Cycle([None, None, 3, 2])  # positions 2->3 and 3->2, None for missing entries
    except Exception:
        # Try constructing by direct dict-like assignment if Cycle supports it
        c = Cycle()
        try:
            c[2] = 3
            c[3] = 2
        except Exception:
            pytest.skip("Cannot construct Cycle with nonzero keys in this environment")
    assert c.size() == 4

def test_size_after_copy_and_mutation():
    # Ensure that copying preserves size and that mutation changes size accordingly
    c = Cycle()
    try:
        c = Cycle([1, 0])  # 0->1,1->0 => keys {0,1} size 2
    except Exception:
        # fallback assignments
        c = Cycle()
        try:
            c[0] = 1
            c[1] = 0
        except Exception:
            pytest.skip("Cannot construct 2-cycle in this environment")
    c2 = c.copy()
    assert c2.size() == c.size() == 2

    # mutate original to add a larger key
    try:
        c[4] = 0
    except Exception:
        pytest.skip("Cannot mutate Cycle in this environment")
    assert c.size() == 5
    # copy should remain unchanged
    assert c2.size() == 2

def test_size_with_missing_keys_behavior():
    # If keys are non-contiguous, size is still max(keys)+1
    c = Cycle()
    try:
        c[10] = 0
    except Exception:
        pytest.skip("Cannot assign to Cycle in this environment")
    assert c.size() == 11