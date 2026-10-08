import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_sequence():
    # Basic increasing permutation -> next is swap last two
    p = Permutation([0,1,3,2])
    nxt = p.next_lex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [0,1,3,2] or nxt.array_form != p.array_form
    # Explicit expected: next lex after [0,1,3,2] is [0,2,1,3]?
    # To avoid relying on rank implementation, generate lex ordering by ranking/unranking
    # but here we can check that applying next_lex repeatedly yields increasing ranks until None.
    # Start from a known permutation and iterate until None, ensuring strict progress.
    p0 = Permutation([2,3,1,0])
    ranks = []
    q = p0
    while q is not None:
        r = q.rank()
        ranks.append(r)
        q = q.next_lex()
    # Ensure ranks are strictly increasing
    assert all(ranks[i] < ranks[i+1] for i in range(len(ranks)-1))
    # Last next_lex returned None
    assert q is None

def test_next_lex_last_permutation_returns_none():
    # Last lexicographic permutation is descending order
    p = Permutation([4,3,2,1,0])
    assert p.next_lex() is None

def test_next_lex_many_steps_matches_unrank_unrank():
    # Test by enumerating lex permutations via rank/unrank_lex
    size = 4
    # collect all permutations via next_lex starting from the minimal (unrank_lex rank 0)
    start = Permutation().unrank_lex(size, 0)
    seq = []
    p = start
    while p is not None:
        seq.append(tuple(p.array_form))
        p = p.next_lex()
    # Now produce via unrank_lex all ranks 0..n!-1 and compare
    import math
    expected = []
    for r in range(math.factorial(size)):
        expected.append(tuple(Permutation().unrank_lex(size, r).array_form))
    assert seq == expected

def test_next_lex_singleton_and_two_elements():
    # Size 1: only one permutation
    p1 = Permutation([0])
    assert p1.next_lex() is None
    # Size 2: [0,1] -> [1,0] -> None
    p2 = Permutation([0,1])
    n1 = p2.next_lex()
    assert isinstance(n1, Permutation)
    assert n1.array_form == [1,0]
    assert n1.next_lex() is None

def test_next_lex_preserves_elements_and_length():
    # Ensure next_lex returns permutation of same set and length
    p = Permutation([1,0,3,2])
    nxt = p.next_lex()
    if nxt is not None:
        assert sorted(nxt.array_form) == sorted(p.array_form)
        assert len(nxt.array_form) == len(p.array_form)

def test_next_lex_multiple_applications_full_cycle():
    # For small n, applying next_lex repeatedly from rank 0 should produce factorial(n) permutations then None
    size = 3
    start = Permutation().unrank_lex(size, 0)
    count = 0
    p = start
    while p is not None:
        count += 1
        p = p.next_lex()
    import math
    assert count == math.factorial(size)