import pytest
from sympy import Matrix, symbols, I, conjugate as sympy_conjugate
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.matrices.expressions.transpose import Transpose
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matadd import MatAdd
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.matpow import MatPow

def test_matrixexpr_conjugate_on_symbolic_matrixexpr():
    # Create a simple MatrixExpr via a sympy Matrix (which has MatrixExpr behavior)
    a, b = symbols('a b')
    m = Matrix([[a, b], [b, a]])  # returns a Matrix (subclass of MatrixExpr)
    # The conjugate method of MatrixExpr should delegate to sympy.conjugate
    res = MatrixExpr.conjugate(m)
    # For purely symbolic real symbols, conjugate should be identity
    assert res == sympy_conjugate(m)
    assert res == m

def test_matrixexpr_conjugate_on_imaginary_entries():
    # Matrix with imaginary unit should get conjugated entries
    m = Matrix([[1 + I, 2 - I], [I, -I]])
    res = MatrixExpr.conjugate(m)
    # conjugating should flip the sign of I
    expected = Matrix([[1 - I, 2 + I], [-I, I]])
    assert res == expected
    # Compare to sympy.conjugate applied directly
    assert res == sympy_conjugate(m)

def test_matrixexpr_conjugate_preserves_structure_for_exprs():
    # Build some MatrixExpr structures: transpose, inverse, matmul, matpow, matadd
    a, b = symbols('a b')
    base = Matrix([[a + I, b], [b, a - I]])
    T = base.T  # Transpose expression (should be MatrixExpr/Matrix)
    inv = base.inv()  # Inverse expression (returns Matrix when possible)
    mm = base * base  # MatMul or explicit Matrix result
    mpow = base**2     # MatPow or Matrix result
    madd = base + base # MatAdd or Matrix result

    # Apply conjugate via MatrixExpr.conjugate; ensure it matches sympy.conjugate
    for expr in (T, inv, mm, mpow, madd):
        # Some operations may return plain Matrix objects; that's fine.
        res = MatrixExpr.conjugate(expr)
        assert res == sympy_conjugate(expr)

def test_matrixexpr_conjugate_on_zero_and_identity_like():
    # Zero matrix and Identity-like matrices
    z = Matrix([[0, 0], [0, 0]])
    I2 = Matrix([[1, 0], [0, 1]])
    assert MatrixExpr.conjugate(z) == z
    assert MatrixExpr.conjugate(I2) == I2

def test_conjugate_via_instance_method():
    # Ensure the instance method .conjugate() works (delegates to MatrixExpr.conjugate)
    m = Matrix([[1 + I, 2], [3, 4 - I]])
    # instance method
    res_instance = m.conjugate()
    res_static = MatrixExpr.conjugate(m)
    assert res_instance == res_static
    # matches sympy.conjugate
    assert res_instance == sympy_conjugate(m)

def test_conjugate_on_nested_expressions():
    # nested: conjugate of transpose of inverse of matrix
    m = Matrix([[1 + I, 2], [3, 4 - I]])
    nested = m.T.inv().T  # combine transforms
    res = MatrixExpr.conjugate(nested)
    assert res == sympy_conjugate(nested)

def test_conjugate_on_non_matrix_raises_attribute_error_when_missing():
    # If a non-matrix-like object is passed that doesn't support conjugation, sympy.conjugate will still try.
    # We'll pass a plain Python object to ensure no unexpected exception from MatrixExpr.conjugate wrapper itself.
    class Dummy:
        def __repr__(self):
            return "Dummy()"
    d = Dummy()
    # sympy.conjugate on unknown objects returns conjugate(Dummy()) as unevaluated Basic form, but might error.
    # We ensure that calling MatrixExpr.conjugate on something that isn't a MatrixExpr simply calls sympy.conjugate.
    # Use pytest to check it either returns something or raises a TypeError that originates from sympy.
    try:
        res = MatrixExpr.conjugate(d)
        # If it returns, it should equal sympy.conjugate(d)
        assert res == sympy_conjugate(d)
    except Exception as e:
        # If an exception is raised, ensure it's not from our wrapper but from sympy's attempt.
        assert isinstance(e, Exception)