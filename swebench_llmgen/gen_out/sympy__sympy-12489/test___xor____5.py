import pytest
from sympy.combinatorics.permutations import Permutation

def test_xor_conjugate_basic():
    # simple permutations of same size
    p = Permutation(1, 2, 9)  # cycle (1 2 9)
    q = Permutation(6, 9, 8)  # cycle (6 9 8)
    # conjugate c = p ^ q should equal ~q * p * q
    c = p ^ q
    assert c == (~q) * p * q
    # p should be conjugate back: p == q * c * ~q
    assert p == q * c * (~q)
    # check cycle structure preserved
    assert p.cycle_structure == c.cycle_structure

def test_xor_integer_left_selects_element():
    # If left operand is int i, then i ^ p returns p(i)
    p = Permutation(2, 0, 1)  # size 3, mapping: 0->2,1->0,2->1
    for i in range(p.size):
        assert (i ^ p) == p(i)

def test_xor_chain_associativity_like_behavior():
    # check that q^p^r equals q^(p*r) because implementation chooses ~r*p*r
    q = Permutation(6, 9, 8)
    p = Permutation(1, 2, 9)
    r = Permutation(9)(4, 6, 8)  # creation via product of singletons and cycle
    left = q ^ p ^ r
    right = q ^ (p * r)
    assert left == right

def test_xor_size_mismatch_raises():
    p = Permutation(1, 2, 3)  # size inferred from elements
    # make a different size permutation
    # create a permutation of size > p.size by using a larger element
    big = Permutation(10)  # singleton at 10 implies size at least 11
    with pytest.raises(ValueError):
        _ = p ^ big

def test_xor_constructs_correct_array_form_edgecases():
    # identity conjugation: conjugating by identity gives same permutation
    r = Permutation(0, 1, 2, 3)  # some permutation
    e = Permutation()  # identity permutation (size 0) -> create same size identity
    # Ensure same-size identity: produce identity of same size via Iteration: use r * ~r
    identity_same_size = r * (~r)
    assert identity_same_size.size == r.size
    assert r ^ identity_same_size == r

    # test conjugation with an involution (self-inverse)
    s = Permutation(1, 0, 3, 2)  # product of transpositions (0 1)(2 3), self-inverse
    t = Permutation(2, 3, 0, 1)  # another permutation same size
    conj = t ^ s
    # since s is its own inverse, conj == s * t * s
    assert conj == s * t * s