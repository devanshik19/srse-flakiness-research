import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic_example():
    # Example from docstring
    Permutation.print_cyclic = False
    p = Permutation([0, 2, 3, 1])
    x = Permutation([2, 0, 3, 1])
    c = p.commutator(x)
    # expected as in doc: Permutation([2,1,3,0])
    assert isinstance(c, Permutation)
    assert list(c) == [2, 1, 3, 0]
    # verify definition: ~x * ~p * x * p
    assert c == (~x) * (~p) * x * p

def test_commutator_identity_and_noncommuting():
    I = Permutation(3)  # identity on 3 points (0,1,2)
    # create a list of permutations by adding offsets to identity
    p_list = [I + i for i in range(6)]
    n = len(p_list)
    for i in range(n):
        for j in range(n):
            pi = p_list[i]
            pj = p_list[j]
            c = pi.commutator(pj)
            if pi * pj == pj * pi:
                assert c == I
            else:
                assert c != I

def test_commutator_size_mismatch_raises():
    p = Permutation([0, 1, 2])
    q = Permutation([0, 1, 2, 3])
    with pytest.raises(ValueError):
        p.commutator(q)

def test_commutator_involution_and_properties():
    # Check that commutator of an element with itself is identity
    a = Permutation([1, 2, 0, 4, 3])
    c = a.commutator(a)
    I = Permutation(a.size)
    assert c == I

    # For inverse elements: commutator(g, g^-1) should be identity as well
    g = Permutation([2, 0, 1, 4, 3])
    gi = ~g
    assert g * gi == I
    assert g.commutator(gi) == I
    assert gi.commutator(g) == I

def test_commutator_consistency_with_manual_array_computation():
    # construct random small permutations and compare to manual computation
    import random
    for n in range(2, 6):
        # test a few random pairs for each size
        for _ in range(10):
            arr1 = list(range(n))
            arr2 = list(range(n))
            random.shuffle(arr1)
            random.shuffle(arr2)
            p = Permutation(arr1)
            q = Permutation(arr2)
            # manual computation following implementation:
            a = p.array_form
            b = q.array_form
            nlen = len(a)
            inva = [None] * nlen
            for i in range(nlen):
                inva[a[i]] = i
            invb = [None] * nlen
            for i in range(nlen):
                invb[b[i]] = i
            manual = [a[b[inva[i]]] for i in invb]
            comm = p.commutator(q)
            assert list(comm) == manual