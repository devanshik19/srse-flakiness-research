import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_increment():
    # simple 3-element permutation tests
    p = Permutation([0, 1, 2])  # first lexicographic permutation
    # next should be [0,2,1]
    nxt = p.next_lex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [0, 2, 1]
    # next again -> [1,0,2]
    nxt2 = nxt.next_lex()
    assert nxt2.array_form == [1, 0, 2]
    # continue through remaining permutations to last
    seq = [p, nxt, nxt2, nxt2.next_lex(), nxt2.next_lex().next_lex(), nxt2.next_lex().next_lex().next_lex()]
    # collect their array forms
    forms = [q.array_form for q in seq if q is not None]
    # There are 6 permutations for 3 elements
    assert len(forms) == 6
    assert forms[0] == [0,1,2]
    assert forms[-1] == [2,1,0]  # last permutation

def test_next_lex_returns_none_at_end():
    # Last permutation in lex order should return None
    last = Permutation([3,2,1,0])
    assert last.array_form == [3,2,1,0]
    assert last.next_lex() is None

def test_next_lex_from_middle_complex():
    # Example from docstring: [2,3,1,0] -> next is with rank +1
    p = Permutation([2, 3, 1, 0])
    nxt = p.next_lex()
    assert nxt is not None
    # Check that nxt is lexicographically larger and is the immediate successor
    assert nxt.array_form > p.array_form
    # Manually compute expected successor:
    # For [2,3,1,0] the next lex permutation is [3,0,1,2]
    assert nxt.array_form == [3, 0, 1, 2]

def test_next_lex_singleton_and_two_elements():
    # singleton permutation: only one permutation, next_lex should return None
    s = Permutation([0])
    assert s.next_lex() is None

    # two elements: [1,0] is last, [0,1] -> next is [1,0]
    a = Permutation([0,1])
    b = a.next_lex()
    assert b.array_form == [1,0]
    assert b.next_lex() is None

def test_next_lex_does_not_mutate_original():
    original = [1, 0, 2, 3]
    p = Permutation(original)
    p_af_before = p.array_form[:]  # copy
    nxt = p.next_lex()
    # original permutation's array_form should remain unchanged
    assert p.array_form == p_af_before
    # returned permutation should be a different object (not the same reference)
    assert nxt is not p

def test_next_lex_full_cycle_through_all_permutations():
    # For n=4, iterate next_lex from first permutation until None,
    # ensure we see 24 unique permutations in lex order.
    start = Permutation([0,1,2,3])
    seen = []
    cur = start
    while cur is not None:
        seen.append(tuple(cur.array_form))
        cur = cur.next_lex()
    assert len(seen) == 24
    # ensure lex ordering
    assert seen == sorted(seen)
    # first and last checks
    assert seen[0] == (0,1,2,3)
    assert seen[-1] == (3,2,1,0)