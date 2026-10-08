import pytest
from sympy import Symbol, I, S, conjugate as sympy_conjugate
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.transpose import Transpose
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matadd import MatAdd
from sympy.matrices.expressions.matpow import MatPow
from sympy.matrices import MatrixSymbol

# Create a minimal concrete subclass to instantiate MatrixExpr-like objects
class _DummyMatrixExpr(MatrixExpr):
    """
    Minimal concrete implementation to allow testing of MatrixExpr.conjugate.
    We implement only what's necessary for creating instances and getting
    a sensible string/representation for assertions.
    """
    def __new__(cls, name, rows=1, cols=1):
        # use MatrixSymbol for underlying behavior where helpful
        ms = MatrixSymbol(name, rows, cols)
        obj = Basic.__new__(cls, ms)
        obj._ms = ms
        return obj

    # Provide required methods/attributes used by other expression constructors
    @property
    def shape(self):
        return self._ms.shape

    def _eval_conjugate(self):
        # return a recognizable wrapper to see that _eval_conjugate is used when present
        return MatMul(sympy_conjugate(1), self)  # trivial MatMul so conjugate pipeline can proceed

    def __repr__(self):
        return f"_DummyMatrixExpr({self._ms.name})"

# Tests

def test_conjugate_calls_sympy_conjugate_for_scalar_like_matrix():
    a = _DummyMatrixExpr('A')
    # MatrixExpr.conjugate should call sympy.functions.conjugate on the object.
    # For our dummy, _eval_conjugate returns MatMul(conjugate(1), a) which simplifies to a form we can inspect.
    c = a.conjugate()
    # conjugate should return a SymPy expression (MatrixExpr/MatrixExpr subclass or expression)
    # Ensure result is not the original instance (since _eval_conjugate produces a wrapper)
    assert c is not a
    # The produced object should contain our dummy in its arguments (MatMul)
    # depending on MatMul repr, we at least ensure conjugate did not error and returned an object
    assert hasattr(c, 'args')

def test_conjugate_of_explicit_imaginary_scalar_in_matrix_expression():
    # Even though MatrixExpr objects are matrices, test conjugation interacts properly with scalar imaginaries
    x = _DummyMatrixExpr('X')
    # Multiply by I to create a MatMul that includes an imaginary scalar
    expr = MatMul(I, x)
    # Calling .conjugate() should apply conjugation: conjugate(I) = -I
    conj_expr = expr.conjugate()
    # The conjugate of MatMul(I, x) should be MatMul(conjugate(I), x.conjugate())
    # conjugate(I) is -I
    # Check that resulting expression contains -I somewhere in its args (or args of nested args)
    found_minus_I = False
    def walk(e):
        nonlocal found_minus_I
        if e == -I:
            found_minus_I = True
            return
        if hasattr(e, 'args'):
            for a in e.args:
                walk(a)
    walk(conj_expr)
    assert found_minus_I, "conjugate did not apply to scalar imaginary factor"

def test_conjugate_preserves_structure_for_transpose_inverse_and_powers():
    A = _DummyMatrixExpr('A', rows=2, cols=2)
    # Build combined expressions and ensure conjugate() runs without error and returns sensible types
    t = Transpose(A)
    inv = Inverse(A)
    powr = MatPow(A, 3)
    # Conjugate each; ensure no exceptions and that result is an expression
    for expr in (t, inv, powr):
        c = expr.conjugate()
        assert c is not None
        assert hasattr(c, 'args')

def test_conjugate_on_matadd_and_matmul_combination():
    A = _DummyMatrixExpr('A')
    B = _DummyMatrixExpr('B')
    add = MatAdd(A, B)
    mul = MatMul(A, B)
    # Should not raise and return an expression object
    cad = add.conjugate()
    cmu = mul.conjugate()
    assert hasattr(cad, 'args')
    assert hasattr(cmu, 'args')

def test_conjugate_idempotence_and_relation_with_sympy_conjugate():
    A = _DummyMatrixExpr('A')
    # For an object without special _eval_conjugate behavior, conjugate should at least delegate to sympy.conjugate
    # Using sympy_conjugate on the object should be same-callable as invoking .conjugate()
    c1 = A.conjugate()
    c2 = sympy_conjugate(A)
    # They should be structurally equal (SymPy equality)
    assert str(c1) == str(c2)  # comparing string forms as a robust proxy

# Ensure tests run when executed directly
if __name__ == "__main__":
    pytest.main([__file__])