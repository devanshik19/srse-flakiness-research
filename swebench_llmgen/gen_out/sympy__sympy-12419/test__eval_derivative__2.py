import pytest
from sympy import Matrix, MatrixBase, Symbol, Integer, S, KroneckerDelta
from sympy.matrices.expressions.matexpr import MatrixElement

def make_matrix_element(mat, i, j):
    # Construct a MatrixElement-like object using the class's __new__ if available,
    # otherwise create a simple surrogate. Here we assume MatrixElement.__new__
    # accepts (name, n, m) per the provided signature, but we can create actual
    # Matrix objects and access their elements via MatrixElement(mat, i, j) usage.
    # The sympy Matrix supports .diff and indexing, and MatrixElement should accept
    # a MatrixBase parent; create a MatrixElement by calling MatrixElement(mat, i, j)
    return MatrixElement(mat, i, j)

def test_derivative_with_non_matrixelement_and_matrixparent():
    # Create a concrete Matrix (MatrixBase) parent
    x = Symbol('x')
    M = Matrix([[x, x], [Integer(0), Integer(1)]])
    # Create a MatrixElement pointing to entry (0,0)
    me = MatrixElement(M, 0, 0)
    # Differentiate with respect to x (a Symbol). According to implementation,
    # it should delegate to parent.diff(x) and then index the result at [i,j].
    d = me._eval_derivative(x)
    # parent.diff(x) for the matrix yields a matrix with 1 at positions with x, else 0.
    # So entry (0,0) is 1
    assert d == Integer(1)

def test_derivative_with_non_matrixelement_and_non_matrixparent_returns_zero():
    # Create a dummy parent that's not a MatrixBase and a MatrixElement over it.
    class DummyParent:
        def diff(self, v):
            raise RuntimeError("should not be called")
    parent = DummyParent()
    me = MatrixElement(parent, 0, 0)
    # Differentiate with respect to a Symbol; since parent is not MatrixBase,
    # implementation should return S.Zero
    d = me._eval_derivative(Symbol('y'))
    assert d == S.Zero

def test_derivative_with_matrixelement_different_parent_returns_zero():
    # Two different parents
    M1 = Matrix([[1, 2]])
    M2 = Matrix([[1, 2]])
    me1 = MatrixElement(M1, 0, 1)
    me2 = MatrixElement(M2, 0, 1)
    # They are MatrixElement instances but with different parent (args[0] differs)
    d = me1._eval_derivative(me2)
    assert d == S.Zero

def test_derivative_with_same_matrixelement_returns_kronecker():
    M = Matrix([[1, 2], [3, 4]])
    # same parent
    me_a = MatrixElement(M, 0, 1)
    me_b = MatrixElement(M, 0, 1)
    d = me_a._eval_derivative(me_b)
    # Should be KroneckerDelta(i,i')*KroneckerDelta(j,j') which is 1
    assert d == KroneckerDelta(me_a.args[1], me_b.args[1]) * KroneckerDelta(me_a.args[2], me_b.args[2])
    assert d == Integer(1)

def test_derivative_with_same_parent_but_different_indices():
    M = Matrix([[1, 2], [3, 4]])
    me = MatrixElement(M, 0, 0)
    me_diff = MatrixElement(M, 1, 0)
    d = me._eval_derivative(me_diff)
    # Different row index -> KroneckerDelta(0,1)=0 => overall 0
    assert d == Integer(0)