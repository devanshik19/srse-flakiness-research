import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_two_permutations():
    # a(i) = [1,0,2] means a: 0->1,1->0,2->2
    # b(i) = [0,2,1] means b: 0->0,1->2,2->1
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # rmul should compute a(b(i)) when called as rmul(a, b)
    prod = Permutation.rmul(a, b)
    assert list(prod) == [1, 2, 0]
    # confirm elementwise application: a(b(i)) matches
    assert [a(b(i)) for i in range(3)] == [1, 2, 0]

def test_rmul_order_differs_from_mul():
    # using same permutations, normal multiplication a*b is b then a?
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    mul_prod = a * b
    rmul_prod = Permutation.rmul(a, b)
    # they should differ (as documented): rmul does a(b(i)); a*b gives b(a(i))
    assert list(mul_prod) != list(rmul_prod)
    assert list(mul_prod) == [2, 0, 1]
    assert list(rmul_prod) == [1, 2, 0]

def test_rmul_with_tuple_and_permutation():
    # first arg must be a Permutation instance; subsequent args can be sequences
    a = Permutation([2, 0, 1])  # cycle (0 2 1)
    tuple_b = (0, 2, 1)         # same as Permutation([0,2,1])
    prod = Permutation.rmul(a, tuple_b)
    # should interpret tuple_b as Permutation and compute a(tuple_b(i))
    assert isinstance(prod, Permutation)
    assert list(prod) == [1, 2, 0]

def test_rmul_multiple_operands():
    # Chain multiple permutations: result should be a(b(c(i)))
    a = Permutation([1, 2, 0, 3])  # sends 0->1,1->2,2->0,3->3
    b = Permutation([2, 0, 1, 3])
    c = Permutation([1, 0, 3, 2])
    # rmul(a, b, c) -> a(b(c(i)))
    res = Permutation.rmul(a, b, c)
    expected = [a(b(c(i))) for i in range(4)]
    assert list(res) == expected

def test_rmul_single_operand_returns_same_object():
    a = Permutation([1, 0, 2])
    # rmul with only one argument should return that argument unchanged
    res = Permutation.rmul(a)
    assert res == a

def test_rmul_type_error_if_first_not_permutation():
    # The implementation assumes first arg supports * as permutation multiplication.
    # If first arg is a plain tuple, subsequent parsing won't be attempted per doc.
    with pytest.raises(TypeError):
        Permutation.rmul((0,1,2), Permutation([0,1,2]))