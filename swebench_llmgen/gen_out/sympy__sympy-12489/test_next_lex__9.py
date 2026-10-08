import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_increment():
    # simple permutation: [0,1,2] -> next is [0,2,1]
    p = Permutation([0, 1, 2])
    nxt = p.next_lex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [0, 2, 1]

    # advance again: [0,2,1] -> [1,0,2]
    nxt2 = nxt.next_lex()
    assert nxt2.array_form == [1, 0, 2]

def test_next_lex_last_returns_none():
    # last lex permutation for 3 elements is [2,1,0]
    p = Permutation([2, 1, 0])
    assert p.next_lex() is None

def test_next_lex_middle_examples():
    # example from docstring: [2,3,1,0] should go to next rank
    p = Permutation([2, 3, 1, 0])
    nxt = p.next_lex()
    # check it's not None and is a permutation of same elements
    assert nxt is not None
    assert sorted(nxt.array_form) == sorted(p.array_form)
    # ensure lexicographic ordering: original < next
    assert p.array_form < nxt.array_form

def test_next_lex_full_cycle_through_all_permutations():
    # for n=4, iterate from first to last using next_lex and collect forms
    n = 4
    start = Permutation(list(range(n)))  # first lex permutation
    seen = []
    cur = start
    while cur is not None:
        seen.append(tuple(cur.array_form))
        cur = cur.next_lex()
    # total should be 4! = 24 permutations
    assert len(seen) == 24
    # they should be in lexicographic order
    assert seen[0] == tuple(range(n))
    assert seen[-1] == tuple(reversed(range(n)))
    # ensure uniqueness
    assert len(set(seen)) == 24

def test_next_lex_does_not_modify_original():
    p = Permutation([1, 0, 2, 3])
    original = p.array_form[:]  # copy
    nxt = p.next_lex()
    # original permutation array_form should be unchanged
    assert p.array_form == original
    # returned permutation should be different object if exists
    if nxt is not None:
        assert nxt is not p
        assert nxt.array_form != original

def test_next_lex_edge_two_elements():
    # n=2 permutations: [0,1] -> [1,0] -> None
    p = Permutation([0, 1])
    nxt = p.next_lex()
    assert nxt.array_form == [1, 0]
    assert nxt.next_lex() is None

def test_next_lex_invalid_internal_behavior_guard():
    # construct a permutation that has a decreasing tail to force i decrement to -1
    p = Permutation([3,2,1,0])
    assert p.next_lex() is None

    # and one that requires swapping elements near end
    p2 = Permutation([0,3,2,1])
    nxt2 = p2.next_lex()
    assert nxt2 is not None
    # confirm lexicographic increment property
    assert p2.array_form < nxt2.array_form