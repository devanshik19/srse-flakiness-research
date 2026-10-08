import pytest
from sympy import Matrix, Symbol, I
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.functions.elementary.complexes import conjugate as sympy_conjugate

def test_matrixexpr_conjugate_on_dense_matrix():
    # Using a concrete Matrix (which is a MatrixExpr subclass) to test conjugate()
    x = Symbol('x')
    m = Matrix([[1, I], [x, 2]])
    # call the MatrixExpr.conjugate method (inherited by Matrix)
    result = MatrixExpr.conjugate(m)
    # conjugate should match sympy.conjugate applied elementwise
    expected = Matrix([[sympy_conjugate(1), sympy_conjugate(I)],
                       [sympy_conjugate(x), sympy_conjugate(2)]])
    assert result == expected

def test_matrixexpr_conjugate_on_zero_and_real_entries():
    m = Matrix([[0, 3], [3, 0]])
    result = MatrixExpr.conjugate(m)
    # all real entries remain the same
    assert result == m
    # conjugating twice returns original
    assert MatrixExpr.conjugate(result) == m

def test_matrixexpr_conjugate_on_symbolic_imaginary_unit():
    # Ensure I is handled
    m = Matrix([[I]])
    result = MatrixExpr.conjugate(m)
    assert result == Matrix([[-I]])

def test_conjugate_returns_matrixexpr_type():
    m = Matrix([[1]])
    # calling the instance method should return an object that behaves like MatrixExpr
    res = m.conjugate()
    assert hasattr(res, 'is_MatrixExpr')
    assert res.is_MatrixExpr

def test_conjugate_with_mutable_and_immutable_consistency():
    # check both as_mutable/as_explicit paths don't break conjugate
    m = Matrix([[1, I]])
    # explicit dense matrix conjugation
    res1 = MatrixExpr.conjugate(m)
    # using the instance method
    res2 = m.conjugate()
    assert res1 == res2

def test_conjugate_on_empty_matrix():
    m = Matrix([]).reshape(0, 0)
    res = MatrixExpr.conjugate(m)
    assert res.shape == (0, 0)

def test_conjugate_on_nonmatrix_raises_attributeerror():
    # Ensure that calling MatrixExpr.conjugate with a non-matrix-like raises
    with pytest.raises(AttributeError):
        # an integer does not have matrix attributes expected by MatrixExpr methods
        MatrixExpr.conjugate(5)