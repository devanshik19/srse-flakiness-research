import pytest
from sympy.combinatorics.permutations import Permutation

# Helper to construct a permutation from array form using internal API:
# Permutation accepts list/tuple to create permutation in sympy
# We'll create permutations and then call mul_inv which returns a new Permutation.

def test_mul_inv_identity_behavior():
    # identity permutation of size 5
    id5 = Permutation(list(range(5)))
    # another permutation
    p = Permutation([2, 0, 4, 1, 3])
    # mul_inv does other * ~self, so if self is identity, result should be other
    res = id5.mul_inv(p)
    assert isinstance(res, Permutation)
    assert res.array_form == p.array_form

def test_mul_inv_self_inverse_relation():
    # create permutations a and b
    a = Permutation([1, 2, 0])  # cycle (0 1 2)
    b = Permutation([2, 1, 0])  # transposition of 0 and 2 plus fixed 1
    # mul_inv returns b * (~a)
    res = a.mul_inv(b)
    # compute expected manually: inverse of a then multiply on left by b
    ainv = ~a
    expected = b * ainv
    assert isinstance(res, Permutation)
    assert res.array_form == expected.array_form

def test_mul_inv_with_same_permutation():
    # when other == self, result should be self * ~self = identity
    p = Permutation([3, 0, 1, 2])
    res = p.mul_inv(p)
    # should be identity of same size
    assert res.is_Identity
    assert res.size == p.size
    assert res.array_form == list(range(p.size))

def test_mul_inv_various_sizes_and_edge_cases():
    # size 1 permutation
    a = Permutation([0])
    b = Permutation([0])
    assert a.mul_inv(b).array_form == [0]

    # size 2 permutations
    id2 = Permutation([0,1])
    swap = Permutation([1,0])
    # swap.mul_inv(id2) => id2 * ~swap = inverse(swap) = swap
    assert swap.mul_inv(id2).array_form == swap.array_form
    # id2.mul_inv(swap) => swap * ~id2 = swap
    assert id2.mul_inv(swap).array_form == swap.array_form

def test_mul_inv_does_not_mutate_operands():
    a = Permutation([1,0,2,3])
    b = Permutation([2,3,0,1])
    a_copy = Permutation(a.array_form[:])
    b_copy = Permutation(b.array_form[:])
    _ = a.mul_inv(b)
    # ensure originals unchanged
    assert a.array_form == a_copy.array_form
    assert b.array_form == b_copy.array_form

def test_mul_inv_composition_property():
    # Check (a.mul_inv(b)) * a == b
    # Since mul_inv returns b * ~a, multiplying on right by a yields b * ~a * a = b
    a = Permutation([2,0,1,4,3])
    b = Permutation([1,4,3,0,2])
    res = a.mul_inv(b)
    composed = res * a
    assert composed.array_form == b.array_form

# run tests when executed directly
if __name__ == "__main__":
    pytest.main([__file__])