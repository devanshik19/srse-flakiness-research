import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_increment():
    # simple 3-element permutation
    p = Permutation([0, 1, 2])
    # next lex of the first permutation should be [0,2,1]
    p2 = p.next_lex()
    assert isinstance(p2, Permutation)
    assert p2.array_form == [0, 2, 1]
    # next lex again -> [1,0,2]
    p3 = p2.next_lex()
    assert p3.array_form == [1, 0, 2]
    # continue through all to the last
    seen = [p, p2, p3]
    cur = p3
    while cur is not None:
        cur = cur.next_lex()
        if cur is not None:
            seen.append(cur)
    # there should be 6 permutations for 3 elements
    assert len(seen) == 6
    # last permutation in lex order for 3 elements is [2,1,0]
    assert seen[-1].array_form == [2, 1, 0]

def test_next_lex_from_middle_and_to_end():
    # start from a middle permutation for 4 elements
    p = Permutation([1, 3, 0, 2])
    # compute next lex manually by using rank/unrank equivalence:
    # but ensure next_lex returns a valid permutation and is lex-greater
    nxt = p.next_lex()
    assert nxt is not None
    assert isinstance(nxt, Permutation)
    assert nxt.array_form != p.array_form
    # verify lex ordering: nxt should be greater in lexicographic comparison
    assert tuple(nxt.array_form) > tuple(p.array_form)
    # advance until None is returned (past last permutation)
    last = nxt
    while True:
        candidate = last.next_lex()
        if candidate is None:
            break
        last = candidate
    assert last.array_form == [3, 2, 1, 0]

def test_next_lex_on_last_returns_none():
    # last permutation should return None
    last = Permutation([3, 2, 1, 0])
    assert last.next_lex() is None

def test_next_lex_singleton_and_two_elements():
    # singleton: only one permutation, next_lex should return None
    p1 = Permutation([0])
    assert p1.next_lex() is None
    # two elements: check sequence [0,1] -> [1,0] -> None
    p2 = Permutation([0,1])
    p2n = p2.next_lex()
    assert p2n.array_form == [1,0]
    assert p2n.next_lex() is None

def test_next_lex_complex_case_preserves_elements():
    # ensure next_lex preserves the set of elements and only reorders
    p = Permutation([2, 0, 4, 1, 3])
    nxt = p.next_lex()
    # elements should be a permutation of the original
    assert sorted(nxt.array_form) == sorted(p.array_form) == [0,1,2,3,4]
    # repeated application until end should not produce duplicates
    seen = set()
    cur = p
    while cur is not None:
        tup = tuple(cur.array_form)
        assert tup not in seen
        seen.add(tup)
        cur = cur.next_lex()
    # count should equal factorial(5) = 120 when starting from the first permutation;
    # since we started from a mid permutation, ensure at least more than 1 result collected
    assert len(seen) > 1