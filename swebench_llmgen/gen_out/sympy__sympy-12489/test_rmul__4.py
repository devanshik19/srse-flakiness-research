import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_permutations():
    # simple permutations as lists
    a = Permutation([1, 0, 2])  # swaps 0 and 1
    b = Permutation([0, 2, 1])  # swaps 1 and 2
    # rmul(a, b) should compute a(b(i)) for each i
    r = Permutation.rmul(a, b)
    assert isinstance(r, Permutation)
    assert list(r) == [1, 2, 0]
    # check that this is equal to applying a after b pointwise
    assert [a(b(i)) for i in range(3)] == [1, 2, 0]

def test_rmul_tuple_and_permutation_mix():
    # first argument must be a Permutation instance (per docstring)
    a = Permutation([1, 0, 2])
    # second can be a raw tuple/list
    tup = [0, 2, 1]
    r1 = Permutation.rmul(a, tup)
    r2 = Permutation.rmul(a, Permutation(tup))
    assert r1 == r2
    assert list(r1) == [1, 2, 0]

def test_rmul_multiple_arguments_associativity_like():
    # Test with three permutations: rmul(a, b, c) = c*b*a applied appropriately
    a = Permutation([2, 0, 1, 3])  # 3-cycle on 0,2,1
    b = Permutation([1, 2, 0, 3])  # 3-cycle on 0,1,2
    c = Permutation([0, 3, 2, 1])  # transposition 1<->3
    # According to rmul, rv = args[0]; for i in 1.., rv = args[i]*rv
    # So result = c * b * a (i.e., apply a, then b, then c)
    r = Permutation.rmul(a, b, c)
    # verify by pointwise application: result(i) == c(b(a(i)))
    assert all(r(i) == c(b(a(i))) for i in range(4))
    # also verify list form
    assert list(r) == [c(b(a(i))) for i in range(4)]

def test_rmul_reverse_order_differs_from_mul_operator():
    # confirm rmul handles reverse of the * operator operands
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # a*b uses __mul__ defined as a after b? The docstring indicates rmul handles reverse.
    prod_mul = list(a*b)   # uses __mul__
    prod_rmul = list(Permutation.rmul(a, b))
    # They should generally differ for non-commuting permutations
    assert prod_mul != prod_rmul
    # And prod_rmul equals [a(b(i)) for i]
    assert prod_rmul == [a(b(i)) for i in range(3)]
    # while prod_mul equals [b(a(i)) for i]
    assert prod_mul == [b(a(i)) for i in range(3)]

def test_rmul_single_argument_returns_same_object():
    # rmul with single argument should just return that argument unchanged
    a = Permutation([1, 0, 2])
    r = Permutation.rmul(a)
    # Might be the same object or equivalent; equality suffices
    assert r == a
    # identity check
    assert list(r) == list(a)

def test_rmul_errors_when_first_not_permutation():
    # Per docstring, first item must be a Permutation for others to be parsed.
    # If first is not a Permutation, multiplication will rely on object's __mul__
    # which should raise when unsupported. We assert TypeError is raised in that case.
    non_perm = [1, 0, 2]  # plain list
    other = Permutation([0, 2, 1])
    with pytest.raises(TypeError):
        # Attempting rmul with first arg a list and second a Permutation should fail
        Permutation.rmul(non_perm, other)