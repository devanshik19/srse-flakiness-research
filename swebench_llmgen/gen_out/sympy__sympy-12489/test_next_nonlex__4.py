import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

def test_next_nonlex_basic_progression():
    # Ensure next_nonlex moves to the next rank_nonlex and returns correct permutation
    # We'll test on size 4 permutations
    size = 4
    # Start with identity permutation which should have rank_nonlex 0
    p = Permutation(list(range(size)))
    assert p.rank_nonlex() == 0
    nxt = p.next_nonlex()
    assert nxt is not None
    assert isinstance(nxt, Permutation)
    # rank should be incremented by 1
    assert nxt.rank_nonlex() == 1
    # iterate through all permutations using next_nonlex and check ranks increase
    current = p
    seen = [current]
    while True:
        n = current.next_nonlex()
        if n is None:
            break
        # Each successive permutation should have rank increased by 1
        assert n.rank_nonlex() == current.rank_nonlex() + 1
        seen.append(n)
        current = n
    # The number of permutations seen should equal ifac(size) (factorial)
    assert len(seen) == ifac(size)

def test_next_nonlex_last_returns_none_and_unrank_consistency():
    # For a given size, the permutation with maximum nonlex rank should return None
    size = 5
    max_rank = ifac(size) - 1
    last = Permutation.unrank_nonlex(size, max_rank)
    assert last.rank_nonlex() == max_rank
    assert last.next_nonlex() is None

    # Also check that unranking rank 0 gives the identity and next_nonlex is consistent
    first = Permutation.unrank_nonlex(size, 0)
    assert first.rank_nonlex() == 0
    second = first.next_nonlex()
    assert second is not None
    assert second.rank_nonlex() == 1
    # ensure unrank_nonlex produces permutations whose rank_nonlex matches the rank used
    for r in [0, 1, max_rank]:
        perm = Permutation.unrank_nonlex(size, r)
        assert perm.rank_nonlex() == r

def test_next_nonlex_on_nonstandard_permutation_forms():
    # Test with a permutation given in array form that's neither identity nor last
    p = Permutation([2, 0, 3, 1])  # example from docstring
    r = p.rank_nonlex()
    nxt = p.next_nonlex()
    assert nxt is not None
    assert nxt.rank_nonlex() == r + 1
    # Confirm that calling next_nonlex repeatedly reaches None at end
    current = p
    count = 0
    while current is not None:
        current = current.next_nonlex()
        count += 1
        # prevent infinite loops in case of bug
        assert count <= ifac(p.size)
    # final count should be <= factorial and >= 1
    assert 1 <= count <= ifac(p.size)

def test_next_nonlex_type_and_immutability():
    # Ensure next_nonlex does not mutate the original permutation
    p = Permutation([1, 2, 0])
    original_af = p.array_form.copy()
    nxt = p.next_nonlex()
    # original array form remains unchanged
    assert p.array_form == original_af
    if nxt is not None:
        # next is a different object (not the same instance)
        assert nxt is not p
        # their array forms should differ (since rank increased)
        assert nxt.array_form != p.array_form