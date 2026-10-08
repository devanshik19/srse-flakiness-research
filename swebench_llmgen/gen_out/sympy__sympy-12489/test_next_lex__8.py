import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_increment():
    # simple permutation in the middle: [0,1,2] -> next is [0,2,1]
    p = Permutation([0,1,2])
    nxt = p.next_lex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [0,2,1]

    # check successive calls iterate lexicographically
    p0 = Permutation([0,1,2,3])
    seq = []
    cur = p0
    while cur is not None:
        seq.append(cur.array_form)
        cur = cur.next_lex()
    # There are 4! = 24 permutations; first should be [0,1,2,3], last [3,2,1,0]
    assert seq[0] == [0,1,2,3]
    assert seq[-1] == [3,2,1,0]
    assert len(seq) == 24

def test_next_lex_last_returns_none():
    # last lex permutation should return None
    p = Permutation([3,2,1,0])
    assert p.next_lex() is None

def test_next_lex_single_and_two_element():
    # single element: it's both first and last
    p1 = Permutation([0])
    assert p1.next_lex() is None

    # two elements: [0,1] -> [1,0] -> None
    p2 = Permutation([0,1])
    p2n = p2.next_lex()
    assert p2n.array_form == [1,0]
    assert p2n.next_lex() is None

def test_next_lex_middle_swap_and_reverse_case():
    # This checks the algorithm's swap and tail reversal behavior.
    # Example from docstring: rank 17 -> next rank 18 for [2,3,1,0]
    p = Permutation([2,3,1,0])
    nxt = p.next_lex()
    # Manually compute expected next lex for [2,3,1,0]:
    # The pivot is at index 1 (value 3) since 1<3 and 0<1; swap with the next larger (none to right),
    # Actually algorithm finds i where perm[i] < perm[i+1]; for [2,3,1,0], pivot is 0-indexed i=0 (2<3)
    # It should swap 2 with the smallest element >2 to its right which is 3, then reverse tail -> [3,0,1,2]
    assert nxt.array_form == [3,0,1,2]

def test_next_lex_exhaustive_small_n():
    # For n=3 verify that next_lex produces the lexicographic successor equal to
    # comparing to python's sorted permutations
    from itertools import permutations
    all_perms = sorted(permutations(range(3)))
    # convert to list of Permutation objects in same lex order
    perm_objs = [Permutation(list(p)) for p in all_perms]
    for i, p in enumerate(perm_objs):
        nxt = p.next_lex()
        if i == len(perm_objs) - 1:
            assert nxt is None
        else:
            assert nxt.array_form == list(all_perms[i+1])

def test_next_lex_does_not_mutate_original():
    base = [0,2,1,3]
    p = Permutation(list(base))
    _ = p.next_lex()
    # original object's array_form should remain unchanged
    assert p.array_form == base