import pytest
from sympy import Symbol, I, Integer, conjugate as sympy_conjugate
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.core.basic import Basic

# We need a concrete subclass of MatrixExpr to instantiate and test.
# Create minimal stub implementations to exercise MatrixExpr.conjugate.
class DummyMatrix(MatrixExpr):
    """
    A minimal concrete MatrixExpr subclass to test conjugate behavior.
    It stores a single element (which can be a scalar or an expression).
    """

    def __new__(cls, element):
        # element should be sympifiable; store as .element attribute
        obj = Basic.__new__(cls)
        obj.element = element
        return obj

    # Implement required methods used by MatrixExpr or tests minimally.
    @property
    def is_Matrix(self):
        return True

    @property
    def is_MatrixExpr(self):
        return True

    def _eval_conjugate(self):
        # Define a specific conjugation behavior for this dummy:
        # return a new DummyMatrix with the conjugated element
        return DummyMatrix(sympy_conjugate(self.element))

    def __repr__(self):
        return f"DummyMatrix({self.element!r})"

    def __eq__(self, other):
        return isinstance(other, DummyMatrix) and self.element == other.element


def test_conjugate_calls_internal_eval_conjugate():
    # Create a dummy with a complex element and ensure conjugate() returns
    # result of _eval_conjugate (i.e., conjugating the stored element).
    x = DummyMatrix(1 + 2*I)
    res = x.conjugate()
    # The element should have been conjugated
    assert isinstance(res, DummyMatrix)
    assert res.element == sympy_conjugate(1 + 2*I)
    assert res.element == 1 - 2*I

def test_conjugate_on_symbolic_element_without__eval_conjugate():
    # Create a different subclass that does not implement _eval_conjugate to
    # exercise fallback behavior in sympy.conjugate for MatrixExpr objects.
    class NoEvalConj(MatrixExpr):
        def __new__(cls, element):
            obj = Basic.__new__(cls)
            obj.element = element
            return obj

        def __repr__(self):
            return f"NoEvalConj({self.element!r})"

        def __eq__(self, other):
            return isinstance(other, NoEvalConj) and self.element == other.element

    s = Symbol('a') + I
    m = NoEvalConj(s)
    # sympy.conjugate will try to call _eval_conjugate; since not present,
    # it should return conjugate applied at the expression level wrapped by
    # sympy.conjugate (which for unknown MatrixExpr types may return a
    # AppliedUndef-like object). However, calling m.conjugate() should
    # not raise; it should return sympy.conjugate(m).
    res = m.conjugate()
    # It should be an expression (Basic) and equal to sympy.conjugate(m)
    assert hasattr(res, "__class__")
    assert sympy_conjugate(m) == res

def test_conjugate_idempotent_and_non_mutating():
    # Ensure calling conjugate does not mutate original object and is idempotent
    d = DummyMatrix(3 + 4*I)
    d2 = d.conjugate()
    d3 = d2.conjugate()
    # Original remains unchanged
    assert d.element == 3 + 4*I
    # d2 is conjugated once, d3 twice -> should equal original
    assert d2.element == 3 - 4*I
    assert d3.element == 3 + 4*I

def test_conjugate_on_real_element_returns_same_value():
    # If element is real, conjugation should leave it unchanged
    d = DummyMatrix(Integer(5))
    res = d.conjugate()
    assert isinstance(res, DummyMatrix)
    assert res.element == Integer(5)