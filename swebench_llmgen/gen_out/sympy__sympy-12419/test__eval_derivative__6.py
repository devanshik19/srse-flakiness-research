import pytest
from sympy import Matrix, MatrixBase, KroneckerDelta, S, symbols
from sympy.matrices.expressions.matexpr import MatrixElement

def make_matrix_element(parent, i, j):
    # Create a MatrixElement-like object using the MatrixElement constructor
    # MatrixElement.__new__(cls, name, n, m) signature from prompt suggests different,
    # but we can construct by calling MatrixElement(parent, i, j) as typical usage.
    return MatrixElement(parent, i, j)

def test_eval_derivative_with_non_matrixelement_and_parent_matrixbase():
    # parent is a concrete Matrix (subclass of MatrixBase)
    M = Matrix([[1, 2], [3, 4]])
    me = make_matrix_element(M, 0, 1)  # element M[0,1] == 2
    x = symbols('x')
    # derivative of a concrete Matrix w.r.t. x is zero matrix; but MatrixBase.diff exists and returns zero
    res = me._eval_derivative(x)
    # Since parent is a Matrix and does not depend on x, result should be the (0,1) entry of zero -> 0
    assert res == S.Zero

def test_eval_derivative_with_non_matrixelement_and_parent_not_matrixbase():
    class DummyParent:
        pass
    parent = DummyParent()
    me = make_matrix_element(parent, 0, 0)
    x = symbols('x')
    res = me._eval_derivative(x)
    assert res == S.Zero

def test_eval_derivative_with_matrixelement_different_parent():
    # If v is a MatrixElement but from a different parent, derivative should be 0
    M1 = Matrix([[1, 2], [3, 4]])
    M2 = Matrix([[5, 6], [7, 8]])
    me1 = make_matrix_element(M1, 0, 0)
    me2 = make_matrix_element(M2, 0, 0)
    res = me1._eval_derivative(me2)
    assert res == S.Zero

def test_eval_derivative_with_matrixelement_same_parent_matching_indices():
    M = Matrix([[1, 2], [3, 4]])
    me = make_matrix_element(M, 1, 0)
    v = make_matrix_element(M, 1, 0)
    res = me._eval_derivative(v)
    # Expect KroneckerDelta(i,i)*KroneckerDelta(j,j) -> 1*1 = 1
    assert res == KroneckerDelta(1,1)*KroneckerDelta(0,0)
    # simplify to ensure it's 1
    assert res.doit() == 1

def test_eval_derivative_with_matrixelement_same_parent_different_indices():
    M = Matrix([[1, 2], [3, 4]])
    me = make_matrix_element(M, 0, 1)
    v = make_matrix_element(M, 1, 0)
    res = me._eval_derivative(v)
    # Different indices lead to product of deltas that is zero
    assert res == KroneckerDelta(0,1)*KroneckerDelta(1,0)
    # simplify to 0
    assert res.doit() == 0