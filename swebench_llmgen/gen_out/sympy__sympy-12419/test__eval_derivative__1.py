import pytest
from sympy import MatrixBase, Matrix, symbols, KroneckerDelta, S
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.core import Integer
from sympy.core.symbol import Symbol

def make_matrix_element(parent, i, j):
    # Construct a MatrixElement-like object using the class constructor signature:
    # MatrixElement(name, n, m) actually in sympy creates an expression representing an element.
    # But for testing _eval_derivative we can directly create via MatrixElement(parent, i, j)
    # However the actual MatrixElement __new__ signature in sympy is (parent, i, j).
    return MatrixElement(parent, i, j)

def test_derivative_wrt_same_matrix_element_returns_kronecker():
    A = Matrix([[1, 2], [3, 4]])
    me1 = make_matrix_element(A, Integer(0), Integer(1))
    me2 = make_matrix_element(A, Integer(0), Integer(1))

    d = me1._eval_derivative(me2)
    # Expect KroneckerDelta(i,i)*KroneckerDelta(j,j) -> 1
    assert isinstance(d, KroneckerDelta)
    # Evaluate the product: KroneckerDelta(0,0)*KroneckerDelta(1,1) equals 1
    assert d.doit() == 1 or d == KroneckerDelta(0, 0) * KroneckerDelta(1, 1)

def test_derivative_wrt_different_indices_returns_zero():
    A = Matrix([[1, 2], [3, 4]])
    me = make_matrix_element(A, Integer(0), Integer(1))
    me_diff = make_matrix_element(A, Integer(1), Integer(1))

    d = me._eval_derivative(me_diff)
    # Different row index -> KroneckerDelta(0,1)*KroneckerDelta(1,1) => 0
    assert d == S.Zero or (hasattr(d, 'doit') and d.doit() == 0)

def test_derivative_wrt_different_parent_returns_zero():
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 6], [7, 8]])
    meA = make_matrix_element(A, Integer(0), Integer(0))
    meB = make_matrix_element(B, Integer(0), Integer(0))

    d = meA._eval_derivative(meB)
    assert d == S.Zero

def test_derivative_wrt_non_matrixelement_and_parent_is_matrixbase():
    # If v is not a MatrixElement, but self.parent is a MatrixBase, it should return parent.diff(v)[i,j]
    x = symbols('x')
    A = Matrix([[x, 2], [3, 4]])
    me = make_matrix_element(A, Integer(0), Integer(0))

    # differentiate w.r.t x
    d = me._eval_derivative(x)
    # parent.diff(x) is Matrix([[1,0],[0,0]]), so element (0,0) is 1
    assert d == 1 or d == Integer(1)

def test_derivative_wrt_non_matrixelement_and_parent_not_matrixbase_returns_zero():
    # Create a dummy parent that is not a MatrixBase
    class DummyParent:
        def diff(self, v):
            # should not be called for this test (parent isn't a MatrixBase)
            raise RuntimeError("diff called unexpectedly")

    parent = DummyParent()
    me = make_matrix_element(parent, Integer(0), Integer(0))
    # differentiate w.r.t some Symbol
    s = Symbol('s')
    d = me._eval_derivative(s)
    assert d == S.Zero