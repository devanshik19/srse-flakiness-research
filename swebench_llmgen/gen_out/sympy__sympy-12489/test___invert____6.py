import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_basic_array_form():
    # simple permutation given as array form in nested cycles-like input
    p = Permutation([[2, 0], [3, 1]])
    inv = ~p
    # inverse should be a Permutation and array form should be correct
    assert isinstance(inv, Permutation)
    # p as array form is [2,3,0,1]; inverse should map 2->0,3->1,0->2,1->3
    assert inv.array_form == [2, 3, 0, 1]  # as shown in the docstring example
    # verify composition p * inv = identity
    identity = Permutation(list(range(p.size)))
    assert p * inv == identity
    assert inv * p == identity
    # check that ~p equals p**-1
    assert inv == p**-1

def test_invert_identity_and_singletons():
    # identity permutation
    e = Permutation([0,1,2,3])
    assert (~e).array_form == e.array_form
    # singleton (size 1) permutation
    s = Permutation([0])
    assert (~s).array_form == [0]
    # empty permutation (size 0) if supported
    empty = Permutation([])
    assert (~empty).array_form == []

def test_invert_random_permutations():
    # test several random permutations for correctness of inverse
    import random
    for n in [1, 2, 5, 7]:
        for _ in range(10):
            arr = list(range(n))
            random.shuffle(arr)
            p = Permutation(arr)
            inv = ~p
            # composing should yield identity
            identity = Permutation(list(range(n)))
            assert p * inv == identity
            assert inv * p == identity
            # double invert returns original
            assert ~(~p) == p

def test_invert_combined_with_other_operations():
    # check inversion interacts correctly with power and multiplication
    p = Permutation([2,0,1,4,3])  # a nontrivial permutation
    inv = ~p
    # p * inv == identity
    assert p * inv == Permutation(list(range(p.size)))
    # inverse of product: ~(p*q) == ~q * ~p
    q = Permutation([1,0,3,2,4])
    left = ~(p * q)
    right = (~q) * (~p)
    assert left == right
    # power: (p**k)**-1 == p**-k
    for k in [-3, -1, 0, 1, 2, 5]:
        assert ~(p**k) == p**(-k)

def test_invert_preserves_cycle_structure_and_support():
    p = Permutation([2,0,1,4,3])
    inv = ~p
    # cycle_structure should match (multiset of cycle lengths)
    assert p.cycle_structure == inv.cycle_structure
    # support (set of moved points) should be the same
    assert set(p.support()) == set(inv.support())

# If Permutation cannot be constructed from some inputs on some versions of sympy,
# make tests robust by skipping with a clear message.
def test_invert_robustness():
    try:
        p = Permutation([[2,0],[3,1]])
    except Exception as e:
        pytest.skip("Permutation construction not supported in this environment: %s" % e)
    inv = ~p
    assert (p * inv).is_Identity()
    assert (inv * p).is_Identity()