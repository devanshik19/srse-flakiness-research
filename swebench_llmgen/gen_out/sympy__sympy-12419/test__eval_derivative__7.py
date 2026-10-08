import pytest
from sympy import Matrix, symbols, Integer, KroneckerDelta, S
from sympy.matrices.expressions.matexpr import MatrixElement

def make_matrix_element(mat, i, j):
    # Create a MatrixElement-like object using the class constructor
    # MatrixElement.__new__(cls, name, n, m) expects parent, i, j when created normally.
    # But public construction for testing: use MatrixElement(mat, i, j)
    return MatrixElement(mat, i, j)

def test_derivative_with_non_matrixelement_and_parent_is_matrixbase():
    a, b = symbols('a b')
    # Parent is a concrete Matrix (MatrixBase)
    M = Matrix([[a, b], [b, a]])
    me = make_matrix_element(M, 0, 1)  # element (0,1) -> b
    # differentiate with respect to symbol b
    d = me._eval_derivative(b)
    # Should be derivative of parent matrix wrt b, then element (0,1) selected.
    # d/d b of M is Matrix([[0,1],[1,0]]), so element (0,1) == 1
    assert d == Integer(1)

    # differentiate with respect to a (element (0,0) and (1,1)), element (0,1) should be 0
    d2 = me._eval_derivative(a)
    assert d2 == Integer(0)

def test_derivative_with_non_matrixelement_and_parent_not_matrixbase():
    x = symbols('x')
    # Use a parent that is not a MatrixBase: e.g., a plain Symbol (not having diff returning MatrixBase)
    parent = symbols('P')  # Symbol has no MatrixBase behavior
    me = make_matrix_element(parent, 0, 0)
    # derivative with respect to x should return 0 (S.Zero)
    d = me._eval_derivative(x)
    assert d is S.Zero

def test_derivative_with_matrixelement_same_parent_and_same_indices():
    # Two MatrixElement objects from the same parent and same indices
    P = Matrix([[1, 2], [3, 4]])
    me1 = make_matrix_element(P, 0, 1)
    me2 = make_matrix_element(P, 0, 1)
    d = me1._eval_derivative(me2)
    # Should be KroneckerDelta(i,i) * KroneckerDelta(j,j) == 1*1 = 1
    assert d == KroneckerDelta(Integer(0), Integer(0)) * KroneckerDelta(Integer(1), Integer(1))
    # Evaluate to integer 1
    assert int(d) == 1

def test_derivative_with_matrixelement_different_parents_or_indices():
    P = Matrix([[1, 2], [3, 4]])
    Q = Matrix([[5, 6], [7, 8]])
    me = make_matrix_element(P, 0, 1)
    # Different parent
    other_parent = make_matrix_element(Q, 0, 1)
    d_parent = me._eval_derivative(other_parent)
    assert d_parent == S.Zero

    # Same parent but different i
    other_i = make_matrix_element(P, 1, 1)
    d_i = me._eval_derivative(other_i)
    assert d_i == S.Zero

    # Same parent but different j
    other_j = make_matrix_element(P, 0, 0)
    d_j = me._eval_derivative(other_j)
    assert d_j == S.Zero