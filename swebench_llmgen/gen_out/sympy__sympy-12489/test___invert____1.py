import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_simple_array_form():
    # simple explicit array form
    p = Permutation([2, 3, 0, 1])
    inv = ~p
    # inverse should satisfy p * inv = identity and inv * p = identity
    identity = Permutation(list(range(p.size())))
    assert p * inv == identity
    assert inv * p == identity
    # double inversion returns original
    assert ~(~p) == p

def test_invert_from_cycles_and_array_equivalence():
    # construct permutation from cycle notation via array form input
    p = Permutation([[2, 0], [3, 1]])
    inv = ~p
    # expected inverse computed manually: array_form of p is [2,3,0,1]
    # inverse should map 2->0, 3->1, 0->2, 1->3 => [2,3,0,1] inverted is [2,3,0,1]
    # in this particular example permutation is its own inverse
    assert inv.array_form == p.array_form
    assert inv == p**-1
    assert p * inv == Permutation([0,1,2,3])
    assert inv * p == Permutation([0,1,2,3])

def test_invert_identity_and_singleton():
    identity = Permutation(list(range(5)))
    assert ~identity == identity
    # singleton (size 1) permutation
    single = Permutation([0])
    assert ~single == single
    assert single * (~single) == single

def test_invert_nontrivial_cycle():
    # 3-cycle: (0 1 2) array form [1,2,0]
    p = Permutation([1,2,0])
    inv = ~p
    # inverse of (0 1 2) is (0 2 1) -> array [2,0,1]
    assert inv.array_form == [2,0,1]
    assert p * inv == Permutation([0,1,2])
    assert inv * p == Permutation([0,1,2])

def test_invert_raises_or_behaves_on_empty():
    # If Permutation supports empty, ensure invert works (size 0)
    empty = Permutation([])
    inv = ~empty
    assert inv == empty
    assert empty * inv == empty

def test_invert_preserves_size_and_support():
    p = Permutation([2,0,1,4,3])
    inv = ~p
    assert p.size() == inv.size()
    # support should be same set
    assert set(p.support()) == set(inv.support())

def test_invert_property_of_parity_and_order():
    p = Permutation([2,0,1,4,3])  # product of a 3-cycle and a transposition
    inv = ~p
    # parity of inverse equals parity of original
    assert p.is_even() == inv.is_even()
    assert p.is_odd() == inv.is_odd()
    # order should be preserved
    assert p.order() == inv.order()