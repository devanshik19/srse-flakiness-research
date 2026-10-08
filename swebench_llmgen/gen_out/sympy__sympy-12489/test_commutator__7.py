import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic():
    # Example from docstring
    Permutation.print_cyclic = False
    p = Permutation([0, 2, 3, 1])
    x = Permutation([2, 0, 3, 1])
    c = p.commutator(x)
    # expected as in docstring
    assert isinstance(c, Permutation)
    assert c == (~x) * (~p) * x * p
    assert c == Permutation([2, 1, 3, 0])

def test_commutator_identity_when_commute():
    # Identity permutation of size 3
    I = Permutation(3)
    # create several permutations of same size using addition behavior from class
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

def test_commutator_different_sizes_raises():
    p = Permutation([0, 1, 2])
    q = Permutation([0, 1, 2, 3])
    with pytest.raises(ValueError):
        p.commutator(q)

def test_commutator_involution_and_nontrivial():
    # Test using a transposition and a 3-cycle
    t = Permutation([1, 0, 2])     # transposition (0 1)
    c3 = Permutation([1, 2, 0])    # 3-cycle (0 1 2)
    comm = t.commutator(c3)
    # Check it's equal to ~c3 * ~t * c3 * t
    assert comm == (~c3) * (~t) * c3 * t
    # For these particular elements, they should not commute, so comm != identity
    I = Permutation(3)
    assert comm != I

def test_commutator_self_and_inverse():
    # commutator of a permutation with itself is the identity
    a = Permutation([2, 0, 1, 3])
    assert a.commutator(a) == Permutation(a.size)

    # commutator with inverse: p and p**-1 always commute? they should not in general,
    # but p * p**-1 == identity == p**-1 * p so they commute -> commutator identity
    inv = ~a
    assert a * inv == inv * a
    assert a.commutator(inv) == Permutation(a.size)