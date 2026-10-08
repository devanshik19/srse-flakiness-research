import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic_noncommuting():
    Permutation.print_cyclic = False
    p = Permutation([0, 2, 3, 1])
    x = Permutation([2, 0, 3, 1])
    c = p.commutator(x)
    # check result equals ~x * ~p * x * p
    assert c == (~x) * (~p) * x * p
    # commutator should not be identity for these
    I = Permutation(4)  # identity of size 4
    assert c != I

def test_commutator_commuting_pairs_give_identity():
    # create several permutations including identity and shifts that commute
    I = Permutation(5)
    p0 = I
    p1 = Permutation([1,2,3,4,0])  # cycle (0 1 2 3 4)
    p2 = Permutation([2,3,4,0,1])  # p1^2, commutes with p1
    # commuting pairs
    assert p1.commutator(p2) == I
    assert p2.commutator(p1) == I
    # identity commutes with all
    for q in (p0, p1, p2):
        assert I.commutator(q) == I
        assert q.commutator(I) == I

def test_commutator_size_mismatch_raises():
    p = Permutation([0,1,2])
    q = Permutation([0,1,2,3])
    with pytest.raises(ValueError):
        p.commutator(q)

def test_commutator_all_pairs_in_small_group():
    # generate small group elements as powers of a 3-cycle and test commutator correctness
    # cycle (0 1 2) on size 3
    base = Permutation([1,2,0])
    I = Permutation(3)
    elements = [I, base, base**2]
    for a in elements:
        for b in elements:
            c = a.commutator(b)
            # if they commute commutator is identity else not
            if a*b == b*a:
                assert c == I
            else:
                assert c != I

def test_commutator_involution_and_swap():
    # Test with an involution and a transposition-like permutation
    a = Permutation([1,0,2,3])  # swap 0 and 1
    b = Permutation([0,2,1,3])  # swap 1 and 2
    # compute commutator both ways and verify definition
    c1 = a.commutator(b)
    c2 = (~b) * (~a) * b * a
    assert c1 == c2
    # They do not commute, so commutator should not be identity
    I = Permutation(4)
    assert c1 != I