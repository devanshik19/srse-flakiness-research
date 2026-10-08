import pytest
from sympy import Symbol, I, conjugate as sympy_conjugate
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.matrices.expressions.transpose import Transpose
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.matadd import MatAdd
from sympy import Matrix

# Create a minimal concrete subclass to instantiate MatrixExpr behavior
class DummyMatrix(MatrixExpr):
    """
    Minimal concrete MatrixExpr for testing conjugate behavior.
    It wraps a scalar/symbolic entry and pretends to be a 1x1 matrix.
    """

    def __new__(cls, entry):
        # Use MatrixExpr.__new__ semantics: create an instance with the entry stored
        obj = Basic.__new__(cls)
        obj._entry_val = entry
        return obj

    @property
    def shape(self):
        return (1, 1)

    def _entry(self, i, j):
        if (i, j) != (0, 0):
            raise IndexError("only 1x1 dummy")
        return self._entry_val

    # implement required eval methods minimally
    def _eval_conjugate(self):
        # If the wrapped entry has conjugate, return a new DummyMatrix with it
        return DummyMatrix(sympy_conjugate(self._entry_val))

    def as_explicit(self):
        # return a 1x1 sympy Matrix for easier comparisons
        return Matrix([[self._entry_val]])

    def __repr__(self):
        return f"DummyMatrix({self._entry_val!r})"


def test_conjugate_calls_sympy_conjugate_via_method():
    x = Symbol('x')
    dm = DummyMatrix(x + I)
    # MatrixExpr.conjugate should call sympy.functions.conjugate which triggers _eval_conjugate
    c = dm.conjugate()
    # The result should be a DummyMatrix wrapping the conjugated entry
    assert isinstance(c, DummyMatrix)
    assert c._entry_val == sympy_conjugate(x + I)
    # conjugating again yields original (since conjugate of conjugate)
    assert c.conjugate()._entry_val == sympy_conjugate(sympy_conjugate(x + I))


def test_conjugate_with_transpose_and_inverse_composition():
    # Compose expressions using existing MatrixExpr subclasses to ensure conjugate delegates correctly.
    # Use DummyMatrix as base operand.
    a = DummyMatrix(1 + I)
    # transpose and inverse are MatrixExpr operations; ensure conjugate can be called on composed objects
    t = Transpose(a)
    inv = Inverse(a)
    mm = MatMul(a, t)
    ma = MatAdd(a, a)

    # Conjugate should be callable and return an expression (not raise)
    for expr in (a, t, inv, mm, ma):
        res = expr.conjugate()
        # The result should be an Expr or MatrixExpr instance; ensure method exists
        assert hasattr(res, 'conjugate')
        # calling conjugate on result should not raise
        _ = res.conjugate()


def test_conjugate_preserves_type_on_zero_and_real():
    # Test that conjugate of purely real entries yields same numeric value
    r = DummyMatrix(3)
    cr = r.conjugate()
    assert isinstance(cr, DummyMatrix)
    assert cr._entry_val == 3

    # Test zero-like entry
    z = DummyMatrix(0)
    cz = z.conjugate()
    assert cz._entry_val == 0


def test_conjugate_integration_with_sympy_conjugate_function():
    # Ensure that calling the top-level sympy.conjugate on a MatrixExpr uses the MatrixExpr.conjugate
    a = DummyMatrix(2 + 3*I)
    # sympy_conjugate dispatch should call a._eval_conjugate via MatrixExpr.conjugate
    from sympy.functions import conjugate as top_conjugate
    res = top_conjugate(a)
    # result must be a DummyMatrix wrapping conjugated entry
    assert isinstance(res, DummyMatrix)
    assert res._entry_val == sympy_conjugate(2 + 3*I)