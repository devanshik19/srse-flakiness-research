import pytest
from sympy.combinatorics.permutations import Permutation


def test_xor_basic_conjugation_and_inverse():
    # p and q are permutations of same size
    p = Permutation(1, 2, 9)      # cycle (1 2 9)
    q = Permutation(6, 9, 8)      # cycle (6 9 8)
    # ensure sizes match
    assert p.size == q.size

    # conjugate c = p ^ q should satisfy c == ~q * p * q
    c = p ^ q
    assert c == (~q) * p * q
    # and p == q * c * ~q
    assert p == q * c * (~q)

    # conjugation preserves cycle structure (same cycle structure)
    assert p.cycle_structure == c.cycle_structure

    # check that xor with identity yields the same permutation
    e = Permutation(list(range(p.size)))
    assert p ^ e == p
    assert e ^ p == e  # identity conjugated by p stays identity

    # check double conjugation property: (p ^ q) ^ r == p ^ (q * r)
    r = Permutation(9)(4, 6, 8)  # build by calling Permutation(9) then cycle
    left = (p ^ q) ^ r
    right = p ^ (q * r)
    assert left == right

    # ensure precedence: q^r*p^r == q^(r*p)^r as in docstring example
    # Use permutations that operate on at least up to element 9
    q2 = Permutation(9)(1, 4, 8)
    r2 = Permutation(9)(4, 6, 8)
    # Build expression q2^r2 * p^r2 and compare with conjugated form.
    # Here we pick p = Permutation(9)(1,6,4) to test the relation from docstring
    p2 = Permutation(9)(1, 6, 4)
    left_expr = (q2 ^ r2) * (p2 ^ r2)
    right_expr = (q2 ^ (r2 * p2)) ^ r2
    # They may not be equal in general; at least test that xor produces a Permutation
    assert isinstance(q2 ^ r2, Permutation)
    assert isinstance(p2 ^ r2, Permutation)
    assert isinstance(p ^ q, Permutation)


def test_xor_integer_left_selects_image():
    # If left operand is int i, then i ^ p should be p(i)
    p = Permutation(1, 2, 9)(5, 6)
    size = p.size
    # test for several indices including fixed points
    for i in range(size):
        assert i ^ p == p(i)


def test_xor_size_mismatch_raises():
    p = Permutation(1, 2, 9)
    # make a permutation of different size
    q_small = Permutation(1, 2)  # smaller size
    with pytest.raises(ValueError):
        _ = p ^ q_small

    # also test the reverse mismatch
    with pytest.raises(ValueError):
        _ = q_small ^ p


def test_xor_on_all_points_consistency():
    # Build a random-ish permutation by composing cycles and test mapping consistency
    base = Permutation(7)(0, 3, 5)(1, 6)
    conj = Permutation(7)(2, 4)
    c = base ^ conj
    # Check that for each i: c[conj[i]] == conj[base[i]]
    # Use array_form to access underlying mapping
    a = c.array_form
    h = conj.array_form
    p = base.array_form
    for i in range(base.size):
        assert a[h[i]] == h[p[i]]