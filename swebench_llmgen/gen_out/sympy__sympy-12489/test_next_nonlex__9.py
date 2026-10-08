import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

def test_next_nonlex_basic_sequence():
    # Setup: a known permutation and its next in nonlex order.
    # Use a 4-element permutation as in the docstring example.
    p = Permutation([2, 0, 3, 1])
    # Ensure rank_nonlex exists and gives expected starting rank (from docstring example)
    r = p.rank_nonlex()
    assert isinstance(r, int)
    # Next in nonlex should exist and have rank r+1
    nxt = p.next_nonlex()
    assert isinstance(nxt, Permutation)
    assert nxt.rank_nonlex() == r + 1
    # Verify the actual array form matches the docstring example
    assert nxt.array_form == [3, 0, 1, 2]

def test_next_nonlex_last_returns_none():
    # For a given size n, the last permutation in nonlex order has rank ifac(n)-1
    # Build the last permutation by unranking that rank.
    n = 5
    last_rank = ifac(n) - 1
    last = Permutation.unrank_nonlex(n, last_rank)
    assert last.rank_nonlex() == last_rank
    assert last.next_nonlex() is None

def test_next_nonlex_iterates_through_all():
    # For a small size (3), iterate through all permutations using next_nonlex
    n = 3
    # Start at rank 0
    cur = Permutation.unrank_nonlex(n, 0)
    seen = [cur.array_form[:]]
    rank = 0
    while True:
        nxt = cur.next_nonlex()
        if nxt is None:
            break
        rank += 1
        assert nxt.rank_nonlex() == rank
        seen.append(nxt.array_form[:])
        cur = nxt
    # There should be factorial(n) permutations seen
    assert rank + 1 == ifac(n)
    # Check uniqueness and coverage: seen should contain all permutations of range(n)
    seen_sets = {tuple(x) for x in seen}
    assert len(seen_sets) == ifac(n)
    expected = {tuple(Permutation.unrank_nonlex(n, r).array_form) for r in range(ifac(n))}
    assert seen_sets == expected

def test_next_nonlex_on_identity_and_random():
    # Identity permutation: rank 0, next should be rank 1 (if size > 1)
    id2 = Permutation(list(range(2)))
    assert id2.rank_nonlex() == 0
    nxt = id2.next_nonlex()
    assert (nxt is None) == (ifac(id2.size) == 1)
    if nxt is not None:
        assert nxt.rank_nonlex() == 1

    # Random check: pick a size 4 and a random rank, ensure next increments rank unless last
    size = 4
    import random
    r = random.randrange(0, ifac(size))
    perm = Permutation.unrank_nonlex(size, r)
    nxt = perm.next_nonlex()
    if r == ifac(size) - 1:
        assert nxt is None
    else:
        assert nxt is not None
        assert nxt.rank_nonlex() == r + 1