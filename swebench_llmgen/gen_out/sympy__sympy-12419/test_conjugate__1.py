import pytest
from sympy import Symbol, I, Integer
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.functions.elementary.complexes import conjugate as sympy_conjugate

# We'll create a minimal concrete subclass of MatrixExpr to test the conjugate method.
class DummyMatrix(MatrixExpr):
    """
    Minimal concrete MatrixExpr for testing purposes.
    We implement only what is necessary so that the conjugate method
    (which delegates to sympy.functions.conjugate) can be exercised.
    """
    def __new__(cls, value):
        # store a single field 'value' so we can inspect behavior
        obj = Basic.__new__(cls)
        obj.value = value
        return obj

    def _eval_conjugate(self):
        # if value has its own conjugate, return a new DummyMatrix wrapping that
        return DummyMatrix(sympy_conjugate(self.value))

    def __repr__(self):
        return f"DummyMatrix({self.value!r})"

    # provide equality for assertions
    def __eq__(self, other):
        return isinstance(other, DummyMatrix) and self.value == other.value

# Tests

def test_conjugate_delegates_to_sympy_conjugate_on_symbolic():
    x = Symbol('x')
    m = DummyMatrix(x)
    # conjugate should call sympy.conjugate; for a Symbol this is just conjugate(Symbol) (unevaluated)
    res = m.conjugate()
    # since our DummyMatrix._eval_conjugate returns a DummyMatrix wrapping conjugate(x)
    assert isinstance(res, DummyMatrix)
    assert str(res.value) == str(sympy_conjugate(x))

def test_conjugate_handles_imaginary_unit_inside():
    # If the internal value is I (imaginary unit), conjugate should produce -I inside DummyMatrix
    m = DummyMatrix(I)
    res = m.conjugate()
    assert isinstance(res, DummyMatrix)
    assert res.value == -I

def test_conjugate_on_numeric():
    # Numeric values should be handled too
    m = DummyMatrix(Integer(3))
    res = m.conjugate()
    assert isinstance(res, DummyMatrix)
    assert res.value == Integer(3)

def test_conjugate_returns_type_preserved():
    # Ensure conjugate returns the same wrapper type even when inner conjugate is itself
    inner = sympy_conjugate(Symbol('y'))
    m = DummyMatrix(inner)
    res = m.conjugate()
    assert isinstance(res, DummyMatrix)
    # inner was already a conjugate object; applying conjugate again yields conjugate(conjugate(y))
    assert str(res.value).startswith("conjugate")

def test_conjugate_does_not_mutate_original():
    x = Symbol('z')
    m = DummyMatrix(x)
    res = m.conjugate()
    # original should stay the same
    assert m.value == x
    assert res.value != m.value or str(res.value) != str(m.value)