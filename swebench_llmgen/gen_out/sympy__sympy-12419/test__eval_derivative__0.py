import pytest
from sympy import MatrixBase, Matrix, Symbol, Integer, S, KroneckerDelta
from sympy.matrices.expressions.matexpr import MatrixElement

def make_matrix_element(parent, i, j):
    # Construct a minimal MatrixElement-like object using the class constructor
    # MatrixElement.__new__(cls, name, n, m) expects (name, n, m) per signature;
    # but the actual MatrixElement instances used in sympy have .parent, .i, .j.
    # We'll create an instance via the provided constructor and then set fields.
    me = MatrixElement.__new__(MatrixElement, parent, i, j)
    # If __new__ didn't set attributes, set them explicitly for tests
    if not hasattr(me, 'parent'):
        me.parent = parent
    if not hasattr(me, 'i'):
        me.i = i
    if not hasattr(me, 'j'):
        me.j = j
    return me

def test_eval_derivative_with_non_matrixelement_and_matrix_parent():
    # v is not a MatrixElement; parent is a MatrixBase (Matrix) so parent.diff should be used
    A = Matrix([[Symbol('a11'), Symbol('a12')], [Symbol('a21'), Symbol('a22')]])
    # Create a MatrixElement referring to A[0,1]
    me = make_matrix_element(A, Integer(0), Integer(1))

    # differentiate with respect to a scalar Symbol
    v = Symbol('a11')
    # The parent's diff will produce a matrix of derivatives; then indexing [i,j]
    res = me._eval_derivative(v)
    # derivative of A[0,1] with respect to a11 is 0
    assert res == S.Zero

    # differentiate with respect to the exact element A[0,1] symbol
    v2 = Symbol('a12')
    res2 = me._eval_derivative(v2)
    # derivative of A[0,1] wrt a12 is 1
    assert res2 == Integer(1)

def test_eval_derivative_non_matrixelement_non_matrix_parent():
    # parent is not a MatrixBase and v is not MatrixElement -> should return 0
    parent = Symbol('M')  # not a MatrixBase
    me = make_matrix_element(parent, Integer(1), Integer(2))
    v = Symbol('x')
    assert me._eval_derivative(v) == S.Zero

def test_eval_derivative_with_matrixelement_different_parent():
    # v is a MatrixElement but with a different parent -> should return 0
    parent1 = Symbol('P1')
    parent2 = Symbol('P2')
    me1 = make_matrix_element(parent1, Integer(0), Integer(0))
    me2 = make_matrix_element(parent2, Integer(0), Integer(0))
    # ensure they are seen as MatrixElement instances
    assert isinstance(me1, MatrixElement) and isinstance(me2, MatrixElement)
    assert me1._eval_derivative(me2) == S.Zero

def test_eval_derivative_with_matrixelement_same_parent_matching_indices():
    # same parent and same indices -> should return product of KroneckerDeltas
    parent = Symbol('M')
    me = make_matrix_element(parent, Integer(1), Integer(2))
    v = make_matrix_element(parent, Integer(1), Integer(2))
    res = me._eval_derivative(v)
    # expect KroneckerDelta(1,1)*KroneckerDelta(2,2) -> 1*1 = 1
    assert res == KroneckerDelta(Integer(1), Integer(1))*KroneckerDelta(Integer(2), Integer(2))
    # simplify to 1
    assert res.doit() == Integer(1) or res == Integer(1)

def test_eval_derivative_with_matrixelement_same_parent_mismatched_indices():
    parent = Symbol('M')
    me = make_matrix_element(parent, Integer(1), Integer(2))
    # different i
    v_i = make_matrix_element(parent, Integer(0), Integer(2))
    res_i = me._eval_derivative(v_i)
    assert res_i == KroneckerDelta(Integer(1), Integer(0))*KroneckerDelta(Integer(2), Integer(2))
    # different j
    v_j = make_matrix_element(parent, Integer(1), Integer(0))
    res_j = me._eval_derivative(v_j)
    assert res_j == KroneckerDelta(Integer(1), Integer(1))*KroneckerDelta(Integer(2), Integer(0))
    # both different
    v_both = make_matrix_element(parent, Integer(0), Integer(0))
    res_both = me._eval_derivative(v_both)
    assert res_both == KroneckerDelta(Integer(1), Integer(0))*KroneckerDelta(Integer(2), Integer(0))