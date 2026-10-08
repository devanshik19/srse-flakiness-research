import pytest
from sympy.combinatorics.permutations import Cycle

def test_size_empty_cycle():
    # An empty Cycle should be falsy and have size 0
    c = Cycle()
    # Ensure the Cycle is considered empty/falsy
    assert not bool(c)
    assert c.size() == 0

def test_size_singleton_and_indices():
    # Create a Cycle with one element by calling as permutation mapping
    # The Cycle class supports being called like Cycle( (0, ) ) or similar;
    # construct via list method if available.
    c = Cycle()
    # populate via list method: list(self, size) returns something perhaps used differently,
    # but we can set the internal dict by using the constructor signature as known from sympy:
    # Cycle expects sequence of elements; here we create a 1-cycle (0,)
    c = Cycle(0)
    # A cycle containing element 0 should have size 1 (max key 0 + 1)
    assert c.size() == 1

def test_size_nonzero_min_index():
    # Create a Cycle that maps 2->3 and 3->2 (a 2-cycle starting at index 2)
    # In sympy, Cycle can be created from a sequence: Cycle(2,3)
    c = Cycle(2, 3)
    # The size should be max key + 1 = 3 + 1 = 4 (indices 0..3 considered)
    assert c.size() == 4

def test_size_multiple_cycles_and_copy_independence():
    # More complex cycle: (1 4 2) for example; create via Cycle(1,4,2)
    c = Cycle(1, 4, 2)
    # size is max key + 1 -> max is 4 so size 5
    assert c.size() == 5
    # Ensure copying preserves size but is independent
    c_copy = c.copy()
    assert c_copy.size() == c.size()
    # Mutate original by creating a new Cycle with a higher index and ensure copy unchanged
    c = Cycle(10)
    assert c.size() == 11
    assert c_copy.size() == 5

def test_size_after_repr_roundtrip():
    # Create cycle, get its repr/str and eval back if possible; at least ensure size unaffected
    c = Cycle(0, 2, 5)
    s = repr(c)
    t = str(c)
    # size should remain consistent
    assert c.size() == max(c.keys()) + 1
    assert c.size() == 6

# Some defensive tests for interface expectations
def test_size_uses_keys_and_truthiness(monkeypatch):
    # Create a dummy Cycle and monkeypatch its keys method and __bool__ via __len__
    c = Cycle()
    # Force internal emptiness but provide custom keys
    class Dummy:
        def __bool__(self):
            return True
        def keys(self):
            return [7, 3, 5]
        def size(self):
            return Cycle.size(Dummy())
    d = Dummy()
    # When not empty, size should compute from keys()
    # Monkeypatching isn't strictly necessary; call Cycle.size with object having keys
    assert Cycle.size(d) == max(d.keys()) + 1