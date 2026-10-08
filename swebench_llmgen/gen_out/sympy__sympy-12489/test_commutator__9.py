import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic():
    # simple permutations where sizes equal
    p = Permutation([0, 2, 3, 1])  # mapping: 0->0,1->2,2->3,3->1
    x = Permutation([2, 0, 3, 1])
    c = p.commutator(x)
    # commutator should equal ~x * ~p * x * p
    assert c == (~x) * (~p) * x * p

    # verify that if two permutations commute, commutator is identity
    I = Permutation(3)  # identity on 3 points
    perms = [I + i for i in range(6)]  # create some permutations of different shifts
    for a in perms:
        for b in perms:
            c = a.commutator(b)
            if a * b == b * a:
                assert c == I
            else:
                assert c != I

def test_commutator_size_mismatch_raises():
    a = Permutation([1, 0, 2])  # size 3
    b = Permutation([1, 0, 2, 3])  # size 4
    with pytest.raises(ValueError):
        a.commutator(b)

def test_commutator_identity_cases():
    # commutator of identity with anything should be identity
    I4 = Permutation(4)
    p = Permutation([2, 3, 0, 1])
    assert I4.commutator(p) == I4
    assert p.commutator(I4) == I4

def test_commutator_involution_and_nontrivial():
    # Test with an involution and a 3-cycle to produce nontrivial commutator
    invol = Permutation([1, 0, 2, 3])  # swap 0 and 1
    three = Permutation([1, 2, 0, 3])  # 3-cycle on 0,1,2
    c = invol.commutator(three)
    # Check definition: c == ~three * ~invol * three * invol
    assert c == (~three) * (~invol) * three * invol
    # Should not be identity because they do not commute
    I4 = Permutation(4)
    assert c != I4