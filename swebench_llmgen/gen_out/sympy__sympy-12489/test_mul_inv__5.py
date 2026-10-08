import pytest
from sympy.combinatorics.permutations import Permutation

# Helper to build Permutation from array form using internal API exposed as constructor via list()
# Permutation(list) constructs permutation mapping positions 0..n-1 to given image list.
# We will construct permutations by giving their array_form (0-based).

def test_mul_inv_basic_identity():
    # identity permutation of size 4
    id4 = Permutation(list(range(4)))
    # some permutation p
    p = Permutation([2, 0, 3, 1])  # mapping: 0->2,1->0,2->3,3->1
    # mul_inv computes other * ~self where ~self is inverse of self
    # So p.mul_inv(id4) should be id4 * ~p == ~p
    inv_p = ~p
    res = p.mul_inv(id4)
    assert isinstance(res, Permutation)
    assert res == inv_p

def test_mul_inv_composition_matches_manual():
    # Define two permutations a and b
    a = Permutation([1, 2, 0, 4, 3])  # 0->1,1->2,2->0,3->4,4->3
    b = Permutation([2, 0, 4, 3, 1])  # 0->2,1->0,2->4,3->3,4->1

    # mul_inv computes other * ~self
    res = a.mul_inv(b)

    # Compute expected by manual composition: b * inverse(a)
    inv_a = ~a
    expected = b * inv_a

    assert res == expected
    # also check that result's array form matches explicit array composition
    # array form of composition: apply inverse(a) then b
    arr_inv_a = inv_a.array_form
    arr_b = b.array_form
    # compute composition c(i) = b(inv_a(i))
    manual = [arr_b[arr_inv_a[i]] for i in range(len(arr_inv_a))]
    assert res.array_form == manual

def test_mul_inv_with_self_inverse():
    # permutation that is its own inverse (transposition and fixed points)
    s = Permutation([1, 0, 2, 3])  # swap 0 and 1
    # then ~s == s, so s.mul_inv(s) == s * ~s == s * s == identity
    res = s.mul_inv(s)
    assert res.is_Identity() or res == Permutation(list(range(s.size())))

def test_mul_inv_different_sizes_raises_or_handles():
    # If sizes mismatch, behavior may be to raise or to handle via array forms.
    # Create permutations of different sizes and assert composition raises or returns a Permutation.
    a = Permutation([1, 0, 2])  # size 3
    b = Permutation([1, 0, 2, 3])  # size 4

    # The implementation uses internal array forms directly; ensure it does not crash.
    try:
        res = a.mul_inv(b)
    except Exception as e:
        # If sympy raises a ValueError or IndexError for mismatched sizes, that's acceptable.
        assert isinstance(e, (ValueError, IndexError))
    else:
        # If it returns a permutation, verify type and basic consistency:
        assert isinstance(res, Permutation)
        # result size should be at least max of operand sizes
        assert res.size() >= max(a.size(), b.size())

def test_mul_inv_with_identity_other():
    # other is identity; result should be identity * ~self == ~self
    s = Permutation([3, 0, 1, 2])
    identity = Permutation(list(range(s.size())))
    res = s.mul_inv(identity)
    assert res == ~s