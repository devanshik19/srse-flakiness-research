import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic():
    # simple small permutations that do not commute
    p = Permutation([0, 2, 3, 1])   # mapping: 0->0,1->2,2->3,3->1
    x = Permutation([2, 0, 3, 1])   # mapping: 0->2,1->0,2->3,3->1
    # compute commutator c = ~x * ~p * x * p
    c = p.commutator(x)
    # explicit equality with product ~x*~p*x*p
    assert c == (~x) * (~p) * x * p
    # ensure result is a Permutation and not identity
    assert isinstance(c, Permutation)
    I = Permutation(4)  # identity of size 4
    assert c != I

def test_commutator_commuting_pairs_are_identity():
    # create a few identity-shifted permutations which commute with identity
    I = Permutation(3)
    perms = [I + i for i in range(6)]
    # verify pairwise commutator behavior matches commutativity
    for i in range(len(perms)):
        for j in range(len(perms)):
            a = perms[i]
            b = perms[j]
            c = a.commutator(b)
            if a * b == b * a:
                assert c == Permutation(3)  # identity of same base size (I)
            else:
                assert c != Permutation(3)

def test_commutator_size_mismatch():
    p = Permutation([1, 0])   # size 2
    q = Permutation([1, 2, 0])  # size 3
    with pytest.raises(ValueError):
        p.commutator(q)

def test_commutator_on_identity_and_self():
    # commutator with identity must be identity
    a = Permutation([2, 0, 1, 4, 3])
    I = Permutation(5)
    assert a.commutator(I) == I
    assert I.commutator(a) == I

def test_commutator_involutive_and_nontrivial_cases():
    # Test with transpositions and longer cycles
    t = Permutation([1, 0, 2, 3])  # transposition (0 1)
    c = Permutation([1, 2, 0, 3])  # 3-cycle on 0,1,2
    # check commutator equals explicit product ~c*~t*c*t
    assert t.commutator(c) == (~c) * (~t) * c * t
    # verify non-identity when they don't commute
    if t * c != c * t:
        assert t.commutator(c) != Permutation(4)
    # check when they do commute (commuting with disjoint supports)
    d = Permutation([0, 1, 3, 2])  # transposition (2 3) disjoint from t
    assert t * d == d * t
    assert t.commutator(d) == Permutation(4)