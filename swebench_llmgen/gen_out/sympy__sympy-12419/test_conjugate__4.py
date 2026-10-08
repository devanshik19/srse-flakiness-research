import pytest
from sympy import Symbol, I, Matrix, Integer
from sympy.matrices.expressions.matexpr import MatrixExpr
from sympy.functions.elementary.complexes import conjugate as sympy_conjugate
from sympy.matrices.expressions.matexpr import MatMul, MatAdd, Transpose, Inverse

# We create a tiny subclass to instantiate MatrixExpr because MatrixExpr is abstract-like
class DummyMatrixExpr(MatrixExpr):
    """
    Minimal concrete MatrixExpr for testing conjugate behavior.
    It stores a single symbolic entry and exposes required methods used by tests.
    """
    _iterable = ()
    is_Matrix = True
    is_MatrixExpr = True
    is_commutative = False

    def __new__(cls, name, rows=1, cols=1):
        name = Symbol(name) if not hasattr(name, 'free_symbols') else name
        obj = Basic.__new__(cls)
        obj._name = name
        obj._rows = rows
        obj._cols = cols
        return obj

    def __repr__(self):
        return f"DummyMatrixExpr({self._name})"

    def _eval_conjugate(self):
        # Return conjugate of the underlying symbol (so conjugate(DummyMatrixExpr(x)) -> DummyMatrixExpr(conjugate(x)))
        return DummyMatrixExpr(sympy_conjugate(self._name), self._rows, self._cols)

    def _eval_transpose(self):
        # simple transpose: swap dims
        return DummyMatrixExpr(self._name, self._cols, self._rows)

    def _eval_adjoint(self):
        # adjoint = transpose + conjugate
        return DummyMatrixExpr(sympy_conjugate(self._name), self._cols, self._rows)

    def rows(self):
        return self._rows

    def cols(self):
        return self._cols

    def as_explicit(self):
        # return a SymPy Matrix for explicit checks
        return Matrix([[self._name]])

def test_conjugate_delegates_to_sympy_conjugate():
    x = Symbol('x')
    m = DummyMatrixExpr(x)
    # MatrixExpr.conjugate should call sympy.functions.conjugate, which for DummyMatrixExpr
    # will use _eval_conjugate and produce DummyMatrixExpr(conjugate(x))
    c = m.conjugate()
    assert isinstance(c, DummyMatrixExpr)
    assert c._name == sympy_conjugate(x)

def test_conjugate_of_complex_entry():
    # Test that conjugating an expression with I flips the sign of imaginary part
    m = DummyMatrixExpr(1 + 2*I)  # underlying is a SymPy expression
    c = m.conjugate()
    # Underlying name should be conjugated
    assert c._name == sympy_conjugate(1 + 2*I)
    assert c._name == 1 - 2*I

def test_conjugate_preserves_shape_and_interacts_with_transpose_and_adjoint():
    x = Symbol('a')
    m = DummyMatrixExpr(x, rows=2, cols=3)
    # Conjugate should preserve shape (as implemented in _eval_conjugate)
    c = m.conjugate()
    assert c.rows() == 2 and c.cols() == 3

    # Transpose then conjugate vs adjoint
    t = m._eval_transpose()
    ct = t.conjugate()
    adj = m._eval_adjoint()
    # adjoint should equal conjugate(transpose)
    assert isinstance(adj, DummyMatrixExpr)
    assert isinstance(ct, DummyMatrixExpr)
    assert adj._name == ct._name
    assert adj.rows() == ct.rows() and adj.cols() == ct.cols()

def test_conjugate_on_explicit_matrix_roundtrip():
    # Ensure that as_explicit can be used after conjugation (integration test)
    m = DummyMatrixExpr(1 + I)
    me = m.conjugate().as_explicit()
    # as_explicit should yield a 1x1 Matrix with conjugated entry
    assert isinstance(me, Matrix)
    assert me.shape == (1, 1)
    assert me[0, 0] == 1 - I

def test_conjugate_composition_with_sympy_functions():
    # Verify that applying sympy.conjugate externally matches MatrixExpr.conjugate
    x = Symbol('z')
    m = DummyMatrixExpr(x)
    from sympy.functions import conjugate as ext_conj
    assert m.conjugate()._name == ext_conj(m._name)

# Run tests when executing the module directly (useful for quick checks)
if __name__ == "__main__":
    pytest.main([__file__])