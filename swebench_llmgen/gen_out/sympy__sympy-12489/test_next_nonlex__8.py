import pytest
from mpmath.libmp.libintmath import ifac
from sympy.combinatorics.permutations import Permutation as Perm
# Ensure print_cyclic doesn't affect representation tests
Perm.print_cyclic = False

def test_next_nonlex_basic_sequence():
    # Create a permutation and get its nonlex rank
    p = Perm([2, 0, 3, 1])
    r = p.rank_nonlex()
    # Confirm rank as in docstring example
    assert r == 5
    # Get the next permutation in nonlex order
    p_next = p.next_nonlex()
    assert isinstance(p_next, Perm)
    # Check that the rank increased by one
    assert p_next.rank_nonlex() == r + 1
    # The expected array form for the next permutation
    assert p_next.array_form == [3, 0, 1, 2]

def test_next_nonlex_last_returns_none():
    # For size 3, there are ifac(3)=6 permutations; rank ranges 0..5
    # Create the permutation with the maximum nonlex rank and ensure next_nonlex returns None.
    size = 3
    last_rank = ifac(size) - 1
    last_perm = Perm.unrank_nonlex(size, last_rank)
    assert last_perm.rank_nonlex() == last_rank
    assert last_perm.next_nonlex() is None

def test_next_nonlex_iterates_through_all():
    # For a small size iterate through all permutations using next_nonlex
    size = 4
    # Start from rank 0
    current = Perm.unrank_nonlex(size, 0)
    seen = [current.array_form[:]]  # copy
    rank = 0
    while True:
        nxt = current.next_nonlex()
        if nxt is None:
            break
        rank += 1
        # Ensure monotonic rank increase
        assert nxt.rank_nonlex() == rank
        seen.append(nxt.array_form[:])
        current = nxt
    # We should have visited exactly ifac(size) permutations
    assert rank + 1 == ifac(size)
    # Ensure all seen permutations are unique
    # convert to tuple for hashability
    seen_tuples = list(map(tuple, seen))
    assert len(set(seen_tuples)) == len(seen_tuples)

def test_next_nonlex_on_identity():
    # Identity permutation should have rank 0; next_nonlex should be rank 1
    id_perm = Perm(list(range(5)))
    assert id_perm.rank_nonlex() == 0
    nxt = id_perm.next_nonlex()
    assert nxt is not None
    assert nxt.rank_nonlex() == 1

def test_next_nonlex_does_not_mutate_original():
    p = Perm([1, 0, 2])
    p_copy_af = p.array_form[:]  # snapshot
    nxt = p.next_nonlex()
    # original permutation array form unchanged
    assert p.array_form == p_copy_af
    # next permutation is a distinct object (not the same instance)
    if nxt is not None:
        assert nxt is not p

# Run tests when executed as a script (useful for quick checks)
if __name__ == "__main__":
    pytest.main([__file__])