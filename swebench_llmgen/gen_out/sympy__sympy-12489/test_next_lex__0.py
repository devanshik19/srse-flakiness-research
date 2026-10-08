import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_sequence():
    # simple increasing permutation -> next is swapping last two
    p = Permutation([0,1,2])
    nxt = p.next_lex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [0,2,1]
    # successive calls produce lexicographic sequence
    seq = [p]
    while seq[-1] is not None:
        seq.append(seq[-1].next_lex())
    # last element should be None (after the final permutation)
    assert seq[-1] is None
    # collect actual array_forms (excluding trailing None)
    arrays = [perm.array_form for perm in seq[:-1]]
    # should start at [0,1,2] and end at [2,1,0] and length = 6 for 3!
    assert arrays[0] == [0,1,2]
    assert arrays[-1] == [2,1,0]
    assert len(arrays) == 6
    # check ordering is lexicographic
    assert arrays == sorted(arrays)

def test_next_lex_middle_case():
    # test known example from docstring: rank 17 -> next rank 18 for [2,3,1,0]
    p = Permutation([2,3,1,0])
    # ensure starting array_form is as expected
    assert p.array_form == [2,3,1,0]
    nxt = p.next_lex()
    assert nxt is not None
    # verify that nxt is lexicographically next: compare to sorted list of perms
    perms = sorted([list(t) for t in __import__('itertools').permutations(p.array_form)])
    idx = perms.index(p.array_form)
    assert perms[idx+1] == nxt.array_form

def test_next_lex_last_returns_none():
    # the last permutation in lexicographic order should return None
    p = Permutation([3,2,1,0])
    assert p.array_form == [3,2,1,0]
    assert p.next_lex() is None

def test_next_lex_singleton_and_two_elements():
    # singleton permutation has only one ordering -> next is None
    p1 = Permutation([0])
    assert p1.next_lex() is None

    # two element permutations: [0,1] -> [1,0] -> None
    p2 = Permutation([0,1])
    p2n = p2.next_lex()
    assert p2n.array_form == [1,0]
    assert p2n.next_lex() is None

def test_next_lex_does_not_mutate_original():
    p = Permutation([1,0,2])
    original = p.array_form[:]  # copy
    nxt = p.next_lex()
    # original permutation should remain unchanged
    assert p.array_form == original
    # next should be a distinct object (but still a Permutation)
    assert isinstance(nxt, Permutation)
    assert nxt.array_form != p.array_form

def test_next_lex_multiple_steps_full_enumeration():
    # enumerate via repeated next_lex and compare to unrank_lex enumeration
    base = [0,1,2,3]
    start = Permutation(base)
    seen = []
    cur = start
    while cur is not None:
        seen.append(cur.array_form)
        cur = cur.next_lex()
    # There should be 4! permutations
    assert len(seen) == 24
    # first and last elements check
    assert seen[0] == base
    assert seen[-1] == sorted(base, reverse=True)