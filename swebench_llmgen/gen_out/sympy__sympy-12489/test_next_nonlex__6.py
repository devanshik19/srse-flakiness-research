import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

def test_next_nonlex_middle_and_end():
    # Ensure print_cyclic doesn't affect representation results
    Permutation.print_cyclic = False

    # Create a permutation and get its nonlex rank
    p = Permutation([2, 0, 3, 1])
    r = p.rank_nonlex()
    # sanity check: computed rank matches example in docstring (5)
    assert isinstance(r, int)
    assert r == 5

    # next_nonlex should return the permutation with rank r+1
    p_next = p.next_nonlex()
    assert isinstance(p_next, Permutation)
    assert p_next == Permutation.unrank_nonlex(p.size, r + 1)
    # check that rank increased by exactly 1
    assert p_next.rank_nonlex() == r + 1

    # Walk forward from first permutation up to last using next_nonlex
    size = 4
    # start at rank 0
    cur = Permutation.unrank_nonlex(size, 0)
    max_rank = ifac(size) - 1
    ranks_seen = [cur.rank_nonlex()]
    count = 0
    while True:
        nxt = cur.next_nonlex()
        count += 1
        if nxt is None:
            break
        ranks_seen.append(nxt.rank_nonlex())
        cur = nxt
        # avoid infinite loop in case of bug
        assert count <= max_rank + 2
    # we should have visited all ranks from 0..max_rank
    assert ranks_seen[0] == 0
    assert ranks_seen[-1] == max_rank
    assert len(ranks_seen) == max_rank + 1
    assert ranks_seen == list(range(0, max_rank + 1))

def test_next_nonlex_on_last_returns_none():
    size = 3
    max_rank = ifac(size) - 1
    last = Permutation.unrank_nonlex(size, max_rank)
    assert last.rank_nonlex() == max_rank
    assert last.next_nonlex() is None

def test_next_nonlex_singleton_and_identity():
    # singleton permutation (size 1) should have no next
    p1 = Permutation([0])
    assert p1.rank_nonlex() == 0
    assert p1.next_nonlex() is None

    # identity of size 2 should have a next (since 2! = 2)
    pid2 = Permutation([0,1])
    assert pid2.rank_nonlex() == 0
    nxt = pid2.next_nonlex()
    assert isinstance(nxt, Permutation)
    assert nxt.rank_nonlex() == 1
    # then next of that should be None
    assert nxt.next_nonlex() is None