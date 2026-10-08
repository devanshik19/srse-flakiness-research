import pytest
from sympy import Matrix, symbols, Integer, KroneckerDelta, S
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.core import Symbol

def make_matrix_element_from_matrix(mat, i, j):
    # MatrixElement normally takes an expression parent and indices.
    # The MatrixElement.__new__ signature in sympy is MatrixElement(parent, i, j)
    return MatrixElement(mat, Integer(i), Integer(j))

def test_eval_derivative_with_non_matrixbase_and_non_matrixelement():
    # If v is not a MatrixElement and parent is not a MatrixBase, should return 0
    # Create a MatrixElement with a plain SymPy Expr as parent
    x = Symbol('x')
    me = MatrixElement(x, Integer(0), Integer(1))
    # v is a plain Symbol (not MatrixElement)
    res = me._eval_derivative(x)
    assert res == S.Zero

def test_eval_derivative_with_matrixbase_parent_and_non_matrixelement():
    # If v is not a MatrixElement and parent is a MatrixBase, call parent.diff(v)[i,j]
    a, b = symbols('a b')
    M = Matrix([[a, b], [b, a]])
    me = make_matrix_element_from_matrix(M, 1, 0)  # element M[1,0] is b
    # differentiate with respect to symbol b: expecting derivative 1 at that entry
    res = me._eval_derivative(b)
    # parent.diff(b) is a matrix with derivative entries; extract at [1,0]
    expected = M.diff(b)[1, 0]
    assert res == expected
    assert res == Integer(1)

def test_eval_derivative_with_matrixelement_different_parent():
    # If v is a MatrixElement but different parent -> zero
    M1 = Matrix([[1, 2], [3, 4]])
    M2 = Matrix([[5, 6], [7, 8]])
    me1 = make_matrix_element_from_matrix(M1, 0, 0)
    me2 = make_matrix_element_from_matrix(M2, 0, 0)
    res = me1._eval_derivative(me2)
    assert res == S.Zero

def test_eval_derivative_with_matrixelement_same_parent_same_indices():
    # If both are MatrixElement of same parent and same indices -> product of KroneckerDeltas equals 1
    M = Matrix([[Symbol('x')]])
    me = make_matrix_element_from_matrix(M, 0, 0)
    v = make_matrix_element_from_matrix(M, 0, 0)
    res = me._eval_derivative(v)
    # KroneckerDelta(0,0)*KroneckerDelta(0,0) == 1
    assert res == KroneckerDelta(Integer(0), Integer(0)) * KroneckerDelta(Integer(0), Integer(0))
    assert res == Integer(1)

def test_eval_derivative_with_matrixelement_same_parent_different_indices():
    # Same parent but different indices -> one KroneckerDelta is zero -> result 0
    M = Matrix([[1,2],[3,4]])
    me = make_matrix_element_from_matrix(M, 0, 1)
    v = make_matrix_element_from_matrix(M, 1, 0)
    res = me._eval_derivative(v)
    assert res == KroneckerDelta(Integer(0), Integer(1)) * KroneckerDelta(Integer(1), Integer(0))
    assert res == Integer(0)