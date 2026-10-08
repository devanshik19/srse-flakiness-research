import pytest
from sympy import Matrix, symbols, Integer, S, KroneckerDelta
from sympy.matrices.expressions.matexpr import MatrixElement

def make_matrix_element(parent, i, j):
    # construct a MatrixElement-like object using the class's __new__ signature:
    # __new__(cls, name, n, m) - but we can instead directly instantiate via parent[i,j]
    # However MatrixElement expects (parent, i, j) in its args normally; create via parent[i,j]
    return parent[i, j]

def test_eval_derivative_with_non_matrixelement_and_matrix_parent():
    x = symbols('x')
    M = Matrix([[x, 2], [3, 4]])
    # create a MatrixElement pointing to (0,0)
    me = make_matrix_element(M, 0, 0)
    # derivative wrt symbol x: underlying parent is a Matrix (MatrixBase)
    d = me._eval_derivative(x)
    # derivative of parent Matrix wrt x is a Matrix with 1 in (0,0); element should be 1
    assert d == Integer(1)

def test_eval_derivative_with_non_matrixelement_and_non_matrix_parent():
    # create a dummy parent that is not MatrixBase and has no diff method
    class Dummy:
        def __init__(self):
            self._mat = [[1]]
        def __getitem__(self, key):
            return self._mat[key[0]][key[1]]
    dummy = Dummy()
    # construct a MatrixElement-like object by bypassing typical parent type:
    # Use MatrixElement.__new__ to create an instance whose parent is dummy.
    me = MatrixElement.__new__(MatrixElement, dummy, 0, 0)
    # derivative wrt a Symbol should be S.Zero because parent is not MatrixBase
    from sympy import Symbol
    d = me._eval_derivative(Symbol('y'))
    assert d == S.Zero

def test_eval_derivative_with_matrixelement_different_parent():
    # create two different matrix parents
    A = Matrix([[1, 0], [0, 1]])
    B = Matrix([[1, 2], [3, 4]])
    ae = make_matrix_element(A, 0, 1)
    be = make_matrix_element(B, 0, 1)
    # derivative of ae wrt be should be zero because parents differ
    d = ae._eval_derivative(be)
    assert d == S.Zero

def test_eval_derivative_with_matrixelement_same_parent_and_indices():
    # parent same and indices same -> KroneckerDelta(i,i)*KroneckerDelta(j,j) = 1
    P = Matrix([[1, 2], [3, 4]])
    me1 = make_matrix_element(P, 1, 0)
    me2 = make_matrix_element(P, 1, 0)
    d = me1._eval_derivative(me2)
    assert d == KroneckerDelta(1, 1)*KroneckerDelta(0, 0)
    # simplify to ensure it's 1
    from sympy import simplify
    assert simplify(d) == Integer(1)

def test_eval_derivative_with_matrixelement_same_parent_different_indices():
    P = Matrix([[1, 2], [3, 4]])
    me = make_matrix_element(P, 0, 0)
    other = make_matrix_element(P, 1, 0)
    d = me._eval_derivative(other)
    # different row index -> one KroneckerDelta is zero => overall zero
    assert d == KroneckerDelta(0, 1)*KroneckerDelta(0, 0)
    from sympy import simplify
    assert simplify(d) == Integer(0)