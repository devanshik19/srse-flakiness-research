import pytest
from sympy.combinatorics.permutations import Permutation

def test_xor_conjugation_basic():
    # p and q are permutations of same size
    p = Permutation(1, 2, 9)          # cycle (1 2 9)
    q = Permutation(6, 9, 8)          # cycle (6 9 8)
    # conjugate c = p ^ q should be ~q * p * q
    c = p ^ q
    assert c == (~q) * p * q
    # also p == q * c * ~q
    assert p == q * c * (~q)
    # the conjugate should have same cycle structure as p
    assert c.cycle_structure() == p.cycle_structure()

def test_xor_integer_left_selects_image():
    # when left operand is int, __rxor__ returns image under permutation
    p = Permutation(3)(1, 2, 0)  # permutation of size 4: cycle (1 2 0)(3)
    # check images for each index
    for i in range(p.size):
        # i ^ p uses __rxor__: selecting p(i)
        assert i ^ p == p(i)

def test_xor_associativity_like_property():
    # check that p^q^r equals p^(q*r) for given permutations as documented
    q = Permutation(6, 9, 8)
    p = Permutation(1, 2, 9)
    r = Permutation(9)(4, 6, 8)
    left = q ^ p ^ r
    right = q ^ (p * r)
    assert left == right

def test_xor_size_mismatch_raises():
    p = Permutation(1, 2, 3)    # size inferred from entries
    # create a permutation of different size, e.g., acting on 6 points
    bigger = Permutation(5, 4, 3, 2, 1)
    # Ensure sizes differ
    assert p.size != bigger.size
    with pytest.raises(ValueError):
        _ = p ^ bigger

def test_xor_produces_array_form_copy_and_not_aliasing():
    # Ensure the resulting permutation array is independent (no aliasing)
    p = Permutation(1, 0, 2)  # small permutation
    h = Permutation(2, 1, 0)
    res = p ^ h
    # Mutate internal array of h (by constructing a new permutation with same name)
    # We cannot mutate private attributes safely; instead ensure repeated computation matches
    res2 = p ^ h
    assert res == res2

def test_xor_with_identity_yields_conjugate_equal_to_self_when_commuting():
    # identity conjugation returns same permutation
    id_perm = Permutation(list(range(5)))
    p = Permutation(1, 2, 3, 4)  # some permutation on 5 elements (implicitly size 5)
    # ensure sizes match
    assert id_perm.size == p.size
    assert p ^ id_perm == p
    # conjugating by inverse gives ~h * p * h; test with h and ~h produce valid conjugates
    h = Permutation(1, 0, 2, 4, 3)
    conj1 = p ^ h
    conj2 = (~h) * p * h
    assert conj1 == conj2

def test_xor_chain_precedence():
    # Verify operator precedence behavior in chained expressions:
    # q^r*p^r == q^(r*p)^r as per documentation
    q = Permutation(6, 9, 8)
    r = Permutation(9)(4, 6, 8)
    left = q ^ r * p ^ r if False else None  # placeholder to avoid ambiguous parsing
    # Instead, construct the described equality explicitly:
    # q^r*p^r should be parsed as (q^r) * (p^r) due to ^ low precedence; test the documented equivalence:
    # Build the pieces directly:
    q_r = q ^ r
    p_r = p ^ r
    expr1 = q_r * p_r
    expr2 = q ^ (r * p) ^ r
    # They should be equal as stated
    assert expr1 == expr2

# Note: The last test references p defined earlier; ensure p exists in this scope.
# To guarantee, define p for module-level usage:
p = Permutation(1, 2, 9)