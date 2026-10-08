import pytest
from sympy.combinatorics.permutations import Permutation
from mpmath.libmp.libintmath import ifac

def test_next_nonlex_basic_and_end():
    # Setup: small permutation
    Permutation.print_cyclic = False

    p = Permutation([2, 0, 3, 1])
    # Verify rank_nonlex works and is as in docstring example
    r = p.rank_nonlex()
    assert isinstance(r, int)
    # Check next_nonlex returns a Permutation and increases rank by 1
    next_p = p.next_nonlex()
    assert isinstance(next_p, Permutation)
    assert next_p.array_form != p.array_form
    assert next_p.rank_nonlex() == r + 1

    # Walk forward from the first permutation (rank 0) through all permutations
    size = p.size
    total = ifac(size)
    # start at rank 0
    cur = Permutation.unrank_nonlex(size, 0)
    seen = {tuple(cur.array_form)}
    ranks = [cur.rank_nonlex()]
    for i in range(1, total):
        cur = cur.next_nonlex()
        # ensure we get a permutation until the last one
        assert isinstance(cur, Permutation)
        # ranks should be strictly increasing by 1 each step
        ranks.append(cur.rank_nonlex())
        seen.add(tuple(cur.array_form))
    # After consuming total permutations, next_nonlex should return None
    assert cur.rank_nonlex() == total - 1
    assert cur.next_nonlex() is None
    # Ensure we saw exactly 'total' distinct permutations
    assert len(seen) == total
    # ranks collected should be 0..total-1
    assert ranks == list(range(total))

def test_next_nonlex_none_on_last_and_singleton():
    Permutation.print_cyclic = False
    # For size 1, only one permutation exists
    p1 = Permutation([0])
    assert p1.rank_nonlex() == 0
    assert p1.next_nonlex() is None

    # For size 2, there are 2 permutations; check last returns None
    p_first = Permutation.unrank_nonlex(2, 0)
    p_second = p_first.next_nonlex()
    assert isinstance(p_second, Permutation)
    assert p_second.rank_nonlex() == 1
    assert p_second.next_nonlex() is None

def test_next_nonlex_invalid_state_unchanged():
    Permutation.print_cyclic = False
    # Create permutation and copy its array_form to ensure next_nonlex doesn't mutate original
    original = Permutation([1, 2, 0, 3])
    arr_before = list(original.array_form)
    _ = original.next_nonlex()
    # original should remain unchanged
    assert original.array_form == arr_before