import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic_example():
    # Example from docstring
    Permutation.print_cyclic = False
    p = Permutation([0, 2, 3, 1])
    x = Permutation([2, 0, 3, 1])
    c = p.commutator(x)
    # commutator should equal ~x*~p*x*p
    assert c == (~x) * (~p) * x * p
    # check expected array form explicitly
    assert list(c.array_form) == [2, 1, 3, 0]

def test_commutator_identity_when_commute():
    # identity permutations of same size
    I = Permutation(3)
    # create list of permutations: I, I+1, I+2,... using __add__
    p = [I + i for i in range(6)]
    for i in range(len(p)):
        for j in range(len(p)):
            c = p[i].commutator(p[j])
            if p[i] * p[j] == p[j] * p[i]:
                assert c == I
            else:
                assert c != I

def test_commutator_different_sizes_raises():
    p = Permutation([0, 1, 2])
    q = Permutation([0, 1, 2, 3])
    with pytest.raises(ValueError):
        p.commutator(q)

def test_commutator_involution_properties():
    # Check that commutator is identity when one is identity
    I = Permutation(5)
    p = Permutation([1, 0, 2, 3, 4])  # a transposition
    assert p.commutator(I) == I
    assert I.commutator(p) == I

def test_commutator_nontrivial_behaviour():
    # Construct two permutations that do not commute
    a = Permutation([1, 2, 0, 4, 3])  # (0 1 2)(3 4)
    b = Permutation([0, 2, 1, 3, 4])  # (1 2)
    c = a.commutator(b)
    # commutator should be permutation (conjugation commutator), check it's not identity
    assert c != Permutation(5)
    # Validate again by direct formula ~b*~a*b*a
    assert c == (~b) * (~a) * b * a