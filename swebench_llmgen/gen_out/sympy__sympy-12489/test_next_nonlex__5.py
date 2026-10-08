import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

def test_next_nonlex_basic_and_sequence():
    # Simple permutation of size 4
    p = Permutation([2, 0, 3, 1])
    # confirm rank_nonlex works and gives expected value for this permutation
    r = p.rank_nonlex()
    assert isinstance(r, int)
    # According to docstring example, rank should be 5
    assert r == 5

    # next_nonlex should return the next permutation in nonlex order
    nxt = p.next_nonlex()
    assert isinstance(nxt, Permutation)
    # Next permutation shown in docstring example
    assert nxt == Permutation([3, 0, 1, 2])
    # rank should be incremented by 1
    assert nxt.rank_nonlex() == r + 1

def test_next_nonlex_last_returns_none():
    # For size 3, construct the last permutation in nonlex order by unranking the max rank
    size = 3
    max_rank = ifac(size) - 1
    last = Permutation.unrank_nonlex(size, max_rank)
    # Ensure last is indeed a Permutation and its rank is max_rank
    assert isinstance(last, Permutation)
    assert last.rank_nonlex() == max_rank
    # next_nonlex of the last should be None
    assert last.next_nonlex() is None

def test_next_nonlex_iterates_through_all():
    # For size 4 iterate through all permutations via next_nonlex from rank 0 to last
    size = 4
    total = ifac(size)
    first = Permutation.unrank_nonlex(size, 0)
    seen = []
    cur = first
    count = 0
    while cur is not None:
        seen.append(tuple(cur.array_form))
        cur = cur.next_nonlex()
        count += 1
        # safety: avoid infinite loop
        assert count <= total + 1
    # We expect to have seen exactly 'total' distinct permutations
    assert len(seen) == total
    # ensure uniqueness
    assert len(set(seen)) == total

def test_next_nonlex_consistent_with_unrank_and_rank():
    # Randomly sample a few ranks for size 5 and ensure next_nonlex matches unrank_nonlex(rank+1)
    size = 5
    total = ifac(size)
    for rank in [0, 1, 5, total - 2]:
        p = Permutation.unrank_nonlex(size, rank)
        expected = Permutation.unrank_nonlex(size, rank + 1)
        # next_nonlex should match expected for non-last ranks
        assert p.next_nonlex() == expected

def test_next_nonlex_edge_case_size_one():
    # For size 1, there's only one permutation; next_nonlex should be None
    p = Permutation([0])
    assert p.rank_nonlex() == 0
    assert p.next_nonlex() is None