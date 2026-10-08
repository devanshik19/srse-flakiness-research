import pytest
from sympy import Matrix, MatrixBase, Symbol, Integer, KroneckerDelta, S
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.matrices.expressions.matexpr import MatMul  # imported to ensure package imports work


def test_eval_derivative_with_non_matrixelement_and_parent_matrixbase():
    # Create a concrete Matrix (MatrixBase) as parent
    M = Matrix([[Symbol('a'), Symbol('b')], [Symbol('c'), Symbol('d')]])
    # MatrixElement pointing to element (0,1)
    me = MatrixElement(M, 0, 1)
    # Differentiate with respect to a Symbol; should delegate to parent.diff and return that entry
    x = Symbol('a')
    res = me._eval_derivative(x)
    # parent.diff(x) will differentiate each entry; only entry (0,0) depends on 'a'.
    # So the derivative of M wrt 'a' is Matrix([[1,0],[0,0]]), thus me at (0,1) gives 0
    assert res == Integer(0)

    # Differentiate element at (0,0) with respect to Symbol('a') should return 1
    me00 = MatrixElement(M, 0, 0)
    res00 = me00._eval_derivative(x)
    assert res00 == Integer(1)


def test_eval_derivative_with_non_matrixelement_and_non_matrix_parent():
    # parent that is not a MatrixBase, e.g., a simple Symbol
    parent = Symbol('P')
    me = MatrixElement(parent, 0, 0)
    # differentiating with respect to a Symbol should return 0 because parent is not MatrixBase
    res = me._eval_derivative(Symbol('anything'))
    assert res == S.Zero


def test_eval_derivative_with_matrixelement_same_parent_and_indices():
    # When v is a MatrixElement with same parent and same indices, should return product of KroneckerDeltas
    parent = Symbol('A')  # parent can be any expression; since both MatrixElements have same parent, it should proceed
    me = MatrixElement(parent, 1, 2)
    v = MatrixElement(parent, 1, 2)
    res = me._eval_derivative(v)
    # expecting KroneckerDelta(i, i') * KroneckerDelta(j, j') => 1*1 = 1
    assert res == KroneckerDelta(1, 1) * KroneckerDelta(2, 2)
    assert res == Integer(1)

    # different column index -> KroneckerDelta yields 0
    v_diff_j = MatrixElement(parent, 1, 3)
    res_diff_j = me._eval_derivative(v_diff_j)
    assert res_diff_j == KroneckerDelta(1, 1) * KroneckerDelta(2, 3)
    assert res_diff_j == Integer(0)

    # different row index -> 0
    v_diff_i = MatrixElement(parent, 0, 2)
    res_diff_i = me._eval_derivative(v_diff_i)
    assert res_diff_i == KroneckerDelta(1, 0) * KroneckerDelta(2, 2)
    assert res_diff_i == Integer(0)


def test_eval_derivative_with_matrixelement_different_parent():
    # If v is a MatrixElement but parents differ, result should be zero
    parent1 = Symbol('A')
    parent2 = Symbol('B')
    me = MatrixElement(parent1, 0, 0)
    v = MatrixElement(parent2, 0, 0)
    res = me._eval_derivative(v)
    assert res == S.Zero