import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.combinatorics.permutations import Permutation

def test_add_basic_identity():
    # identity + a.rank() should give a (as in docstring)
    Permutation.print_cyclic = False
    I = Permutation([0, 1, 2, 3])
    a = Permutation([2, 1, 3, 0])
    result = I + a.rank()
    assert isinstance(result, Perm)
    # equality by array_form
    assert result.array_form == a.array_form

def test_add_with_integer_and_wraparound():
    # small size, check wraparound using cardinality
    p = Permutation([1, 0, 2])  # size 3, some permutation
    rank_p = p.rank()
    card = p.cardinality
    # add 0 should return same permutation
    r0 = p + 0
    assert r0.array_form == p.array_form
    # add card should be same as add 0 (wrap around)
    r_card = p + card
    assert r_card.array_form == p.array_form
    # add 1 should move to next lexicographic permutation
    r1 = p + 1
    expected = Perm.unrank_lex(p.size, (rank_p + 1) % card)
    assert r1.array_form == expected.array_form

def test_add_with_large_integer_and_rank_field_set():
    # verify that _rank is set on returned permutation and respects modulo
    q = Permutation([2, 0, 1, 3])
    base_rank = q.rank()
    card = q.cardinality
    add_val = card + 5  # effectively same as adding 5
    res = q + add_val
    assert hasattr(res, "_rank")
    assert res._rank == (base_rank + add_val) % card
    # returned permutation corresponds to unrank_lex of that _rank
    expected = Perm.unrank_lex(q.size, res._rank)
    assert res.array_form == expected.array_form

def test_add_type_errors_and_invalid():
    # ensure adding non-int-like raises TypeError (e.g., a permutation object)
    p = Permutation([0, 1, 2])
    with pytest.raises(TypeError):
        # Passing another permutation (object) should not be accepted by the arithmetic
        _ = p + Permutation([1, 0, 2])