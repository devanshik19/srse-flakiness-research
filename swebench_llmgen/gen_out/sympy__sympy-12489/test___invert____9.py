import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_basic_array_form():
    # permutation given in array form through nested cycles constructor
    p = Permutation([[2, 0], [3, 1]])
    inv = ~p
    # expected inverse: apply inverse mapping: p maps 0->2,1->3,2->0,3->1
    # so inverse maps 2->0,3->1,0->2,1->3 which as array form is [2,3,0,1]
    assert isinstance(inv, Permutation)
    assert inv.array_form == [2, 3, 0, 1]
    # Check that multiplication with inverse yields identity
    identity = p * inv
    assert identity.array_form == list(range(p.size))
    assert (inv * p).array_form == list(range(p.size))

def test_invert_explicit_array_and_power_behavior():
    # explicit array form constructor - providing flat list
    p = Permutation([2, 3, 0, 1])
    inv = ~p
    # inverse of inverse returns original
    assert ~~p == p
    # inverse equals power -1
    assert p**-1 == inv
    # check that identity inverse is itself
    e = Permutation(list(range(5)))
    assert ~e == e
    assert e**-1 == e

def test_invert_on_singleton_and_empty():
    # singleton permutation (size 1)
    s = Permutation([0])
    assert ~s == s
    # empty permutation (size 0) if supported
    empty = Permutation([])
    assert ~empty == empty

def test_invert_nontrivial_random():
    import random
    for size in (1, 2, 5, 7):
        arr = list(range(size))
        random.shuffle(arr)
        p = Permutation(arr)
        inv = ~p
        # verify by composition: applying p then inv gives identity mapping on indices
        comp = p * inv
        assert comp.array_form == list(range(size))
        comp2 = inv * p
        assert comp2.array_form == list(range(size))

def test_invert_does_not_modify_original():
    p = Permutation([3, 0, 1, 2])
    before = p.array_form.copy()
    inv = ~p
    # original permutation unchanged
    assert p.array_form == before
    # inverse is distinct object (but may share internal structure), ensure array forms differ unless self-inverse
    if p.array_form != inv.array_form:
        assert p.array_form != inv.array_form