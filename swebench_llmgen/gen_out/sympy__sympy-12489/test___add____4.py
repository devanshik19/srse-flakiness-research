import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy import symbols

def test_add_basic_rank_and_unrank():
    # identity permutation plus any permutation's rank should give that permutation
    Permutation.print_cyclic = False
    I = Permutation([0, 1, 2, 3])
    a = Permutation([2, 1, 3, 0])
    # confirm rank + identity works
    assert I + a.rank() == a

def test_add_wraps_mod_cardinality():
    # ensure addition wraps modulo cardinality
    p = Permutation([1, 0, 2])  # size 3, cardinality = 6
    card = p.cardinality
    r = p.rank()
    # add card should wrap to same permutation
    res = p + card
    assert res == p
    # add card + 1 should be next lex after p
    nextp = p + (card + 1)
    expected = Perm.unrank_lex(p.size, (r + 1) % card)
    assert nextp == expected

def test_add_sets_rank_attribute():
    # verify that the returned permutation has _rank set to the wrapped rank
    q = Permutation([2, 0, 1, 3])
    initial_rank = q.rank()
    # add 2 (as int) and check _rank on returned object
    added = q + 2
    assert hasattr(added, "_rank")
    assert added._rank == (initial_rank + 2) % q.cardinality

def test_add_with_zero_and_large_values():
    # adding zero should return same permutation (via unrank_lex)
    r = Permutation([0,2,1])
    out = r + 0
    assert out == r
    # adding large number wraps properly
    big = r + (10 * r.cardinality + 3)
    assert big._rank == (r.rank() + 3) % r.cardinality
    assert big == Perm.unrank_lex(r.size, big._rank)

def test_add_rejects_non_integers():
    # __add__ expects an integer-like 'other' to be used modulo cardinality.
    # Passing an object that supports modulo via __int__ should work if convertible.
    class IntLike:
        def __init__(self, v): self.v = v
        def __mod__(self, other): return self.v % other
        def __int__(self): return int(self.v)
        def __rmod__(self, other): return self.v % other

    p = Permutation([1,2,0])
    # using IntLike that behaves like an integer (via mod) should work
    res = p + IntLike(2)
    assert res._rank == (p.rank() + 2) % p.cardinality
    # but passing a totally incompatible object should raise TypeError when used in arithmetic
    with pytest.raises(TypeError):
        _ = p + "not an int"