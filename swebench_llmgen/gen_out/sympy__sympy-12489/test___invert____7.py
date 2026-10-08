import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_basic_array_form():
    # simple permutation given as array-form via nested lists in constructor
    p = Permutation([[2, 0], [3, 1]])  # should create [2,0,3,1]
    inv = ~p
    # inverse of [2,0,3,1] is [1->0,0->2,2->3,3->1] -> [1,0,3,2]? verify by composition
    # Confirm that p * inv and inv * p yield the identity
    identity = Permutation(list(range(p.size())))
    assert p * inv == identity
    assert inv * p == identity
    # also check that ~p equals p**-1
    assert inv == p**-1

def test_invert_identity_and_even_odd():
    # identity permutation should invert to itself
    id_perm = Permutation(list(range(5)))
    assert ~id_perm == id_perm
    # a single transposition invert equals itself
    trans = Permutation([1, 0, 2, 3])
    assert ~trans == trans
    # check parity unaffected: inverse has same parity as original
    assert trans.is_odd() == (~trans).is_odd()
    assert id_perm.is_even() == (~id_perm).is_even()

def test_invert_support_and_repr_preserved():
    p = Permutation([2, 3, 0, 1])
    inv = ~p
    # support should match (non-fixed points)
    assert set(p.support()) == set(inv.support())
    # string representation for invert should be a Permutation repr
    assert repr(inv).startswith("Permutation(")
    # confirm elements mapping: applying permutation then inverse returns same elements
    arr = list(range(p.size()))
    mapped_then_inverted = [inv[p[i]] for i in arr]
    assert mapped_then_inverted == arr

def test_invert_random_small_permutations():
    # test several random permutations for correctness of inverse property
    import random
    for n in range(1, 6):
        for _ in range(20):
            seq = list(range(n))
            random.shuffle(seq)
            p = Permutation(seq)
            inv = ~p
            # compose to check identity
            assert p * inv == Permutation(list(range(n)))
            assert inv * p == Permutation(list(range(n)))
            # checking that applying p then inv gives original positions
            for i in range(n):
                assert inv[p[i]] == i
                assert p[inv[i]] == i

def test_invert_consistency_with_pow_negative_one():
    # ensure ~p equals p**-1 for a variety including larger size
    p = Permutation([3, 0, 4, 1, 2])
    assert ~p == p**-1

def test_invert_raises_on_invalid_internal_structure():
    # construct a Permutation and tamper with its _array_form to simulate bad state
    p = Permutation([0,1,2])
    # monkeypatching the internal array to a wrong length should still let __invert__ attempt invert:
    p._array_form = [0, 1]  # invalid for size 3
    # Depending on implementation this may raise; assert that it raises an Exception to catch incorrect internal state
    with pytest.raises(Exception):
        _ = ~p