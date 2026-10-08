import pytest
from sympy import Matrix, I, symbols
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.functions.elementary.complexes import conjugate as conj_func
from sympy.matrices.expressions import MatMul, MatAdd
from sympy import Integer

# We will create a tiny subclass of MatrixExpr to test the conjugate method.
# The real MatrixExpr is abstract and many methods/fields are not needed for this test.
class DummyMatrixExpr(MatrixExpr):
    # minimal implementation: store a wrapped SymPy matrix-like expression (for testing)
    def __new__(cls, base):
        # base is any SymPy Expr or Matrix; store it as .arg for inspection
        obj = Basic.__new__(cls)
        obj.arg = base
        return obj

    def _eval_conjugate(self):
        # delegate to wrapped arg's conjugate to simulate typical behaviour
        return DummyMatrixExpr(conj_func(self.arg))

    def __repr__(self):
        return f"DummyMatrixExpr({self.arg!r})"

    # implement equality to help assertions
    def __eq__(self, other):
        return isinstance(other, DummyMatrixExpr) and self.arg == other.arg

def test_conjugate_delegates_to_conjugate_function():
    # scalar inside dummy: conjugate should wrap the conjugated inner object
    x = symbols('x')
    dm = DummyMatrixExpr(I + x)
    # MatrixExpr.conjugate should return the SymPy conjugate applied to the object.
    res = MatrixExpr.conjugate(dm)
    # The DummyMatrixExpr._eval_conjugate returns DummyMatrixExpr(conjugated arg)
    assert isinstance(res, DummyMatrixExpr)
    assert res.arg == conj_func(I + x)

def test_conjugate_with_integer_and_zero():
    # integer should remain the same under conjugation
    dm = DummyMatrixExpr(Integer(3))
    res = MatrixExpr.conjugate(dm)
    assert isinstance(res, DummyMatrixExpr)
    assert res.arg == Integer(3)

    # zero remains zero
    dm0 = DummyMatrixExpr(Integer(0))
    res0 = MatrixExpr.conjugate(dm0)
    assert res0.arg == Integer(0)

def test_conjugate_on_nested_expressions():
    # ensure conjugation works when inner arg is an expression like a MatAdd/MatMul-like placeholder
    a, b = symbols('a b')
    # use simple SymPy expressions that mimic matrix expressions for the purpose of conjugation
    inner = a + I*b
    dm = DummyMatrixExpr(inner)
    res = MatrixExpr.conjugate(dm)
    # conjugate(a + I*b) => a - I*b
    assert res.arg == conj_func(inner)
    assert res.arg == a - I*b

def test_conjugate_returns_object_of_same_class():
    # The result should preserve the MatrixExpr subclass type if _eval_conjugate does so
    dm = DummyMatrixExpr(I)
    res = dm.conjugate()
    assert isinstance(res, DummyMatrixExpr)
    assert res.arg == conj_func(I)