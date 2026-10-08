import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic():
    # Example from docstring
    Permutation.print_cyclic = False
    p = Permutation([0, 2, 3, 1])
    x = Permutation([2, 0, 3, 1])
    c = p.commutator(x)
    # expected commutator equals ~x*~p*x*p
    assert c == (~x) * (~p) * x * p
    # check the returned object is a Permutation and has correct array_form
    assert isinstance(c, Permutation)
    assert c.array_form == [2, 1, 3, 0]

def test_commutator_identity_when_commute():
    # identity permutation of size 3
    I = Permutation(3)
    # generate a few permutations by adding to identity (using __add__)
    p_list = [I + i for i in range(6)]
    for i in range(len(p_list)):
        for j in range(len(p_list)):
            a = p_list[i]
            b = p_list[j]
            c = a.commutator(b)
            if a * b == b * a:
                assert c == I
            else:
                assert c != I

def test_commutator_size_mismatch_raises():
    p = Permutation([0, 1, 2])
    q = Permutation([0, 1, 2, 3])
    with pytest.raises(ValueError):
        p.commutator(q)

def test_commutator_involution_cases():
    # test with transposition and 3-cycle
    t = Permutation([1, 0, 2, 3])  # transposition (0 1)
    c3 = Permutation([1, 2, 0, 3])  # 3-cycle on 0,1,2
    comm = t.commutator(c3)
    # check that commutator equals identity iff they commute
    assert (t * c3 == c3 * t) == (comm == Permutation(4))
    # also check anti-commuting yields non-identity
    assert comm != Permutation(4) or t * c3 == c3 * t

def test_commutator_with_self_is_identity():
    # commutator of a permutation with itself should be identity
    p = Permutation([2, 0, 1, 3])
    assert p.commutator(p) == Permutation(4)