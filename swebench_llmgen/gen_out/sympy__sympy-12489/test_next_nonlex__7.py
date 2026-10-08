import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

def test_next_nonlex_basic_sequence():
    # Set print flag to stable representation (not strictly required for functionality)
    Permutation.print_cyclic = False

    # Create a permutation and get its nonlex rank
    p = Permutation([2, 0, 3, 1])
    r = p.rank_nonlex()
    # Ensure rank matches documented example (sanity)
    assert isinstance(r, int)
    # next_nonlex should return the permutation with rank r+1
    next_p = p.next_nonlex()
    assert isinstance(next_p, Permutation)
    assert next_p == Permutation.unrank_nonlex(p.size, r + 1)
    # Check that applying rank_nonlex on the next gives incremented rank
    assert next_p.rank_nonlex() == r + 1

def test_next_nonlex_sequence_until_end():
    # Iterate through all permutations of a small size using next_nonlex
    n = 4
    # Start from the first permutation in nonlex order (rank 0)
    current = Permutation.unrank_nonlex(n, 0)
    seen = [current]
    # Walk through using next_nonlex until it returns None
    while True:
        nxt = current.next_nonlex()
        if nxt is None:
            break
        # ranks should be strictly increasing by 1
        assert nxt.rank_nonlex() == current.rank_nonlex() + 1
        seen.append(nxt)
        current = nxt
    # Number of permutations should be factorial(n)
    assert len(seen) == ifac(n)
    # The final permutation should have the maximal rank
    final_rank = current.rank_nonlex()
    assert final_rank == ifac(n) - 1
    # next_nonlex on the last permutation returns None
    assert current.next_nonlex() is None

def test_next_nonlex_on_last_returns_none():
    n = 3
    last = Permutation.unrank_nonlex(n, ifac(n) - 1)
    assert last.rank_nonlex() == ifac(n) - 1
    assert last.next_nonlex() is None

def test_next_nonlex_preserves_size_and_structure():
    # Ensure that next_nonlex returns a permutation of the same size
    p = Permutation([1, 0, 2])  # size 3
    nxt = p.next_nonlex()
    if nxt is not None:
        assert nxt.size == p.size
        # array forms must be permutations of same elements
        assert sorted(nxt.array_form) == sorted(p.array_form)
    else:
        # If p was the last, ensure it really was the last
        assert p.rank_nonlex() == ifac(p.size) - 1