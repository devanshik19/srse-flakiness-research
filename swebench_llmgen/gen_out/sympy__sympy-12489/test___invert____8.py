import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_identity_and_inverse_property():
    # identity permutation of size 4
    p = Permutation([0, 1, 2, 3])
    inv = ~p
    # inverse of identity is identity
    assert inv == p
    # multiplication with inverse yields identity
    assert p * inv == Permutation([0, 1, 2, 3])
    assert inv * p == Permutation([0, 1, 2, 3])

def test_invert_from_array_of_cycles_and_array_form():
    # construct via cycles given in array-of-cycles form as in docstring example
    p = Permutation([[2, 0], [3, 1]])
    # array form should be [2,3,0,1]
    assert p.array_form == [2, 3, 0, 1]
    inv = ~p
    # inverse array form should map 2->0,3->1,0->2,1->3 => [2,3,0,1] inverse is [2,3,0,1] (self-inverse here)
    assert inv.array_form == [2, 3, 0, 1]
    # check that power -1 equals bitwise invert
    assert inv == p**-1
    # composition both ways yields identity
    assert p * inv == Permutation(list(range(p.size)))
    assert inv * p == Permutation(list(range(p.size)))

def test_invert_nontrivial_and_not_self_inverse():
    # a 3-cycle is not self-inverse
    p = Permutation([[1, 2, 0]])  # this is array form [1,2,0]
    assert p.array_form == [1, 2, 0]
    inv = ~p
    # inverse of [1,2,0] should be [2,0,1]
    assert inv.array_form == [2, 0, 1]
    # composition yields identity
    assert p * inv == Permutation([0, 1, 2])
    assert inv * p == Permutation([0, 1, 2])
    # ensure equality with exponent -1
    assert inv == p**-1

def test_invert_consistent_with_cycles_and_full_cyclic_form():
    # create permutation with two cycles of different lengths
    p = Permutation([[1, 3, 4], [2, 0]])
    inv = ~p
    # check that cycle structure length matches
    cs = p.cycle_structure
    cs_inv = inv.cycle_structure
    assert sorted(cs) == sorted(cs_inv)
    # invert twice yields original
    assert ~~p == p

def test_invert_raises_no_exceptions_for_various_sizes():
    # test small sizes including singleton and empty-like representations
    p0 = Permutation([])  # empty permutation interpreted as size 0
    assert (~p0).array_form == []
    p1 = Permutation([0])
    assert (~p1).array_form == [0]
    p2 = Permutation([1,0])
    assert (~p2).array_form == [1,0]
    # random permutation of size 5: inverse composition check
    p3 = Permutation([2,4,1,0,3])
    inv3 = ~p3
    assert p3 * inv3 == Permutation(list(range(p3.size)))
    assert inv3 * p3 == Permutation(list(range(p3.size)))