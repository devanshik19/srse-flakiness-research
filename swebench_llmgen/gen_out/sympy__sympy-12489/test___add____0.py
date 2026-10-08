import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy import Basic

def test_add_basic_and_identity():
    # identity plus a permutation by adding its rank should return the permutation
    Perm.print_cyclic = False
    I = Perm([0, 1, 2, 3])
    a = Perm([2, 1, 3, 0])
    # Ensure rank and cardinality behave as expected
    r = a.rank()
    assert isinstance(r, int)
    assert I.cardinality == a.cardinality
    # Using __add__: I + a.rank() should equal a
    res = I + r
    assert res == a
    # Also test adding with object that is int-like modulo cardinality:
    # rank + cardinality should wrap around to same permutation
    res2 = I + (r + I.cardinality)
    assert res2 == a
    # Adding zero should give identity
    assert I + 0 == I

def test_add_returns_fresh_permutation_and_sets__rank():
    # Construct a permutation and add an offset to it
    p = Perm([1, 0, 2])  # size 3
    # Save original to ensure returned is not the same object (fresh instance)
    original_id = id(p)
    new_rank = (p.rank() + 1) % p.cardinality
    q = p + 1
    assert isinstance(q, Perm)
    assert id(q) != original_id  # new object
    # Confirm internal _rank attribute set to computed rank
    assert hasattr(q, "_rank")
    assert q._rank == new_rank
    # Check that unranking the size with that rank yields the same array_form
    expected = Perm.unrank_lex(p.size, new_rank)
    assert q.array_form == expected.array_form

def test_add_wraps_mod_cardinality_and_handles_large_ints():
    p = Perm([2, 0, 1, 3])  # size 4
    # large add value wraps by cardinality
    add_value = p.cardinality * 3 + 2
    q = p + add_value
    # Equivalent to adding add_value % cardinality
    expected = p + (add_value % p.cardinality)
    assert q == expected

def test_add_with_non_int_like_raises_attribute_error_or_typeerror():
    p = Perm([0, 1])
    # The implementation expects other to be usable with % and int math.
    # Passing an object without these should raise; accept either TypeError or AttributeError.
    class Bad:
        pass
    with pytest.raises((TypeError, AttributeError)):
        _ = p + Bad()

def test_add_full_range_matches_unrank_lex():
    # For a small size, test all possible additive offsets produce correct permutations
    size = 3
    base = Perm(list(range(size)))  # identity
    total = base.cardinality
    seen = set()
    for k in range(total):
        res = base + k
        # Ensure array_form is as produced by unrank_lex
        expected = Perm.unrank_lex(size, k)
        assert res.array_form == expected.array_form
        seen.add(tuple(res.array_form))
    # All permutations should be seen exactly once
    assert len(seen) == total