import pytest
from sympy.combinatorics.permutations import Permutation

def test_xor_basic_conjugation_and_inverse():
    # create permutations p and q of same size via array-form constructors
    p = Permutation(1, 2, 9)  # cycles (1 2 9)
    q = Permutation(6, 9, 8)  # cycles (6 9 8)
    # ensure sizes match
    assert p.size == q.size

    # conjugate p by q: c = p ^ q (which returns ~q * p * q)
    c = p ^ q
    # check conjugation identities: c == ~q*p*q and p == q*c*~q
    assert c == (~q) * p * q
    assert p == q * c * (~q)

    # check that conjugate has same cycle structure as original
    assert p.cycle_structure == c.cycle_structure

    # conjugation is consistent with exponent chaining: q^p^r == q^(p*r)
    r = Permutation(9)(4, 6, 8)  # build via call to create a cycle on existing size
    left = q ^ p ^ r
    right = q ^ (p * r)
    assert left == right

def test_xor_integer_left_selects_image():
    # For integer i ^ p, __rxor__ is used; ensure integer selection matches p(i)
    p = Permutation(1, 0, 2)  # size 3, mapping 0->1,1->0,2->2
    for i in range(p.size):
        # left operand int, right operand Permutation: uses __rxor__ of Permutation via Python
        # But this test ensures that i ^ p equals p(i)
        assert i ^ p == p(i)

def test_xor_size_mismatch_raises():
    p = Permutation(1, 2, 3)  # size 4 (0..3)
    q = Permutation(1, 2)     # size 3 (0..2)
    # Ensure sizes differ
    assert p.size != q.size
    with pytest.raises(ValueError):
        _ = p ^ q

def test_xor_result_is_new_and_not_alias_of_inputs():
    # verify that returned permutation is a distinct object (not the same identity)
    p = Permutation(1, 2, 3)  # some permutation
    q = Permutation(3, 0, 1, 2)
    c = p ^ q
    assert isinstance(c, Permutation)
    # ensure array forms differ from inputs unless conjugation yields same
    # but at minimum, identity of object should be different
    assert c is not p
    assert c is not q

def test_xor_conjugate_properties_with_inverse_choice():
    # Test that using ~r produces the other conjugate r*p*~r
    p = Permutation(1, 2, 9)(5, 6)  # composite cycles
    r = Permutation(9)(4, 6, 8)
    # p ^ ~r should equal r * p * ~r
    assert p ^ (~r) == r * p * (~r)
    # and ~r * p * r is also a valid conjugate (but may differ)
    conjugate1 = (~r) * p * r
    conjugate2 = r * p * (~r)
    # They may or may not be equal; ensure both are permutations of same size and same cycle structure as p
    assert conjugate1.size == p.size
    assert conjugate2.size == p.size
    assert conjugate1.cycle_structure == p.cycle_structure
    assert conjugate2.cycle_structure == p.cycle_structure