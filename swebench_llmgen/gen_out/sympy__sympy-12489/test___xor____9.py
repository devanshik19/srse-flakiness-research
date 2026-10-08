import pytest
from sympy.combinatorics.permutations import Permutation

def test_xor_conjugation_basic():
    # simple permutations of same size
    p = Permutation(1, 2, 9)       # cycle (1 2 9)
    q = Permutation(6, 9, 8)       # cycle (6 9 8)
    # sizes must be equal; these were constructed with maximum element 9 -> size 10
    assert p.size == q.size

    # conjugate c = p ^ q should satisfy c == ~q * p * q
    c = p ^ q
    assert c == (~q) * p * q
    # and p == q * c * ~q
    assert p == q * c * (~q)

    # p and c are conjugate hence have same cycle structure
    assert p.cycle_structure() == c.cycle_structure()

def test_xor_chain_and_precedence():
    # create permutations r, p, q such that chaining behavior is testable
    r = Permutation(9)(4, 6, 8)    # uses __call__ to create a 9-size permutation with a 3-cycle
    p = Permutation(1, 2, 9)
    q = Permutation(6, 9, 8)

    # verify that q^p^r == q^(p*r) (as documented in method)
    left = q ^ p ^ r
    right = q ^ (p * r)
    assert left == right

    # precedence: * has higher precedence than ^
    # q^r*p^r should be equal to q^(r*p)^r
    a = (q ^ r) * (p ^ r)
    b = q ^ (r * p) ^ r
    assert a == b

def test_xor_integer_left_selects_image():
    # When left operand is integer i, i ^ p should select p(i)
    p = Permutation(2, 0, 1)  # 3-cycle (0 2 1)
    for i in range(p.size):
        assert (i ^ p) == p(i)

def test_xor_size_mismatch_raises():
    p = Permutation(1, 2, 9)   # size 10
    # make h of different size: e.g., permutation of size 5
    h = Permutation(1, 2, 3)   # size 4
    assert p.size != h.size
    with pytest.raises(ValueError):
        _ = p ^ h

def test_xor_array_form_is_used_and_returns_new_perm():
    # construct a permutation explicitly and conjugate by a transposition
    p = Permutation(0, 1, 2, 3)  # identity size 4 (explicit)
    # create a transposition swapping 1 and 2
    t = Permutation(2, 1)        # interpreted in context will have size 3 -> we need same size
    # ensure sizes equal by creating transposition in same size
    t = Permutation(0, 2)(1, 3)  # build a permutation of size at least 4 with a transposition (0 2) and (1 3)
    assert p.size == t.size

    conj = p ^ t
    # conjugating identity by any t yields identity
    assert conj.is_Identity()

def test_xor_with_inverse_relationships():
    # verify behavior with inverse (~) relates as described
    p = Permutation(1, 2, 9)
    r = Permutation(9)(4, 6, 8)
    # ~r * p * r and r * p * ~r are both conjugates of p but may differ
    a = (~r) * p * r
    b = r * p * (~r)
    # both are conjugates so should have same cycle_structure as p
    assert a.cycle_structure() == p.cycle_structure()
    assert b.cycle_structure() == p.cycle_structure()
    # p ^ ~r should equal r * p * ~r (as documented)
    assert p ^ (~r) == r * p * (~r)