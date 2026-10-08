import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_basic_and_inverse_property():
    # Create a permutation from cycles [[2,0], [3,1]]
    p = Permutation([[2, 0], [3, 1]])
    # Inverse via bitwise not (~)
    inv = ~p
    # The inverse should equal the power -1
    assert inv == p**-1
    # Multiplying permutation by its inverse should give identity of appropriate size
    identity = Permutation(list(range(p.size())))
    assert p * inv == identity
    assert inv * p == identity

def test_invert_array_form_and_double_inversion():
    # Create using array form directly
    arr = [2, 3, 0, 1]
    p = Permutation(arr)
    # ~p should produce the mathematical inverse: compute inverse manually
    expected_inv = [0] * len(arr)
    for i, image in enumerate(arr):
        expected_inv[image] = i
    inv = ~p
    assert inv.array_form == expected_inv
    # Double inversion returns the original permutation
    assert ~(~p) == p

def test_invert_identity_and_singleton():
    # Identity permutation should be its own inverse
    id_perm = Permutation(list(range(5)))
    assert ~id_perm == id_perm
    # Singleton permutation (size 1) is identity as well
    single = Permutation([0])
    assert ~single == single

def test_invert_commutation_with_mul_and_properties():
    # Random small permutation via explicit array
    p = Permutation([3, 0, 2, 1])
    inv = ~p
    # Check that inv is indeed inverse by composing and checking each image
    comp = (p * inv).array_form
    assert comp == list(range(p.size()))
    comp2 = (inv * p).array_form
    assert comp2 == list(range(p.size()))
    # Check parity preserved between p**-1 and ~p
    assert inv == p**-1
    assert inv.parity() == (p**-1).parity()

def test_invert_raises_or_handles_invalid_constructs():
    # Ensure that permutations created from invalid iterable sizes raise appropriately
    # Permutation will usually normalize input; constructing from mismatched forms may raise
    with pytest.raises(Exception):
        # Passing a nested malformed structure that Permutation should reject
        Permutation([[1, 2], [3]])  # inconsistent cycle pairs likely invalid