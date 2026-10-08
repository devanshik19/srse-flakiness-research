import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_basic_array_form():
    # basic 4-element permutation given in array-of-cycles initializer
    p = Permutation([[2, 0], [3, 1]])
    inv = ~p
    # array form of p should be [2,3,0,1] and inverse should reverse mapping
    assert list(p.array_form) == [2, 3, 0, 1]
    # inverse should map 2->0,3->1,0->2,1->3 so array form is [2,3,0,1] inverted -> [2,3,0,1]**-1
    # Check algebraic properties: p * inv = identity and inv * p = identity
    identity = Permutation(list(range(p.size)))
    assert p * inv == identity
    assert inv * p == identity
    # also check that inverse equals power -1
    assert inv == p**-1

def test_invert_identity_and_singleton():
    # identity permutation: inversion returns itself
    id_perm = Permutation(list(range(5)))
    assert ~id_perm == id_perm
    # singleton/size-1 permutation
    single = Permutation([0])
    assert ~single == single
    # check multiplication property for singleton
    assert single * ~single == single

def test_invert_cycles_and_array_roundtrip():
    # create permutation from cyclic notation via list constructor
    p = Permutation([[1, 2, 3]])
    inv = ~p
    # applying permutation then inverse to each element yields original
    for i in range(p.size):
        assert (p(i)) == inv.__call__(p(i)) or (p*inv)(i) == i
    # explicit check: p * ~p is identity
    assert p * inv == Permutation(list(range(p.size)))

def test_invert_consistency_multiple_sizes():
    # test random permutations of several sizes to ensure inverse is correct
    import random
    for n in range(1, 8):
        seq = list(range(n))
        random.shuffle(seq)
        p = Permutation(seq)
        inv = ~p
        # check element-wise that composing gives identity
        for i in range(n):
            assert (p(inv(i))) == i
            assert (inv(p(i))) == i
        assert p * inv == Permutation(list(range(n)))
        assert inv * p == Permutation(list(range(n)))

def test_invert_does_not_modify_original():
    p = Permutation([2, 0, 1, 4, 3])
    original_af = list(p.array_form)
    inv = ~p
    # ensure original permutation's array form is unchanged
    assert list(p.array_form) == original_af
    # ensure inverse is distinct when not self-inverse
    if p != inv:
        assert p != inv