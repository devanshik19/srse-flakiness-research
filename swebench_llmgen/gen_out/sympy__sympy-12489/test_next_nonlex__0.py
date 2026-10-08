import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

# Ensure deterministic printing behavior isn't required for comparisons
Permutation.print_cyclic = False

def test_next_nonlex_basic_progression():
    # A known permutation and its next in nonlex order from the docstring example
    p = Permutation([2, 0, 3, 1])
    # confirm rank_nonlex progression as in docstring
    r = p.rank_nonlex()
    assert isinstance(r, int)
    # using next_nonlex should give the documented next permutation
    nxt = p.next_nonlex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [3, 0, 1, 2]
    # rank should increase by 1
    assert nxt.rank_nonlex() == r + 1

def test_next_nonlex_last_returns_none():
    # For size 3, there are ifac(3) = 6 permutations in nonlex order (rank 0..5)
    size = 3
    last_rank = ifac(size) - 1
    # create the last permutation by unranking
    last = Permutation.unrank_nonlex(size, last_rank)
    # sanity: it should have the max rank and next_nonlex should be None
    assert last.rank_nonlex() == last_rank
    assert last.next_nonlex() is None

def test_next_nonlex_all_cycle_through():
    # For small size, iterate through all nonlex permutations using next_nonlex
    size = 4
    # start with rank 0 permutation
    cur = Permutation.unrank_nonlex(size, 0)
    seen = [cur.array_form[:]]
    # iterate until None
    while True:
        cur = cur.next_nonlex()
        if cur is None:
            break
        seen.append(cur.array_form[:])
    # number of permutations seen should equal factorial(size)
    assert len(seen) == ifac(size)
    # all seen array_forms should be unique
    assert len({tuple(a) for a in seen}) == ifac(size)

def test_next_nonlex_does_not_mutate_original():
    p = Permutation([1, 0, 2])
    p_copy = Permutation(p.array_form[:])  # create a separate Permutation with same array
    _ = p.next_nonlex()
    # original should remain equal to the copy
    assert p.array_form == p_copy.array_form

def test_next_nonlex_invalid_behaviour_none_for_singleton():
    # For size 1, there's only one permutation; next_nonlex should be None
    single = Permutation([0])
    assert single.next_nonlex() is None