import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_permutations():
    # simple example from docstring
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # rmul does a(b(i))
    res = list(Permutation.rmul(a, b))
    assert res == [1, 2, 0]
    # check that this equals applying a after b to each index
    assert [a(b(i)) for i in range(3)] == res

def test_rmul_with_tuple_and_permutation():
    # first arg must be a Permutation instance but later args may be sequences
    a = Permutation([2, 0, 1])
    t = [1, 2, 0]  # as a tuple/list representing a permutation
    res = list(Permutation.rmul(a, t))
    # interpreting t as permutation: t(i) = [1,2,0][i], then a(t(i))
    expected = [a(Permutation(t)(i)) for i in range(3)]
    assert res == expected

def test_rmul_multiple_operands_and_ordering():
    # verify order: rmul(a,b,c) = c*b*a when applied as function composition
    p = Permutation([1, 0, 2, 3])
    q = Permutation([0, 2, 1, 3])
    r = Permutation([0, 1, 3, 2])
    # compute rmul chain
    got = list(Permutation.rmul(p, q, r))
    # for each i, result should equal p(q(r(i)))
    expected = [p(q(r(i))) for i in range(4)]
    assert got == expected

def test_rmul_returns_first_when_single_argument():
    # If only one argument, rmul should return it unchanged (as Permutation)
    p = Permutation([1, 2, 0])
    out = Permutation.rmul(p)
    # rmul returns the permutation object itself; ensure its array form matches
    assert list(out) == list(p)

def test_rmul_raises_if_first_not_permutation():
    # According to docs, the first item must be a Permutation. If not, behavior
    # should be that subsequent items are multiplied onto the first; but if the
    # first isn't a Permutation, other parsing may fail. We assert TypeError
    # when first is a plain list and second is a Permutation (invalid use).
    p = Permutation([1, 0])
    with pytest.raises(TypeError):
        # first argument is not a Permutation instance here
        Permutation.rmul([0, 1], p)

def test_rmul_with_identity_and_size_mismatch():
    # Identity of size larger should still work when composed appropriately
    p = Permutation([1, 0, 2])
    # identity of size 4 as list
    id4 = [0, 1, 2, 3]
    # if first is Permutation and next is a larger identity, rmul will attempt
    # to multiply; ensure result is sensible (it should promote/interpret)
    res = Permutation.rmul(p, id4)
    # applying id4 then p: p(id4(i)) for i in range(4) -> for indices >=3 default behavior keeps them fixed
    # Represent result as list by iterating over its size
    out_list = list(res)
    # first three positions should match p applied to identity
    assert out_list[:3] == [p(i) for i in range(3)]
    # the extra position (index 3) should map to 3 (fixed)
    assert out_list[3] == 3