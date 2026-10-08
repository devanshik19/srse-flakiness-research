import pytest
from sympy.combinatorics.permutations import Permutation

# Helper to construct permutation from array form using Permutation._af_new if available,
# otherwise use the public constructor with list (Permutation accepts a list to create)
def make_perm_from_array(arr):
    try:
        # Some sympy versions expose _af_new as classmethod
        return Permutation._af_new(arr)
    except Exception:
        # Fallback: Permutation can be constructed from list/sequence
        return Permutation(arr)

def array_of(perm):
    # access protected field for test inspection
    return perm._array_form

def test_mul_inv_identity_and_simple_cycle():
    # identity permutation
    id_perm = Permutation(list(range(5)))
    # simple 3-cycle on 0..4 (0->1,1->2,2->0,3->3,4->4)
    p = make_perm_from_array([1,2,0,3,4])
    # mul_inv computes other * ~self, so if other is identity, result should be inverse of self
    res = id_perm.mul_inv(p)
    # inverse of [1,2,0,3,4] is [2,0,1,3,4]
    assert isinstance(res, Permutation)
    assert array_of(res) == [2,0,1,3,4]

    # Now other is p and self is p, so result should be p * ~p = identity
    res2 = p.mul_inv(p)
    assert array_of(res2) == list(range(5))

def test_mul_inv_nontrivial_operands():
    # Permutation a: swap 0<->1, 2->3->4->2 (a 3-cycle on 2,3,4)
    a = make_perm_from_array([1,0,3,4,2])
    # Permutation b: rotate everything right by 1: i -> i-1 mod 5
    b = make_perm_from_array([4,0,1,2,3])

    # compute expected: b * ~a
    # get inverse of a
    ainv = make_perm_from_array([1,0,4,2,3])  # manually computed inverse of a
    # multiply arrays: we need to compute composition b o ainv (apply ainv then b)
    def compose(x, y):
        # x and y are array forms where mapping i -> x[i]
        n = len(x)
        return [x[y[i]] for i in range(n)]

    expected_arr = compose(b._array_form, ainv._array_form)
    res = a.mul_inv(b)  # note mul_inv is other * ~self
    assert array_of(res) == expected_arr

def test_mul_inv_different_sizes_and_errors():
    # permutations of different sizes should raise or handle appropriately.
    small = make_perm_from_array([1,0])  # size 2
    large = make_perm_from_array([1,2,0,3])  # size 4
    # Depending on sympy version behavior, operation across different sizes may raise ValueError
    # or produce a permutation by interpreting smaller as extended identity. We assert one of those.
    try:
        _ = small.mul_inv(large)
    except ValueError:
        pass
    except Exception as exc:
        # allow TypeError or IndexError as alternative failure modes
        assert isinstance(exc, (TypeError, IndexError))
    else:
        # If no error, result must be a Permutation
        res = small.mul_inv(large)
        assert isinstance(res, Permutation)
        # Ensure that the resulting array has length at least max of inputs
        assert len(res._array_form) >= max(len(small._array_form), len(large._array_form))

def test_mul_inv_with_identity_other_and_various_self():
    # Test many random permutations to exercise branches
    import random
    for n in range(1, 6):
        for _ in range(10):
            seq = list(range(n))
            random.shuffle(seq)
            selfp = make_perm_from_array(seq)
            other = Permutation(list(range(n)))  # identity of size n
            res = selfp.mul_inv(other)
            # res should equal other * ~self = identity * inverse(self) = inverse(self)
            # compute inverse directly
            inv = [0]*n
            for i, v in enumerate(selfp._array_form):
                inv[v] = i
            assert res._array_form == inv