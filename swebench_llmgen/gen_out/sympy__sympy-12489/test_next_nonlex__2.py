import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

def test_next_nonlex_basic_sequence():
    # Ensure print_cyclic doesn't affect behavior
    Permutation.print_cyclic = False

    # Start with a known permutation and check next_nonlex increments rank_nonlex by 1
    p = Permutation([2, 0, 3, 1])
    r = p.rank_nonlex()
    nxt = p.next_nonlex()
    assert nxt is not None
    assert isinstance(nxt, Permutation)
    assert nxt.rank_nonlex() == r + 1

    # Check that next_nonlex actually returns the expected permutation
    # Based on the docstring example: next of [2,0,3,1] is [3,0,1,2]
    assert nxt.array_form == [3, 0, 1, 2]

def test_next_nonlex_last_returns_none():
    # For size n, there are ifac(n) permutations in nonlex order (factorial)
    # Build the last permutation in nonlex order by unranking with rank = ifac(n)-1
    n = 4
    last = Permutation.unrank_nonlex(n, ifac(n) - 1)
    assert isinstance(last, Permutation)
    # The next_nonlex of the last permutation should be None
    assert last.next_nonlex() is None

def test_next_nonlex_iterate_through_all():
    # Iterate through all permutations of size 3 in nonlex order using next_nonlex
    size = 3
    total = int(ifac(size))
    first = Permutation.unrank_nonlex(size, 0)
    seen = []
    cur = first
    for i in range(total):
        assert cur is not None
        seen.append(tuple(cur.array_form))
        cur = cur.next_nonlex()
    # After total steps, cur should be None (we exhausted all)
    assert cur is None
    # Ensure we have the expected number and uniqueness
    assert len(seen) == total
    assert len(set(seen)) == total

def test_next_nonlex_consistent_with_unrank_rank():
    # For several sizes and ranks, ensure next_nonlex gives the permutation corresponding to rank+1
    for n in (1, 2, 3, 4):
        total = int(ifac(n))
        for r in range(max(0, total - 1)):
            p = Permutation.unrank_nonlex(n, r)
            nxt = p.next_nonlex()
            assert nxt == Permutation.unrank_nonlex(n, r + 1)
        # check last rank returns None
        last = Permutation.unrank_nonlex(n, total - 1)
        assert last.next_nonlex() is None