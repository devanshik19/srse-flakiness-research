import pytest
from sympy.combinatorics.permutations import Permutation

def test_invert_simple_cycle():
    # 2-cycle (swap 0 and 1)
    p = Permutation([1,0])
    inv = ~p
    # inverse of swap is itself
    assert isinstance(inv, Permutation)
    assert inv.array_form == [1,0]
    # multiplication yields identity
    assert (p * inv).array_form == [0,1]
    assert (inv * p).array_form == [0,1]

def test_invert_multiple_cycles():
    # permutation given in cycle pairs: [[2,0],[3,1]] corresponds to mapping 0->2,1->3,2->0,3->1
    p = Permutation([[2,0],[3,1]])
    inv = ~p
    # expected inverse mapping swaps back: 0->2 means inverse sends 2->0 etc.
    assert inv.array_form == [2,3,0,1]
    # check p times inv and inv times p are identity
    identity = Permutation(list(range(4)))
    assert (p * inv) == identity
    assert (inv * p) == identity
    # also check that ~p equals p**-1
    assert inv == p**-1

def test_invert_identity():
    # identity permutation should be its own inverse
    id4 = Permutation(list(range(4)))
    assert (~id4) == id4
    assert (id4 * ~id4).array_form == id4.array_form

def test_invert_edge_cases_singleton_empty():
    # singleton
    s = Permutation([0])
    assert (~s).array_form == [0]
    # larger identity via empty cycle input (some constructors accept [])
    i = Permutation(list(range(1)))
    assert (~i).array_form == [0]

def test_invert_composed():
    # compose two permutations and invert: ~(a*b) == ~b * ~a
    a = Permutation([2,0,1])  # sends 0->2,1->0,2->1
    b = Permutation([1,2,0])  # sends 0->1,1->2,2->0
    composed = a * b
    inv_composed = ~composed
    # inverse of composition is reverse composition of inverses
    assert inv_composed == (~b) * (~a)
    # verify multiplied gives identity
    assert (composed * inv_composed).array_form == [0,1,2]

def test_invert_type_and_hash_behavior():
    # ensure result is a Permutation and behaves consistently for hashing/equality
    p = Permutation([3,0,1,2])
    inv = ~p
    assert isinstance(inv, Permutation)
    # equality with another construction of same inverse
    explicit_inv = Permutation(inv.array_form)
    assert inv == explicit_inv
    # check that double invert returns original
    assert ~~p == p

def test_invert_preserves_size_and_support():
    p = Permutation([2,3,0,1])
    inv = ~p
    assert p.size == inv.size
    # support should match
    assert set(p.support()) == set(inv.support())

# Run tests if module executed directly
if __name__ == "__main__":
    pytest.main([__file__])