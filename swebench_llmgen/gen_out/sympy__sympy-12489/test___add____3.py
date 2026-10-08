import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.combinatorics.permutations import Permutation
from sympy.core.compatibility import as_int

def test_add_basic_identity():
    # identity + a.rank() == a (as in docstring example)
    Permutation.print_cyclic = False
    I = Perm([0, 1, 2, 3])
    a = Perm([2, 1, 3, 0])
    # Ensure rank works and addition returns expected permutation
    result = I + a.rank()
    assert isinstance(result, Perm)
    assert result == a

def test_add_wraparound_rank():
    # Test wraparound when rank exceeds cardinality
    p = Perm([1, 0, 2])  # a simple transposition on 3 points
    card = p.cardinality
    r = p.rank()
    # add a value that causes wraparound: card + r should reduce modulo card to r
    res = p + (card + r)
    assert isinstance(res, Perm)
    assert res == p

def test_add_with_zero_and_max_rank():
    # Adding zero should return the same permutation (since other=0 means identity rank shift)
    p = Perm([2, 0, 1, 3])
    res_zero = p + 0
    assert res_zero == p
    # Adding cardinality-1 should move to the previous lex permutation
    # Compute expected via unrank_lex: rank + (card-1) modulo card == rank-1 modulo card
    card = p.cardinality
    new = p + (card - 1)
    expected_rank = (p.rank() + (card - 1)) % card
    expected = Perm.unrank_lex(p.size, expected_rank)
    # Ensure returned permutation has its _rank set properly and equals expected
    assert new == expected
    assert getattr(new, "_rank", None) == expected_rank

def test_add_with_nonint_other_raises_or_coerces():
    # The implementation uses modulo with self.cardinality; test behavior when other is not int
    p = Perm([0,1,2])
    # If other provides __int__ or is int-like, it should work; as_int coerces in many sympy places
    class IntLike:
        def __int__(self):
            return 1
        def __index__(self):
            return 1
    res = p + IntLike()
    # Expect same as adding 1
    expected = Perm.unrank_lex(p.size, (p.rank() + 1) % p.cardinality)
    assert res == expected

def test_add_commutes_not_required():
    # __add__ is not symmetric; ensure adding permutations vs adding ints behaves as documented:
    a = Perm([1,2,0])
    b = Perm([2,0,1])
    # a + b.rank() should equal b shifted by a.rank() if done in correct order
    res1 = a + b.rank()
    res2 = Perm.unrank_lex(a.size, (a.rank() + b.rank()) % a.cardinality)
    assert res1 == res2

def test_add_preserves_size_and_cardinality():
    p = Perm([3,2,1,0])
    other = 2
    r = p + other
    assert r.size == p.size
    assert r.cardinality == p.cardinality

def test_add_invalid_other_type_raises_typeerror():
    # If other cannot be used with modulo, it should raise a TypeError
    p = Perm([0,1,2])
    class Bad:
        pass
    with pytest.raises(TypeError):
        _ = p + Bad()