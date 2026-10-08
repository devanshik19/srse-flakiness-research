import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy import S

def test_add_basic_identity():
    # identity + a.rank() should return a (as in docstring)
    Permutation.print_cyclic = False
    I = Permutation([0, 1, 2, 3])
    a = Permutation([2, 1, 3, 0])
    # ensure rank and cardinality behave as expected
    r = a.rank()
    assert isinstance(r, int)
    res = I + r
    assert res == a
    # rank attribute of returned permutation should equal (I.rank()+r) % cardinality
    assert res._rank == (I.rank() + r) % res.cardinality

def test_add_wraparound_and_type_int():
    # create a permutation and add an integer larger than cardinality to force wraparound
    p = Permutation([1, 2, 0])  # size 3
    card = p.cardinality
    # choose other such that rank wraps around
    other = p.rank() + card * 2 + 1
    res = p + other
    # result should be same as unrank_lex(size, (p.rank()+other)%card)
    expected_rank = (p.rank() + other) % card
    expected = Perm.unrank_lex(p.size, expected_rank)
    assert res == expected
    assert res._rank == expected_rank

def test_add_with_zero_other_returns_self_shifted():
    p = Permutation([2, 0, 1, 3])
    res = p + 0
    # should be permutation with rank increased by p.rank()
    expected = Perm.unrank_lex(p.size, (p.rank() + 0) % p.cardinality)
    assert res == expected
    assert res._rank == expected.rank()

def test_add_invalid_type_raises():
    p = Permutation([0,1])
    # other must be an integer-like; passing a non-int should raise TypeError when used in modulo
    with pytest.raises(TypeError):
        _ = p + "not an int"

def test_add_uses_unrank_lex_called_correctly(monkeypatch):
    p = Permutation([0,1,2])
    called = {}
    def fake_unrank_lex(size, rank):
        called['args'] = (size, rank)
        # return a genuine Permutation so attribute checks work
        return Perm.unrank_lex(size, rank)
    monkeypatch.setattr(Perm, 'unrank_lex', staticmethod(fake_unrank_lex))
    other = 2
    res = p + other
    assert called['args'] == (p.size, (p.rank() + other) % p.cardinality)
    assert isinstance(res, Permutation)