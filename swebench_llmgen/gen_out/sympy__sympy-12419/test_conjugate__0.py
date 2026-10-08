import pytest
from sympy import Symbol, I, Integer
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.functions import conjugate as sympy_conjugate
from sympy.matrices import MatrixBase
from sympy.core import S

# Create a minimal concrete subclass of MatrixExpr for testing
class DummyMatrix(MatrixExpr):
    """
    A tiny concrete MatrixExpr subclass that holds a single scalar entry
    for simplicity. Implements necessary methods used in tests.
    """
    def __new__(cls, entry):
        obj = Basic.__new__(cls)
        obj._entry = entry
        # mark some flags expected by MatrixExpr API
        obj.is_Matrix = True
        obj.is_MatrixExpr = True
        obj.is_commutative = getattr(entry, "is_commutative", False)
        return obj

    def _eval_conjugate(self):
        # Mirror SymPy behavior: return conjugated entry wrapped in same type
        return DummyMatrix(sympy_conjugate(self._entry))

    def __repr__(self):
        return f"DummyMatrix({self._entry!r})"

    # Minimal implementations for other MatrixExpr expected methods used by tests:
    def as_explicit(self):
        return self

    def __eq__(self, other):
        return isinstance(other, DummyMatrix) and self._entry == other._entry

def test_conjugate_delegates_to_sympy_conjugate():
    # Real scalar should remain the same
    m_real = DummyMatrix(Integer(3))
    res_real = m_real.conjugate()
    assert isinstance(res_real, DummyMatrix)
    assert res_real._entry == Integer(3)
    # Imaginary scalar should get conjugated (I -> -I)
    m_imag = DummyMatrix(2*I)
    res_imag = m_imag.conjugate()
    assert isinstance(res_imag, DummyMatrix)
    assert res_imag._entry == -2*I

def test_conjugate_uses__eval_conjugate_if_present():
    # Ensure that if subclass defines _eval_conjugate it is used.
    # Our DummyMatrix defines _eval_conjugate to wrap conjugated entry.
    x = Symbol('x')
    m = DummyMatrix(x + I)
    res = m.conjugate()
    assert isinstance(res, DummyMatrix)
    # The entry should be conjugated
    assert res._entry == sympy_conjugate(x + I)

def test_conjugate_idempotent_on_real_entries():
    # Conjugating a real-valued entry twice yields same result
    m = DummyMatrix(Integer(5))
    res1 = m.conjugate()
    res2 = res1.conjugate()
    assert res1 == res2