import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.permutations import _af_new


def test_xor_conjugation_basic():
    # simple permutations of same size
    p = Permutation(1, 2, 9)             # cycle (1 2 9)
    q = Permutation(6, 9, 8)             # cycle (6 9 8)
    # conjugate c = p ^ q should equal ~q * p * q
    c = p ^ q
    assert c == (~q) * p * q
    # and p should be q * c * ~q
    assert p == q * c * (~q)
    # conjugation preserves cycle structure (lengths)
    assert p.cycle_structure == c.cycle_structure


def test_xor_chaining_precedence():
    # verify associativity behavior described in docstring:
    q = Permutation(6, 9, 8)
    p = Permutation(1, 2, 9)
    r = Permutation(9)(4, 6, 8)  # r is product of fixed 9 and cycle (4 6 8)
    # q^p^r is (q^p)^r because of python left-associativity of ^
    left_assoc = q ^ p ^ r
    right_expr = q ^ (p * r)  # as documented, q^p^r == q^(p*r)
    assert left_assoc == right_expr

    # Also check q^(p^r) is not necessarily equal (sanity check using different grouping)
    alt = q ^ (p ^ r)
    # They may or may not be equal; ensure at least values are Permutation and comparable
    assert isinstance(alt, Permutation)
    assert isinstance(left_assoc, Permutation)


def test_xor_integer_on_left_selects_image():
    # If left operand is integer i, i ^ p should select p(i)
    p = Permutation(1, 2, 3, 0)  # a 4-cycle (0 1 2 3)
    for i in range(p.size):
        # __rxor__ is implemented so integer ^ permutation returns image
        assert (i ^ p) == p(i)


def test_xor_size_mismatch_raises():
    p = Permutation(1, 2, 3)      # size 4 (0..3)
    q = Permutation(1, 2)         # size 3 (0..2)
    # Ensure sizes differ
    assert p.size != q.size
    with pytest.raises(ValueError):
        _ = p ^ q


def test_xor_internal_array_form_result_consistency():
    # Construct permutations by array forms and validate __xor__ uses array forms internally.
    # Build permutation a: mapping 0->2,1->0,2->1 (cycle (0 2 1))
    a_af = [2, 0, 1]
    a = _af_new(list(a_af))
    # Build permutation b: mapping 0->1,1->2,2->0 (cycle (0 1 2))
    b_af = [1, 2, 0]
    b = _af_new(list(b_af))

    # compute conjugate via algorithm: for i, result[h[i]] = h[p[i]]
    # replicate algorithm to verify
    h = b._array_form
    p = a._array_form
    expected = [None] * a.size
    for i in range(a.size):
        expected[h[i]] = h[p[i]]
    expected_perm = _af_new(expected)

    got = a ^ b
    assert got == expected_perm
    # double-check algebraic conjugation property
    assert got == (~b) * a * b


def test_xor_with_identity_and_inversion():
    # conjugating by identity yields same permutation
    p = Permutation(3, 0, 2, 1)  # some permutation
    e = Permutation()            # identity permutation (size 0 by default) - create matching size identity
    # need identity of same size as p
    e_same = Permutation(list(range(p.size)))
    assert p ^ e_same == p

    # conjugating by inverse (~p) yields something conjugate: (~p)*p*p == p?
    conj = p ^ ~p
    # Should equal (~(~p))*p*(~p) == p*p*~p but simpler: conj == (~(~p))*p*(~p) == p*(~p)
    # Instead check conjugation algebra: conj == (~p) * p * p
    assert conj == (~p) * p * p


# Run tests directly if module executed (useful for debugging outside pytest)
if __name__ == "__main__":
    pytest.main([__file__])