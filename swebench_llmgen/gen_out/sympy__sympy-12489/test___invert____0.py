import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_basic_array_form():
    # simple 4-element permutation given in cycle pairs form (as in doc example)
    p = Permutation([[2, 0], [3, 1]])
    inv = ~p
    # The inverse of p should be equal to p**-1
    assert inv == p**-1
    # Multiplying a permutation by its inverse yields the identity of appropriate size
    identity = Permutation(list(range(p.size)))
    assert p*inv == identity
    assert inv*p == identity
    # Confirm the array form explicitly matches expected inverse mapping
    # p maps: 0->2, 1->3, 2->0, 3->1 so inverse maps: 0->2,1->3,2->0,3->1
    assert inv.array_form == [2, 3, 0, 1]

def test_invert_identity_and_singleton():
    # Identity permutation: inverse is itself
    id_perm = Permutation([0, 1, 2, 3, 4])
    assert ~id_perm == id_perm
    # Singleton permutation (size 1)
    s = Permutation([0])
    assert ~s == s
    assert (s * ~s).array_form == [0]

def test_invert_composed_and_power():
    # Create permutations and test that inverse of a product equals reverse product of inverses
    a = Permutation([2, 0, 1, 4, 3])  # some permutation
    b = Permutation([1, 2, 0, 3, 4])  # another permutation
    ab = a * b
    inv_ab = ~ab
    # (~(a*b)) should equal (~b * ~a)
    assert inv_ab == (~b) * (~a)
    # Inverse of a power: (a**n)**-1 == (a**-1)**n
    for n in range(0, 6):
        left = ~(a**n)
        right = (~a)**n
        assert left == right

def test_invert_preserves_size_and_support():
    p = Permutation([3, 0, 1, 2, 5, 4])
    inv = ~p
    assert p.size == inv.size
    # support (moved points) should be same
    assert set(p.support()) == set(inv.support())

def test_invert_random_consistency():
    # test random permutations of varying sizes for consistency properties
    import random
    for size in range(1, 8):
        seq = list(range(size))
        random.shuffle(seq)
        perm = Permutation(seq)
        inv = ~perm
        # composing twice yields identity when composing perm and its inverse
        assert (perm * inv).array_form == list(range(size))
        assert (inv * perm).array_form == list(range(size))
        # double inversion yields original
        assert ~(~perm) == perm

def test_invert_edge_cases():
    # test that inverting doesn't modify original object (immutability expected)
    p = Permutation([1, 0, 2])
    p_before = p.array_form.copy()
    inv = ~p
    assert p.array_form == p_before
    # ensure inverse has expected array form
    assert inv.array_form == [1, 0, 2]