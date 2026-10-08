import pytest
from sympy.combinatorics.permutations import Permutation as Perm
from sympy.combinatorics.permutations import Permutation
from sympy.core.compatibility import as_int

def test_add_basic_identity():
    # identity + a.rank() should give a (as in docstring)
    Permutation.print_cyclic = False
    I = Perm([0,1,2,3])
    a = Perm([2,1,3,0])
    # ensure rank and cardinality behave
    assert isinstance(a.rank(), int)
    assert I + a.rank() == a

def test_add_wraparound_rank():
    # rank addition wraps around modulo cardinality
    p = Perm([1,0,2])  # size 3 permutation
    c = p.cardinality
    r = p.rank()
    # adding c should return same permutation
    res = p + c
    assert res == p
    # adding c+1 should be same as adding 1
    assert p + (c + 1) == p + 1

def test_add_with_permutation_like_other_int():
    # other can be an integer (the code uses other modulo cardinality)
    q = Perm([2,0,1,3])  # size 4
    r = q.rank()
    # add a small integer
    plus_two = q + 2
    # compute expected by unranking manually via Perm.unrank_lex
    expected = Perm.unrank_lex(q.size, (r + 2) % q.cardinality)
    expected._rank = (r + 2) % q.cardinality
    assert plus_two == expected

def test_add_returns_new_object_and_sets_rank():
    # ensure returned object is fresh and has _rank set
    s = Perm([0,2,1])
    original_rank = s.rank()
    out = s + 1
    assert out is not s
    assert hasattr(out, '_rank')
    assert out._rank == (original_rank + 1) % s.cardinality

def test_add_various_branches_and_errors():
    # test with zero and large integers
    p = Perm([1,2,0,3,4])
    r = p.rank()
    out0 = p + 0
    assert out0 == p
    out_large = p + (10**6)
    assert out_large == Perm.unrank_lex(p.size, (r + (10**6 % p.cardinality)) % p.cardinality)

    # Also test that adding a negative integer works via Python modulo semantics
    neg = p + (-1)
    expected_rank = (r + (-1)) % p.cardinality
    assert neg == Perm.unrank_lex(p.size, expected_rank)

def test_add_with_non_int_like_raises_typeerror():
    p = Perm([0,1,2])
    # Passing something that cannot be used with % should raise TypeError
    class Bad:
        def __rmod__(self, other):
            raise TypeError("bad")
    with pytest.raises(TypeError):
        # the implementation does (self.rank() + other) % self.cardinality
        # So if other doesn't support addition, Python will try __radd__ of Bad or fail.
        p + Bad()