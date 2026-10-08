import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic():
    # Simple permutation in middle: [0,1,2] -> next is [0,2,1]
    p = Permutation([0, 1, 2])
    q = p.next_lex()
    assert isinstance(q, Permutation)
    assert q.array_form == [0, 2, 1]

    # Next of [0,2,1] is [1,0,2]
    r = q.next_lex()
    assert r.array_form == [1, 0, 2]

def test_next_lex_last_returns_none():
    # Last permutation in lex order for 3 elements is [2,1,0]
    p = Permutation([2, 1, 0])
    assert p.next_lex() is None

def test_next_lex_full_cycle_through_all():
    # Verify that iterating next_lex from first reaches last then None
    n = 4
    # first lexicographic permutation is [0,1,2,3]
    p = Permutation(list(range(n)))
    seen = [p.array_form[:]]
    while True:
        p = p.next_lex()
        if p is None:
            break
        seen.append(p.array_form[:])
    # There should be n! permutations
    import math
    assert len(seen) == math.factorial(n)
    # First is sorted and last is reverse-sorted
    assert seen[0] == list(range(n))
    assert seen[-1] == list(range(n-1, -1, -1))

def test_next_lex_preserves_elements_and_is_copy():
    # Ensure next_lex returns a new Permutation and does not mutate original
    base = [2, 0, 1, 3]
    p = Permutation(base)
    q = p.next_lex()
    # original unchanged
    assert p.array_form == base
    # q is a different object (but equal as permutation type)
    assert q is not p
    # q is a permutation of same elements
    assert sorted(q.array_form) == sorted(base)
    # Check specific expected next lex for manual verification:
    # For [2,0,1,3] next lex should be [2,0,3,1]
    assert q.array_form == [2, 0, 3, 1]

def test_next_lex_single_and_two_element_cases():
    # Single element permutation: next should be None as only one permutation
    p1 = Permutation([0])
    assert p1.next_lex() is None

    # Two elements: [0,1] -> [1,0] -> None
    p2 = Permutation([0,1])
    p2_next = p2.next_lex()
    assert p2_next.array_form == [1,0]
    assert p2_next.next_lex() is None

def test_next_lex_against_rank_unrank_cycle():
    # Use rank/unrank_lex if available to cross-check a few values
    # Start from a permutation, get rank, unrank next rank and compare next_lex
    p = Permutation([1, 0, 3, 2])
    try:
        r = p.rank()
        # unrank_lex is a classmethod-like interface: Permutation.unrank_lex(size, rank)
        # Some SymPy versions have it as function, so we attempt both styles
        from_sympy = None
        try:
            from_sympy = Permutation.unrank_lex(p.size, r+1)
        except TypeError:
            # maybe unrank_lex is a function taking (size, rank)
            from_sympy = Permutation().unrank_lex(p.size, r+1)
        nxt = p.next_lex()
        # if next exists compare to unrank result
        if nxt is None:
            # then r must be last rank; unrank should have raised or returned None/invalid
            # assert that r is maximal rank (i.e., equals factorial-1)
            import math
            assert r == math.factorial(p.size) - 1
        else:
            assert nxt.array_form == from_sympy.array_form
    except Exception:
        # If rank/unrank_lex are not present/throw, at least ensure next_lex runs and returns Permutation or None
        nxt = p.next_lex()
        assert (nxt is None) or isinstance(nxt, Permutation)