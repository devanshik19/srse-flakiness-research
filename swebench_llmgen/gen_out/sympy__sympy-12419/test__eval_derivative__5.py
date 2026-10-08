import pytest
from sympy import Matrix, MatrixBase, Symbol, Integer, KroneckerDelta, S
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.core import Basic

def make_matrix_element(parent, i, j):
    # Construct a MatrixElement directly using the class interface.
    # The MatrixElement.__new__ normally takes (cls, name, n, m) for matrix symbols,
    # but MatrixElement instances are normally created by indexing an expression:
    # e.g. M[i, j] where M is a MatrixSymbol or MatrixExpr. To be robust in tests,
    # create a small concrete Matrix and index it to get a MatrixElement.
    return parent[i, j]

def test_eval_derivative_with_non_matrixelement_and_matrixparent():
    # parent is a concrete Matrix (MatrixBase). Request derivative w.r.t a Symbol.
    M = Matrix([[1, 2], [3, 4]])
    me = make_matrix_element(M, 0, 1)  # element M[0,1] == 2
    v = Symbol('x')
    # For a Matrix parent, _eval_derivative should call parent's diff and then index.
    # Matrix.diff on a Symbol returns a matrix of zeros, so the element should be 0.
    res = me._eval_derivative(v)
    assert res == S.Zero

def test_eval_derivative_with_non_matrixelement_and_non_matrixparent():
    # parent is not a MatrixBase subclass: use a generic Basic to simulate
    class Dummy(Basic):
        pass
    D = Dummy()
    # Create a MatrixElement-like object manually using MatrixElement.__new__ pattern by
    # leveraging a small MatrixSymbol-like object: simplest is to use Matrix([[x]]) and index,
    # but to ensure parent isn't MatrixBase, create a fake parent stored into the element.
    # We'll construct a MatrixElement from a 1x1 Matrix and then monkeypatch its parent.
    M = Matrix([[Symbol('a')]])
    me = make_matrix_element(M, 0, 0)
    # replace parent with non-MatrixBase object
    object.__setattr__(me, 'parent', D)
    res = me._eval_derivative(Symbol('y'))
    assert res == S.Zero

def test_eval_derivative_with_matrixelement_and_same_parent_and_same_indices():
    # When v is a MatrixElement with the same parent and same indices,
    # derivative should be KroneckerDelta(i, i')*KroneckerDelta(j, j') -> 1
    M = Matrix([[Symbol('a'), Symbol('b')], [Symbol('c'), Symbol('d')]])
    me = make_matrix_element(M, 0, 1)
    v = make_matrix_element(M, 0, 1)
    res = me._eval_derivative(v)
    # indices equal, so KroneckerDelta(0,0)*KroneckerDelta(1,1) = 1
    assert res == KroneckerDelta(Integer(0), Integer(0)) * KroneckerDelta(Integer(1), Integer(1))
    assert res == Integer(1)

def test_eval_derivative_with_matrixelement_and_same_parent_different_indices():
    M = Matrix([[1,2],[3,4]])
    me = make_matrix_element(M, 0, 1)
    v = make_matrix_element(M, 1, 0)
    res = me._eval_derivative(v)
    # indices differ, so at least one KroneckerDelta is zero -> overall zero
    assert res == KroneckerDelta(Integer(0), Integer(1)) * KroneckerDelta(Integer(1), Integer(0))
    assert res == Integer(0)

def test_eval_derivative_with_matrixelement_different_parent():
    # If v is a MatrixElement but from a different parent, derivative is S.Zero
    M1 = Matrix([[1,2],[3,4]])
    M2 = Matrix([[5,6],[7,8]])
    me = make_matrix_element(M1, 0, 0)
    v = make_matrix_element(M2, 0, 0)
    res = me._eval_derivative(v)
    assert res == S.Zero