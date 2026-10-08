import pytest
from sympy.combinatorics.permutations import Permutation

def test_xor_conjugation_basic_cycle():
    # simple 3-cycle conjugation; size inferred from largest element
    p = Permutation(1, 2, 3)  # (1 2 3)
    q = Permutation(0, 2, 1)  # (1 0)(2) i.e. swap 0 and 1 on size 3
    # Ensure sizes match
    assert p.size == q.size
    # conjugate c = p ^ q (which computes ~q * p * q)
    c = p ^ q
    # Check that c equals ~q * p * q
    assert c == (~q) * p * q
    # Check conjugation property: p == q * c * ~q
    assert p == q * c * (~q)

def test_xor_integer_left_operand_selects_image():
    # If left operand is an integer i, i ^ p should equal p(i)
    p = Permutation(2, 0, 1)  # mapping: 0->2,1->0,2->1
    for i in range(p.size):
        # using __rxor__ behavior: integer ^ permutation
        assert (i ^ p) == p(i)

def test_xor_chain_associativity_vs_precedence():
    # Demonstrate (q ^ p) ^ r differs from q ^ (p * r) generally,
    # but due to implementation p^q^r == p^(q*r) as described in docstring.
    p = Permutation(1, 2, 9)  # creates size at least 10
    q = Permutation(6, 9, 8)
    r = Permutation(9)(4, 6, 8)  # compose a 3-cycle on size >=10
    left = q ^ p ^ r
    right = q ^ (p * r)
    assert left == right

def test_xor_size_mismatch_raises():
    p = Permutation(0, 1, 2)       # size 3
    q = Permutation(0, 1, 2, 3)    # size 4
    with pytest.raises(ValueError):
        _ = p ^ q

def test_xor_identity_and_inverse_behavior():
    # identity permutation
    e = Permutation(list(range(5)))
    p = Permutation(1, 3, 4)(0, 2)  # some permutation of size >=5
    # conjugating by identity leaves permutation unchanged
    assert p ^ e == p
    # conjugating by inverse (i.e. ~p) should give ~p * p * p = ~p * (p*p) = ~p * p^2
    # but more directly: p == p ^ e, and also ~p ^ p should equal p * ~p * p?? check consistency:
    # Ensure conjugation returns a Permutation object and has same cycle structure
    conj = p ^ p
    assert isinstance(conj, Permutation)
    assert conj.cycle_structure() == p.cycle_structure()

def test_xor_internal_array_form_result_matches_manual_computation():
    # Build permutations by explicit array form to control mapping
    # Define size 6 permutation p and h with array forms
    # array form: list where index -> image
    p = Permutation([2, 0, 1, 5, 4, 3])  # cycles: (0 2 1)(3 5)(4)
    h = Permutation([1, 2, 0, 4, 5, 3])  # cycles: (0 1 2)(3 4 5)
    # manual computation of a[h[i]] = h[p[i]] per implementation
    size = p.size
    a = [None] * size
    h_af = h.array_form
    p_af = p.array_form
    for i in range(size):
        a[h_af[i]] = h_af[p_af[i]]
    expected = Permutation(a)
    result = p ^ h
    assert result == expected
    # Ensure result has same size and valid array form (no None)
    assert result.size == size
    assert None not in result.array_form