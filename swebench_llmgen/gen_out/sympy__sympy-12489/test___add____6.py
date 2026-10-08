import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.core.compatibility import as_int

def test_add_basic_and_identity():
    # identity permutation
    I = Permutation([0, 1, 2, 3])
    a = Permutation([2, 1, 3, 0])
    # Ensure rank and cardinality behave as expected
    r = a.rank()
    assert isinstance(r, int)
    assert I.cardinality == a.cardinality
    # I + a.rank() should give a (as in docstring example)
    res = I + r
    # result should be equal to a (array form)
    assert res.array_form == a.array_form
    # And the stored _rank should match (I.rank() is 0)
    assert res._rank == (I.rank() + r) % I.cardinality

def test_add_wraps_around_cardinality(monkeypatch):
    # create a small permutation and force a large other so wrapping occurs
    p = Permutation([1, 0, 2])  # size 3
    # check cardinality for size 3 is 6
    card = p.cardinality
    assert card == 6
    # choose other so sum exceeds cardinality
    other = card + 2  # rank offset
    res = p + other
    # expected rank is (p.rank() + other) % card
    expected_rank = (p.rank() + other) % card
    assert res._rank == expected_rank
    # verify that unranking gives the same permutation
    unranked = Perm.unrank_lex(p.size, expected_rank)
    assert res.array_form == unranked.array_form

def test_add_with_zero_and_full_cycle():
    # zero should behave like identity addition
    perm = Permutation([2, 0, 1, 3])
    zero = 0
    res = perm + zero
    assert res.array_form == Perm.unrank_lex(perm.size, perm.rank()).array_form
    # adding exactly cardinality should be same as adding 0
    res2 = perm + perm.cardinality
    assert res2.array_form == res.array_form

def test_add_uses_unrank_lex_internal(monkeypatch):
    # Ensure __add__ calls Perm.unrank_lex with correct parameters
    p = Permutation([0, 2, 1])
    called = {}
    def fake_unrank_lex(size, rank):
        # record and return a real permutation to keep behavior valid
        called['size'] = size
        called['rank'] = rank
        return Perm.unrank_lex.__wrapped__(Perm, size, rank) if hasattr(Perm.unrank_lex, "__wrapped__") else Perm.unrank_lex(size, rank)
    # monkeypatch the class method
    monkeypatch.setattr(Perm, "unrank_lex", fake_unrank_lex, raising=True)
    other = 2
    res = p + other
    assert called['size'] == p.size
    assert called['rank'] == (p.rank() + other) % p.cardinality
    # result should still be a Permutation (array_form present)
    assert hasattr(res, "array_form")

def test_add_invalid_other_types():
    # other should be interpreted as integer via modulo; non-int that cannot be used should raise
    p = Permutation([0,1,2])
    class Bad:
        def __rmod__(self, other):
            raise TypeError("bad mod")
    bad = Bad()
    with pytest.raises(TypeError):
        # (p.rank() + bad) % p.cardinality will attempt to add int and Bad -> TypeError
        _ = p + bad