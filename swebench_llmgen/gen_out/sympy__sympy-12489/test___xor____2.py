import pytest
from sympy.combinatorics.permutations import Permutation

def test_xor_conjugation_basic():
    # Create permutations p and q of same size
    p = Permutation(1, 2, 9)        # a 10-point permutation since max is 9
    q = Permutation(6, 9, 8)        # also size 10
    # conjugate c = p ^ q should satisfy c == ~q * p * q
    c = p ^ q
    assert c == (~q) * p * q
    # also p == q * c * (~q)
    assert p == q * c * (~q)
    # check that the conjugate has the same cycle structure as p
    assert c.cycle_structure == p.cycle_structure

def test_xor_associativity_like_property():
    # Verify that p^q^r equals p^(q*r) per the docstring choice
    p = Permutation(1, 2, 9)
    q = Permutation(6, 9, 8)
    r = Permutation(9)(4, 6, 8)  # composition of a fixed-point and a 10-point 3-cycle
    left = q ^ p ^ r
    right = q ^ (p * r)
    assert left == right

def test_xor_integer_left_selects_image():
    # If left argument is an integer i, i ^ p should be p(i)
    p = Permutation(1, 2, 9)
    size = p.size
    for i in range(size):
        # __rxor__ is implemented so that integer ^ permutation yields image
        assert (i ^ p) == p(i)

def test_xor_size_mismatch_raises():
    # Different sizes should raise ValueError
    p = Permutation(1, 2, 3)  # size 4 (max 3)
    q = Permutation(1, 2, 3, 4, 5)  # size 6 (max 5)
    with pytest.raises(ValueError):
        _ = p ^ q

def test_xor_internal_array_form_mapping():
    # Construct a permutation explicitly via cycles and verify the array-form mapping
    # Use small size where behavior is easy to verify
    # Permutation a: (0 2 1) on size 3 -> array form [2,0,1]
    a = Permutation(0, 2, 1)
    # Permutation h: (0 1) -> array form [1,0,2]
    h = Permutation(0, 1)
    # Compute conjugate a^h using formula: a^h = ~h * a * h
    conj = a ^ h
    expected = (~h) * a * h
    assert conj == expected
    # Verify that the array form of conj matches mapping a[h[i]] -> h[a[i]] per implementation
    # Rebuild expected array form directly
    h_af = h.array_form
    a_af = a.array_form
    size = a.size
    arr = [None] * size
    for i in range(size):
        arr[h_af[i]] = h_af[a_af[i]]
    # create permutation from array form and compare
    from sympy.combinatorics.permutations import _af_new
    arr_perm = _af_new(arr)
    assert conj == arr_perm

def test_xor_involution_with_inverse():
    # For any r, ~r * p * r and r * p * ~r are conjugates; ensure both are valid and of same structure
    p = Permutation(1, 2, 9)(5, 6)
    r = Permutation(9)(4, 6, 8)
    left = (~r) * p * r
    right = r * p * (~r)
    # They should both be permutations of same size and have same cycle structure
    assert left.size == p.size == right.size
    assert left.cycle_structure == right.cycle_structure
    # It's allowed that they may be different; ensure xor can reproduce them:
    assert left == p ^ r  # since p ^ r is defined as ~r * p * r
    # And conjugating p by ~r gives the other
    assert right == p ^ (~r)