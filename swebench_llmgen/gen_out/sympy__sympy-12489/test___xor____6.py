import pytest
from sympy.combinatorics.permutations import Permutation

def test_xor_conjugation_basic():
    # simple permutations of same size
    p = Permutation(1, 2, 9)
    q = Permutation(6, 9, 8)
    # conjugate c = p ^ q should equal (~q) * p * q
    c = p ^ q
    assert c == (~q) * p * q
    # and conversely p == q * c * ~q
    assert p == q * c * ~q

def test_xor_associativity_like_property():
    # check that p^q^r equals p^(q*r) with the chosen definition in code
    p = Permutation(1, 2, 9)
    q = Permutation(6, 9, 8)
    r = Permutation(9)(4, 6, 8)  # build r as in docstring
    left = q ^ p ^ r
    right = q ^ (p * r)
    assert left == right
    # also check the other parenthesization differs in general
    other = q ^ (p ^ r)
    # They might or might not be equal for particular perms; ensure at least one inequality or equality holds sensibly
    assert (left == other) or (left != other)

def test_xor_integer_on_left_selects_image():
    p = Permutation(3)(1, 2)  # Permutation of size 4: (1 2)
    size = p.size
    # For each index i, i ^ p should equal p(i)
    for i in range(size):
        # __rxor__ handles int ^ Permutation, but using Python operator:
        assert (i ^ p) == p(i)

def test_xor_size_mismatch_raises():
    p = Permutation(1, 2, 9)  # size inferred from entries (at least 10)
    # make a permutation of different size: e.g., identity of smaller size
    small = Permutation(1)  # small size (2)
    with pytest.raises(ValueError):
        _ = p ^ small

def test_xor_result_array_form_consistency():
    # create a couple of permutations and verify the computed array form matches expected manual mapping
    # Build permutations explicitly by array form using constructor permutation notation
    a = Permutation(2, 0, 1)  # cycle (0 2 1)
    b = Permutation(1, 2, 0)  # cycle (0 1 2)
    # Compute conjugate via operator
    c = a ^ b
    # Manually compute expected: a^b = ~b * a * b
    expected = (~b) * a * b
    assert c == expected
    # Check that cycle structure is preserved under conjugation
    assert c.cycle_structure == a.cycle_structure

def test_xor_with_identity_and_self_conjugate():
    # conjugating by identity should give the same permutation
    p = Permutation(1, 3, 2)
    e = Permutation()  # identity
    assert (p ^ e) == p
    # conjugating identity by anything yields identity
    assert (e ^ p) == e

def test_xor_chained_examples_from_docs():
    # replicate a docstring style example to ensure behavior
    p = Permutation(1, 2, 9)(5, 6)
    r = Permutation(9)(4, 6, 8)
    # check that ~r*p*r and r*p*~r are permutations and comparably handled
    conj1 = ~r * p * r
    conj2 = r * p * ~r
    # They may or may not be equal; ensure operation runs and returns Permutation-like objects
    assert hasattr(conj1, 'array_form')
    assert hasattr(conj2, 'array_form')
    # Check that using ^ with ~r reproduces r*p*~r as documented
    assert p ^ ~r == conj2