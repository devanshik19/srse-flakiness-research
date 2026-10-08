import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

def test_next_nonlex_basic_and_sequence():
    # ensure print formatting doesn't affect equality/representation tests
    Permutation.print_cyclic = False

    # A small permutation where next_nonlex exists
    p = Permutation([2, 0, 3, 1])
    # verify current rank in nonlex order
    r = p.rank_nonlex()
    assert isinstance(r, int)
    # next_nonlex should advance rank by 1
    next_p = p.next_nonlex()
    assert isinstance(next_p, Permutation)
    assert next_p.rank_nonlex() == r + 1
    # Confirm that the returned permutation is what unrank_nonlex would produce
    expected = Permutation.unrank_nonlex(p.size, r + 1)
    assert next_p == expected

    # Check representation / array_form consistency
    assert next_p.array_form == expected.array_form

def test_next_nonlex_at_last_permutation_returns_none():
    # For a given size, the last nonlex permutation (rank = ifac(n)-1) should return None
    for n in range(1, 6):
        # construct the last permutation by unranking the last index
        last_rank = ifac(n) - 1
        last_perm = Permutation.unrank_nonlex(n, last_rank)
        assert last_perm.rank_nonlex() == last_rank
        assert last_perm.next_nonlex() is None

def test_next_nonlex_consistency_over_full_cycle():
    # For a moderate size, walk through all permutations using next_nonlex
    n = 4
    # start from the first permutation (rank 0)
    p = Permutation.unrank_nonlex(n, 0)
    visited = {p.rank_nonlex(): p}
    current = p
    count = 1
    # iterate using next_nonlex until it returns None
    while True:
        nxt = current.next_nonlex()
        if nxt is None:
            break
        # ranks should be strictly increasing by 1
        assert nxt.rank_nonlex() == current.rank_nonlex() + 1
        visited[nxt.rank_nonlex()] = nxt
        current = nxt
        count += 1

    # Total visited should equal total permutations (ifac(n))
    assert count == ifac(n)
    # verify that unranking any rank produces the same permutation we visited
    for r in range(ifac(n)):
        assert visited[r] == Permutation.unrank_nonlex(n, r)

def test_next_nonlex_edge_cases_singleton_and_two():
    # n = 1: only one permutation, next_nonlex should be None
    p1 = Permutation.unrank_nonlex(1, 0)
    assert p1.size == 1
    assert p1.next_nonlex() is None

    # n = 2: two permutations; test both transitions
    p0 = Permutation.unrank_nonlex(2, 0)
    p1 = Permutation.unrank_nonlex(2, 1)
    assert p0.next_nonlex() == p1
    assert p1.next_nonlex() is None