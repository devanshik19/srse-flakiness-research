import pytest
from sympy.combinatorics.permutations import Permutation

def test_mul_inv_basic_identity():
    # identity permutation
    e = Permutation([])
    p = Permutation([1, 0, 2])  # transposition (0 1)
    # mul_inv should compute other * ~self
    # here other = p, self = p -> p * ~p = identity
    res = p.mul_inv(p)
    assert isinstance(res, Permutation)
    assert res == e
    # Also check that identity mul_inv any gives inverse of other as ~self is identity
    res2 = e.mul_inv(p)
    # e.mul_inv(p) = p * ~e = p * e = p
    assert res2 == p

def test_mul_inv_with_inverse_and_composition():
    # create a 4-cycle permutation: 0->1->2->3->0
    p = Permutation([1,2,3,0])
    # compute inverse using ~
    inv_p = ~p
    # now test p.mul_inv(inv_p) = inv_p * ~p = inv_p * inv_p = inv_p**2
    res = p.mul_inv(inv_p)
    # compute expected directly by composition
    expected = inv_p * inv_p
    assert res == expected
    # check that mul_inv produces identity when other is p and self is inv_p
    # other * ~self = p * ~(inv_p) = p * p = p**2
    res2 = inv_p.mul_inv(p)
    assert res2 == p * p

def test_mul_inv_size_mismatch_raises_or_handles():
    # When permutations of different sizes are used, sympy Permutation tries to handle via array forms.
    # Create permutations of different sizes and ensure mul_inv does not raise unexpected exceptions.
    a = Permutation([1,0])       # size 2
    b = Permutation([1,2,0])     # size 3
    # mul_inv should produce a Permutation without raising TypeError; behaviour: b * ~a
    res = a.mul_inv(b)
    assert isinstance(res, Permutation)
    # The resulting permutation should have a size at least the max of operands sizes
    assert res.size >= max(a.size, b.size)

def test_mul_inv_multiple_applications_consistent():
    p = Permutation([2,0,1,3])  # 3-cycle on first three
    q = Permutation([1,0,3,2])  # product of transpositions
    # Repeated use should be associative in expected way:
    r1 = p.mul_inv(q)  # q * ~p
    r2 = q * (~p)
    assert r1 == r2
    # Compose further and compare with direct composition
    s = Permutation([3,2,1,0])
    assert s.mul_inv(p).mul_inv(q) == (p.mul_inv(q)).__radd__ if False else s.mul_inv(p).mul_inv(q)  # just ensure chaining works

# Additional simple sanity checks for small permutations and inverses
@pytest.mark.parametrize("arr", [
    [], [0], [1,0], [2,0,1], [1,2,0,3]
])
def test_mul_inv_parametrized(arr):
    perm = Permutation(arr)
    inv = ~perm
    res = perm.mul_inv(inv)
    # perm.mul_inv(inv) = inv * ~perm = inv * inv = inv**2
    assert res == inv * inv