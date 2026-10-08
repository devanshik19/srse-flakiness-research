import pytest
from sympy import Symbol, I, conjugate as sympy_conjugate
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.matrices.expressions.matmul import MatMul
from sympy.matrices.expressions.matadd import MatAdd
from sympy.matrices.expressions.transpose import Transpose
from sympy.matrices.expressions.inverse import Inverse
from sympy.matrices.expressions.matpow import MatPow
from sympy.core import Integer, Expr

# We'll create a minimal concrete subclass of MatrixExpr so we can instantiate objects.
class _DummyMatrixExpr(MatrixExpr):
    """
    Minimal concrete implementation of MatrixExpr for testing conjugate.
    It stores a single Expr element to simulate behavior.
    """
    def __new__(cls, expr):
        # sympify the expr to ensure it's a SymPy Expr
        expr = Expr(expr) if not isinstance(expr, Expr) else expr
        obj = Expr.__new__(cls, expr)
        obj._expr = expr
        return obj

    # implement representation helpers that some operations might expect
    def __repr__(self):
        return f"_DummyMatrixExpr({self._expr!r})"

    # required methods used by other MatrixExpr routines; minimal implementations
    def _eval_conjugate(self):
        # Return the conjugate applied to the internal expression
        return _DummyMatrixExpr(sympy_conjugate(self._expr))

    def _eval_transpose(self):
        # For testing, transpose just returns self (or a wrapper)
        return Transpose(self)

    def _eval_inverse(self):
        return Inverse(self)

    def _eval_power(self, exp):
        return MatPow(self, exp)

    def _eval_simplify(self):
        return self

    def _eval_adjoint(self):
        return MatMul((self.T,))  # arbitrary non-None object

    def _entry(self, i, j):
        # pretend a 1x1 matrix containing the stored expr
        if i != 0 or j != 0:
            raise IndexError("out of bounds")
        return self._expr

    def rows(self):
        return 1

    def cols(self):
        return 1

    @property
    def T(self):
        # simulate transpose attribute
        return Transpose(self)

# Helper to access sympy.conjugate for internal use
from sympy import conjugate as sympy_conjugate

def test_conjugate_returns_conjugate_object():
    # Create a Dummy containing a symbolic expression
    x = Symbol('x')
    d = _DummyMatrixExpr(x + I)
    # MatrixExpr.conjugate should call sympy.functions.conjugate on the object,
    # which will in turn use the subclass's _eval_conjugate implementation.
    c = d.conjugate()
    # Expect the result to be a _DummyMatrixExpr wrapping conjugate(x + I)
    assert isinstance(c, _DummyMatrixExpr)
    assert c._expr == sympy_conjugate(x + I)

def test_conjugate_on_real_expr_is_real():
    # If the internal expr is real (Integer), conjugate should be same value
    d = _DummyMatrixExpr(Integer(5))
    c = d.conjugate()
    assert isinstance(c, _DummyMatrixExpr)
    # conjugate of 5 is 5
    assert c._expr == Integer(5)

def test_conjugate_combines_with_other_matrix_ops():
    # Ensure conjugate can be called on composite matrix expressions built
    # from MatrixExpr subclass instances. Use MatMul and MatAdd wrappers.
    a = _DummyMatrixExpr(Symbol('a') + I)
    b = _DummyMatrixExpr(Symbol('b'))
    # MatMul and MatAdd accept MatrixExpr instances; build combined exprs
    mm = MatMul(a, b)
    ma = MatAdd(a, b)
    # calling conjugate on those should return sympy.conjugate applied
    # to the MatMul/MatAdd object (which will not error)
    cm = mm.conjugate()
    ca = ma.conjugate()
    # Should return an Expr (MatrixExpr or wrapper), not raise
    assert hasattr(cm, 'args')
    assert hasattr(ca, 'args')

def test_conjugate_on_transpose_inverse_pow_delegation():
    # For completeness, ensure that conjugate can be called on other wrappers
    x = _DummyMatrixExpr(Symbol('z') + I)
    t = Transpose(x)
    inv = Inverse(x)
    p = MatPow(x, 2)
    # Should not raise; result should be an Expr-like object
    assert hasattr(t.conjugate(), 'args')
    assert hasattr(inv.conjugate(), 'args')
    assert hasattr(p.conjugate(), 'args')

def test_conjugate_preserves_type_for_custom_eval():
    # If subclass implements _eval_conjugate to return something else,
    # conjugate() should return that value.
    class Custom(_DummyMatrixExpr):
        def _eval_conjugate(self):
            return "custom-result"

    inst = Custom(Symbol('y') + I)
    res = inst.conjugate()
    assert res == "custom-result"