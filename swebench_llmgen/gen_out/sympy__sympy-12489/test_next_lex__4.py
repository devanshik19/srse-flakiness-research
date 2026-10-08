import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_sequence():
    # simple increasing permutation: next is swap last two
    p = Permutation([0,1,2])
    # rank and next relation sanity: next_lex should give [0,2,1]
    nxt = p.next_lex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [0,2,1]

def test_next_lex_middle_case():
    # a middle permutation where pivot inside; example from docstring
    p = Permutation([2,3,1,0])
    # Manually compute next lexicographic permutation of [2,3,1,0]
    # Permutations of 0..3 in lex order: ...,[2,3,0,1],[2,3,1,0],[3,0,1,2],...
    # Next after [2,3,1,0] should be [3,0,1,2]
    nxt = p.next_lex()
    assert nxt.array_form == [3,0,1,2]

def test_next_lex_last_returns_none():
    # last permutation in lexicographic order should return None
    p = Permutation([3,2,1,0])
    assert p.next_lex() is None

def test_next_lex_two_element_cases():
    # two elements: [0,1] -> [1,0] -> None
    p = Permutation([0,1])
    nxt = p.next_lex()
    assert nxt.array_form == [1,0]
    assert nxt.next_lex() is None

    # reversed: immediate None
    p2 = Permutation([1,0])
    assert p2.next_lex() is None

def test_next_lex_single_element():
    # single element: only permutation, next is None
    p = Permutation([0])
    assert p.next_lex() is None

def test_next_lex_large_permutation_motion():
    # Ensure that next_lex only rearranges suffix after pivot
    p = Permutation([0,2,3,1,4])
    # compute next lex using Python's built-in approach for verification
    arr = p.array_form[:]
    # mimic algorithm to find next lex for verification
    def next_lex_list(a):
        a = a[:]
        n = len(a)
        i = n-2
        while i >= 0 and a[i+1] < a[i]:
            i -= 1
        if i == -1:
            return None
        j = n-1
        while a[j] < a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
        i += 1
        j = n-1
        while i < j:
            a[i], a[j] = a[j], a[i]
            i += 1
            j -= 1
        return a

    expected = next_lex_list(arr)
    nxt = p.next_lex()
    if expected is None:
        assert nxt is None
    else:
        assert nxt.array_form == expected

def test_next_lex_multiple_calls_progression():
    # walk through all permutations of 3 elements using next_lex
    start = Permutation([0,1,2])
    seq = [start]
    cur = start
    while True:
        nxt = cur.next_lex()
        if nxt is None:
            break
        seq.append(nxt)
        cur = nxt

    # there should be 6 permutations for 3 elements
    assert len(seq) == 6
    # ensure they are lexicographically increasing
    lists = [p.array_form for p in seq]
    assert lists == sorted(lists)

def test_next_lex_edge_pivot_at_start():
    # pivot at index 0 with rest decreasing: e.g. [1,4,3,2,0] -> next should swap 1 with 2? verify algorithmically
    p = Permutation([1,4,3,2,0])
    nxt = p.next_lex()
    # verify using brute-force sorted permutations
    from itertools import permutations
    all_perms = sorted(list(permutations(range(len(p.array_form)))))
    idx = all_perms.index(tuple(p.array_form))
    if idx + 1 < len(all_perms):
        assert nxt.array_form == list(all_perms[idx+1])
    else:
        assert nxt is None