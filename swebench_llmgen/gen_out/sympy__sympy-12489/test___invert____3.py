import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_basic_array_form():
    # create permutation from cycles input ([[2,0],[3,1]] means mapping 0->2,2->0,1->3,3->1)
    p = Permutation([[2, 0], [3, 1]])
    inv = ~p  # uses __invert__
    # array form of p should be [2,3,0,1] (0->2,1->3,2->0,3->1)
    assert p.array_form == [2, 3, 0, 1]
    # inverse should bring each element back
    assert inv.array_form == [2, 3, 0, 1]  # here inverse equals same because p is product of disjoint transpositions
    # multiplication by inverse yields identity
    identity = p * inv
    assert identity.array_form == list(range(p.size))
    identity2 = inv * p
    assert identity2.array_form == list(range(p.size))

def test_invert_vs_pow_negative_and_mul():
    # test with a non-involution permutation
    # permutation mapping: 0->1,1->2,2->0 (3-cycle), extended with fixed 3
    p = Permutation([1,2,0,3])
    inv = ~p
    # p**-1 should equal inverse
    assert p**-1 == inv
    # check that multiplying gives identity
    assert (p * inv).is_Identity()
    assert (inv * p).is_Identity()
    # ensure inverse mapping is correct: array form of inverse should map 1->0,2->1,0->2
    assert inv.array_form == [2,0,1,3]

def test_invert_of_identity_and_singleton():
    # identity permutation remains identity after invert
    idp = Permutation(list(range(5)))
    inv = ~idp
    assert inv.is_Identity()
    assert inv.array_form == idp.array_form
    # singleton/empty style handling: size 1
    s = Permutation([0])
    assert (~s).array_form == [0]
    assert (~s).is_Identity()

def test_invert_commutation_and_properties():
    # create a more complex permutation and ensure properties hold
    p = Permutation([3,0,4,1,2])  # a 5-element permutation
    inv = ~p
    # inverse should satisfy p[inv[i]] == i and inv[p[i]] == i for all i
    for i in range(p.size):
        assert p.array_form[inv.array_form[i]] == i
        assert inv.array_form[p.array_form[i]] == i
    # inverse of inverse is original
    assert ~(~p) == p
    # inverse parity same as original
    assert p.parity() == inv.parity()

def test_invert_raises_on_invalid_internal_state(monkeypatch):
    # simulate a malformed internal array_form to ensure invert handles unexpected shapes
    p = Permutation([1,0,2])
    # monkeypatch internal _array_form to an invalid mapping (duplication)
    monkeypatch.setattr(p, '_array_form', [1,1,2], raising=False)
    # attempting to invert such malformed permutation may raise an exception (ValueError or similar)
    with pytest.raises(Exception):
        _ = ~p