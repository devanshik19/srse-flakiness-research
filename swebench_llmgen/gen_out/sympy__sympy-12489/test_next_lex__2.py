import pytest
from sympy.combinatorics.permutations import Permutation

def test_next_lex_basic_increment():
    # simple permutation: [0,1,2] -> next is [0,2,1]
    p = Permutation([0,1,2])
    nxt = p.next_lex()
    assert isinstance(nxt, Permutation)
    assert nxt.array_form == [0,2,1]

def test_next_lex_middle():
    # from example in docstring: [2,3,1,0] rank 17 -> next rank 18
    p = Permutation([2,3,1,0])
    nxt = p.next_lex()
    assert nxt.array_form == [3,0,1,2]  # verified next lexicographic permutation
    # ensure original not mutated
    assert p.array_form == [2,3,1,0]

def test_next_lex_full_cycle_through():
    # iterate through all permutations of size 3 in lex order and ensure last returns None
    start = Permutation([0,1,2])
    perms = [start]
    cur = start
    while True:
        cur = cur.next_lex()
        if cur is None:
            break
        perms.append(cur)
    # There are 3! = 6 permutations
    assert len(perms) == 6
    # Check lex order by comparing array_forms
    array_forms = [p.array_form for p in perms]
    assert array_forms == sorted(array_forms)

def test_next_lex_last_returns_none():
    # last lexicographic permutation for size 4 is descending
    last = Permutation([3,2,1,0])
    assert last.next_lex() is None

def test_next_lex_singleton_and_two_elements():
    # size 1: only one permutation, next should be None
    p1 = Permutation([0])
    assert p1.next_lex() is None

    # size 2: [0,1] -> [1,0] -> None
    p2 = Permutation([0,1])
    p2n = p2.next_lex()
    assert p2n.array_form == [1,0]
    assert p2n.next_lex() is None

def test_next_lex_with_duplicates_not_permutation_raises():
    # The Permutation class expects a permutation; constructing with duplicates should
    # either normalize or raise. We check that next_lex doesn't silently produce a wrong result.
    # Create a malformed "permutation" via the constructor if allowed.
    with pytest.raises(Exception):
        # attempt to create an invalid permutation - SymPy should raise
        Permutation([1,1,0]).next_lex()

def test_next_lex_does_not_modify_internal_state():
    p = Permutation([1,0,2,3])
    af_before = list(p.array_form)
    nxt = p.next_lex()
    # original permutation should be unchanged
    assert p.array_form == af_before
    # next is a different object if not None
    if nxt is not None:
        assert nxt is not p
        assert isinstance(nxt, Permutation)

def test_next_lex_multiple_steps_consistency():
    p = Permutation([0,1,2,3])
    # collect via next_lex
    seq1 = []
    cur = p
    while cur is not None:
        seq1.append(cur.array_form)
        cur = cur.next_lex()
    # collect via unrank_lex if available: compare counts and distinctness
    # ensure all are unique and in lexicographic order
    assert len(seq1) == 24
    assert len({tuple(x) for x in seq1}) == 24
    assert seq1 == sorted(seq1)