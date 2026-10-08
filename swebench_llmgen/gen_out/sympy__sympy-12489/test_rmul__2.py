import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_permutations():
    # simple tuple inputs parsed as Permutation when first arg is Permutation
    a = Permutation([1, 0, 2])  # mapping: 0->1,1->0,2->2
    b = Permutation([0, 2, 1])  # mapping: 0->0,1->2,2->1
    # rmul does a(b(i)) for each i (reverse order compared to * operator)
    result = Permutation.rmul(a, b)
    # result should be a after applying b then a: a(b(0))=a(0)=1, a(b(1))=a(2)=2, a(b(2))=a(1)=0
    assert list(result) == [1, 2, 0]
    # check that providing a tuple as second argument works (per docstring)
    result2 = Permutation.rmul(a, [0, 2, 1])
    assert result2 == result

def test_rmul_multiple_args_and_ordering():
    # test with three permutations
    p = Permutation([2, 0, 1, 3])   # 0->2,1->0,2->1,3->3
    q = Permutation([1, 2, 0, 3])   # 0->1,1->2,2->0,3->3
    r = Permutation([0, 1, 3, 2])   # swap 2 and 3
    # rmul(p, q, r) should compute p(q(r(i))) for each i
    res = Permutation.rmul(p, q, r)
    expected = [None]*4
    for i in range(4):
        expected[i] = p(q(r(i)))
    assert list(res) == expected
    # Compare with iterative application to ensure correct reverse-order behavior
    # (note: '*' operator does the other order: (p*q)(i) == p(q(i)) normally,
    # but rmul applies reverse args so rmul(p, q) == q*p)
    left = Permutation.rmul(p, q)
    right = q * p
    assert left == right

def test_rmul_single_arg_is_returned():
    # When only one argument passed, it should simply return that argument unchanged.
    s = Permutation([1, 0])
    out = Permutation.rmul(s)
    assert out is s  # should return the same object (no composition performed)

def test_rmul_type_error_on_non_permutation_first_arg():
    # The implementation expects the first argument to be a Permutation (so that subsequent
    # items can be parsed). If the first arg is not a Permutation, attempts to call
    # __mul__ on subsequent args will raise. We ensure that passing a non-Permutation first
    # argument results in an AttributeError/TypeError when .__mul__ is missing.
    class Dummy:
        pass
    dummy = Dummy()
    with pytest.raises(Exception):
        # Use something that doesn't implement __mul__ with Permutation to provoke failure.
        Permutation.rmul(dummy, [0, 1])

def test_rmul_with_identity_and_size_mismatch():
    # Permutation of different sizes: ensure composition still works by implicit sizing rules.
    # Create identity of size 5 and a smaller permutation of size 3.
    id5 = Permutation(list(range(5)))
    small = Permutation([1, 0, 2])  # size 3
    # rmul(id5, small) should compute id5(small(i)) == small(i) for i in range(3),
    # but the resulting permutation's list will be according to id5*small behavior.
    res = Permutation.rmul(id5, small)
    # For indices 0..2 result should equal small applied then id5 (id keeps value).
    assert list(res)[:3] == list(small)
    # Conversely, rmul(small, id5) should apply small(id5(i)) == small(i)
    res2 = Permutation.rmul(small, id5)
    assert list(res2)[:3] == list(small)

def test_rmul_raises_with_incompatible_objects():
    # If later args cannot be multiplied with the running rv, __mul__ should raise TypeError
    p = Permutation([0, 1])
    class NoMul:
        def __init__(self): pass
    nm = NoMul()
    with pytest.raises(TypeError):
        Permutation.rmul(p, nm)