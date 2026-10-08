import pytest
from sympy.combinatorics.permutations import Permutation

def test_xor_conjugation_basic():
    # p and q of same size
    p = Permutation(1, 2, 9)           # cycle (1 2 9)
    q = Permutation(6, 9, 8)           # cycle (6 9 8)
    # conjugate c = p ^ q should equal ~q * p * q
    c = p ^ q
    assert c == (~q) * p * q
    # also p == q * c * ~q per docstring relation
    assert p == q * c * (~q)

def test_xor_associativity_like_behavior():
    # demonstrate p^q^r == p^(q*r) (as chosen by implementation)
    p = Permutation(1, 4, 8)           # (1 4 8)
    q = Permutation(9)(6, 8)           # (6 8) with fixed 9
    r = Permutation(9)(4, 6, 8)        # (4 6 8) with fixed 9
    left = q ^ p ^ r
    right = q ^ (p * r)
    assert left == right

def test_xor_integer_left_selects_image():
    # If left operand is integer i, then i ^ p returns p(i)
    p = Permutation(1, 2, 0)  # permutation on 3 points: 0->1,1->2,2->0
    for i in range(p.size):
        assert (i ^ p) == p(i)

def test_xor_size_mismatch_raises():
    p = Permutation(1, 2, 3)  # size 4 (0..3)
    q = Permutation(1, 2)     # smaller permutation
    with pytest.raises(ValueError):
        _ = p ^ q

def test_xor_full_array_form_result():
    # construct permutations via array form and test explicit mapping
    # Define h as mapping: 0->2,1->0,2->1 (cycle (0 2 1))
    h = Permutation(2, 0, 1)
    # Define p as mapping: 0->1,1->2,2->0 (cycle (0 1 2))
    p = Permutation(1, 2, 0)
    # Compute a = p ^ h using algorithm: a[h[i]] = h[p[i]]
    a = p ^ h
    # Manually compute expected array form:
    # p: [1,2,0], h: [2,0,1]
    # For i=0: a[h[0]=2] = h[p[0]=1] = h[1]=0  => a[2]=0
    # i=1: a[h[1]=0] = h[p[1]=2] = h[2]=1  => a[0]=1
    # i=2: a[h[2]=1] = h[p[2]=0] = h[0]=2  => a[1]=2
    expected = Permutation(1, 2, 0)
    assert a == expected

def test_xor_with_involution_and_inverse_relations():
    # check that conjugating by inverse (~h) gives alternate conjugate
    r = Permutation(1, 3, 2)(4, 5)  # mix of cycles
    p = Permutation(1, 2, 9)(5, 6)
    # ~r * p * r and r * p * ~r are both conjugates but not necessarily equal
    conj1 = (~r) * p * r
    conj2 = r * p * (~r)
    # Both should have same cycle structure (conjugates)
    assert conj1.cycle_structure == conj2.cycle_structure
    # Using method p ^ ~r should produce r * p * ~r (per docstring)
    assert p ^ (~r) == r * p * (~r)