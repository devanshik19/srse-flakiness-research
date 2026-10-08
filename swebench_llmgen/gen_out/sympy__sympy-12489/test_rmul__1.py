import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_two_permutations():
    # a(i) = [1,0,2] means a: 0->1,1->0,2->2
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # rmul(a, b) should compute a(b(i))
    r = Permutation.rmul(a, b)
    assert list(r) == [1, 2, 0]
    # verify pointwise composition
    assert [a(b(i)) for i in range(3)] == list(r)

def test_rmul_with_tuple_operand():
    # first arg must be a Permutation instance; later args can be sequences
    a = Permutation([1, 0, 2])
    # provide second operand as raw sequence (tuple/list)
    r1 = Permutation.rmul(a, [0, 2, 1])
    r2 = Permutation.rmul(a, Permutation([0, 2, 1]))
    assert r1 == r2
    assert list(r1) == [1, 2, 0]

def test_rmul_multiple_operands():
    # chain three permutations: result is a(b(c(i)))
    a = Permutation([2, 0, 1, 3])
    b = Permutation([1, 2, 3, 0])
    c = Permutation([3, 0, 1, 2])
    r = Permutation.rmul(a, b, c)
    # compute expected by direct application
    expected = [a(b(c(i))) for i in range(4)]
    assert list(r) == expected

def test_rmul_single_operand_returns_same():
    p = Permutation([1, 0, 2, 3])
    # rmul with single argument should return that argument unchanged
    r = Permutation.rmul(p)
    assert r == p
    assert list(r) == list(p)

def test_rmul_raises_if_first_not_permutation():
    # The implementation assumes first arg behaves like a Permutation.
    # Passing a plain list as first argument would make rmul try to call
    # list * something which should raise a TypeError.
    with pytest.raises(TypeError):
        Permutation.rmul([1, 0, 2], Permutation([0, 2, 1]))

def test_rmul_commutation_order_difference():
    # Ensure rmul handles reverse of __mul__ ordering:
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    prod_rmul = Permutation.rmul(a, b)  # a(b(i))
    prod_mul = a * b                   # a.__mul__(b) yields (a after b?) check inequality
    # These two are generally not equal (order matters); assert they are different here
    assert prod_rmul != prod_mul