import pytest
from sympy.combinatorics.permutations import Permutation

def test_commutator_basic():
    # Example from docstring
    Permutation.print_cyclic = False
    p = Permutation([0, 2, 3, 1])
    x = Permutation([2, 0, 3, 1])
    c = p.commutator(x)
    # check equals ~x*~p*x*p
    assert c == (~x) * (~p) * x * p
    # explicit expected array form
    assert list(c.array_form) == [2, 1, 3, 0]

def test_commutator_identity_and_noncommuting():
    I = Permutation(3)
    # Create a small set of permutations: identity and shifts
    p_list = [I + i for i in range(6)]
    # verify commutator properties: commutator is identity iff they commute
    for i in range(len(p_list)):
        for j in range(len(p_list)):
            a = p_list[i]
            b = p_list[j]
            c = a.commutator(b)
            if a * b == b * a:
                assert c == I
            else:
                assert c != I

def test_commutator_size_mismatch():
    p = Permutation([0,1,2])
    q = Permutation([0,1,2,3])
    with pytest.raises(ValueError):
        p.commutator(q)

def test_commutator_involutive_and_trivial_cases():
    # commutator of identity with any permutation is identity
    I = Permutation(5)
    a = Permutation([1,0,2,3,4])  # transposition (0 1)
    assert I.commutator(a) == I
    assert a.commutator(I) == I

    # commutator of element with itself is identity
    assert a.commutator(a) == I

def test_commutator_random_pairs_small():
    # test random permutations of size 6 for consistency with formula
    import random
    random.seed(0)
    n = 6
    for _ in range(20):
        arr1 = list(range(n))
        arr2 = list(range(n))
        random.shuffle(arr1)
        random.shuffle(arr2)
        p = Permutation(arr1)
        q = Permutation(arr2)
        c = p.commutator(q)
        # verify def: c == ~q*~p*q*p
        assert c == (~q) * (~p) * q * p

def test_commutator_structure_matches_computed_array():
    # Construct two permutations where we can compute commutator manually
    a = Permutation([2,0,1,4,3])  # cycles (0 2 1)(3 4)
    b = Permutation([1,2,0,3,4])  # cycle (0 1 2)
    # compute using array_form operations to mirror implementation
    arr_a = a.array_form
    arr_b = b.array_form
    n = len(arr_a)
    inva = [None]*n
    for i in range(n):
        inva[arr_a[i]] = i
    invb = [None]*n
    for i in range(n):
        invb[arr_b[i]] = i
    # expected array as in implementation: [a[b[inva[i]]] for i in invb]
    expected = [arr_a[arr_b[inva[i]]] for i in invb]
    c = a.commutator(b)
    assert list(c.array_form) == expected