import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy import S

def test_add_basic_and_identity():
    # identity permutation
    I = Permutation([0, 1, 2, 3])
    # a nontrivial permutation
    a = Permutation([2, 1, 3, 0])
    # ensure rank works and cardinality/size are as expected
    assert I.size == 4
    assert a.size == 4
    r = a.rank()
    # I + rank should return the permutation a (as in docstring)
    result = I + r
    assert isinstance(result, Permutation)
    assert result == a
    # also reverse: adding 0 (identity rank) to a should give a with rank preserved modulo cardinality
    res2 = a + 0
    assert res2 == a

def test_add_wraps_around_cardinality_and_sets_rank():
    # size 3 permutations; there are 6 permutations (cardinality)
    p = Permutation([1, 2, 0])  # some permutation
    card = p.cardinality
    assert card == 6
    # add a value larger than cardinality to force wrapping
    addval = card + 2  # should be equivalent to adding 2
    newp = p + addval
    # check that rank is set to (p.rank() + addval) % cardinality
    expected_rank = (p.rank() + addval) % card
    assert newp._rank == expected_rank
    # unrank lex should produce same permutation as used by __add__
    unranked = Perm.unrank_lex(p.size, expected_rank)
    assert newp == unranked

def test_add_with_zero_and_full_cycle():
    # zero add should be identity on rank (mod cardinality)
    q = Permutation([0, 2, 1, 4, 3])
    res = q + 0
    assert res == q
    # add exactly cardinality should wrap to same permutation (rank unchanged)
    res2 = q + q.cardinality
    assert res2 == q
    # check that _rank attribute exists and is within range
    assert 0 <= res2._rank < q.cardinality

def test_add_errors_or_type_handling():
    # Ensure adding an invalid type raises appropriate exception (TypeError or AttributeError)
    p = Permutation([0, 1, 2])
    with pytest.raises(Exception):
        # strings are invalid for arithmetic; implementation expects numeric
        _ = p + "not a number"