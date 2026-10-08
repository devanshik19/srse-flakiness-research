import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic_noncommuting():
    # Example from docstring: p and x do not commute
    Permutation.print_cyclic = False
    p = Permutation([0, 2, 3, 1])
    x = Permutation([2, 0, 3, 1])
    c = p.commutator(x)
    # commutator should equal ~x*~p*x*p
    assert c == (~x) * (~p) * x * p
    # and the result is not the identity
    I = Permutation(4)
    assert c != I
    # check explicit array form of the expected commutator
    assert list(c.array_form) == [2, 1, 3, 0]

def test_commutator_commuting_pairs_return_identity():
    # Identity permutation I of size 3
    I = Permutation(3)
    # create list [I + i for i in range(6)] as in docstring: this uses __add__
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
    p = Permutation([1, 0, 2])  # size 3
    q = Permutation([1, 0, 2, 3])  # size 4
    with pytest.raises(ValueError):
        p.commutator(q)

def test_commutator_involution_properties():
    # If p and x are inverses (p*x = identity), commutator simplifies:
    # comm = ~x*~p*x*p -> when x = ~p, this becomes p*~p*~p*p = identity
    p = Permutation([2, 0, 1, 3])  # a 3-cycle on first three
    invp = ~p
    c = p.commutator(invp)
    I = Permutation(4)
    assert c == I

def test_commutator_with_identity():
    # commutator with identity should be identity
    I = Permutation(5)
    p = Permutation([1, 2, 3, 4, 0])
    assert p.commutator(I) == I
    assert I.commutator(p) == I