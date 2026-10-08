import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_increment():
    # simple permutation: [0,1,2] -> next is [0,2,1]
    p = Permutation([0, 1, 2])
    nxt = p.next_lex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [0, 2, 1]

    # from [0,2,1] next is [1,0,2]
    nxt2 = nxt.next_lex()
    assert nxt2.array_form == [1, 0, 2]

    # ensure original not mutated
    assert p.array_form == [0, 1, 2]

def test_next_lex_middle_swap_and_reverse():
    # example from docstring-like: [2,3,1,0] -> next should be computed correctly
    p = Permutation([2, 3, 1, 0])
    # Manually compute expected next lexicographical permutation for [2,3,1,0]:
    # permutations of 0..3 in lex order: ... [2,3,0,1], [2,3,1,0], [3,0,1,2] ...
    # So next after [2,3,1,0] is [3,0,1,2]
    nxt = p.next_lex()
    assert nxt.array_form == [3, 0, 1, 2]

def test_next_lex_last_returns_none():
    # highest lex permutation for size 4 is [3,2,1,0]
    p = Permutation([3, 2, 1, 0])
    assert p.next_lex() is None

def test_next_lex_all_perms_walkthrough():
    # Walk through all lex permutations of size 3 using next_lex starting from first
    start = Permutation([0, 1, 2])
    seen = [start.array_form[:]]
    cur = start
    while True:
        cur = cur.next_lex()
        if cur is None:
            break
        seen.append(cur.array_form[:])

    # There should be 3! = 6 permutations in lex order
    assert len(seen) == 6
    # Check lexicographic ordering property
    assert seen == sorted(seen)

def test_next_lex_singleton_and_two_elements():
    # size 1: only permutation, next should be None
    p1 = Permutation([0])
    assert p1.next_lex() is None

    # size 2: [0,1] -> [1,0] -> None
    p2 = Permutation([0, 1])
    nxt = p2.next_lex()
    assert nxt.array_form == [1, 0]
    assert nxt.next_lex() is None

def test_next_lex_multiple_calls_idempotence_on_none():
    p = Permutation([1, 0])  # last for size 2
    assert p.next_lex() is None
    # calling again still returns None
    assert p.next_lex() is None

def test_next_lex_does_not_share_list_reference():
    p = Permutation([0, 2, 1])
    nxt = p.next_lex()
    # mutate returned array (via its attribute) and ensure original is unchanged
    nxt_af = nxt.array_form
    nxt_af[0] = 9
    assert p.array_form == [0, 2, 1]
    # also ensure nxt's internal array reflects mutation (sanity of reference separation)
    assert nxt.array_form[0] == 9