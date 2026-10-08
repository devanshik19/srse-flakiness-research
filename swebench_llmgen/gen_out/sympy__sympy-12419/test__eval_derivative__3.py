import pytest
from sympy import Matrix, Symbol, Integer, S, KroneckerDelta
from sympy.matrices.expressions.matexpr import MatrixElement
from sympy.core import Basic

def test_eval_derivative_with_non_matrixelement_and_parent_matrix():
    # Create a concrete Matrix parent and a MatrixElement referring to it
    M = Matrix([[1, 2], [3, 4]])
    # MatrixElement expects (parent, i, j) where parent is matrix expression
    me = MatrixElement(M, Integer(0), Integer(1))
    # differentiate w.r.t a symbol (non-MatrixElement). The code checks isinstance(v, MatrixElement)
    x = Symbol('x')
    # Since parent is a MatrixBase (concrete Matrix), it will call parent.diff(x)[i,j].
    # A concrete Matrix's diff w.r.t a symbol returns a zero matrix, so element is 0
    res = me._eval_derivative(x)
    assert res == S.Zero

def test_eval_derivative_with_non_matrixelement_and_parent_not_matrix():
    # parent is a Basic (not a MatrixBase), create a MatrixElement with Basic parent
    parent = Basic()  # not a MatrixBase
    me = MatrixElement(parent, Integer(1), Integer(0))
    x = Symbol('x')
    # parent is not a MatrixBase, so should return S.Zero
    res = me._eval_derivative(x)
    assert res == S.Zero

def test_eval_derivative_with_matrixelement_different_parent():
    # two MatrixElement instances with different parents -> derivative zero
    parent1 = Basic()
    parent2 = Basic()
    me1 = MatrixElement(parent1, Integer(0), Integer(0))
    me2 = MatrixElement(parent2, Integer(0), Integer(0))
    res = me1._eval_derivative(me2)
    assert res == S.Zero

def test_eval_derivative_with_matrixelement_same_parent_same_indices():
    # same parent and same indices -> KroneckerDelta( i, i ) * KroneckerDelta( j, j ) => 1
    parent = Basic()
    i = Integer(0)
    j = Integer(1)
    me = MatrixElement(parent, i, j)
    res = me._eval_derivative(me)
    # Expect KroneckerDelta(i,i)*KroneckerDelta(j,j) which simplifies to 1
    assert (res == KroneckerDelta(i, i) * KroneckerDelta(j, j))
    # evaluate numerically/simplify to 1
    assert res.doit() == Integer(1)

def test_eval_derivative_with_matrixelement_same_parent_different_indices():
    # same parent but different indices -> product of deltas, one will be zero
    parent = Basic()
    me1 = MatrixElement(parent, Integer(0), Integer(0))
    me2 = MatrixElement(parent, Integer(0), Integer(1))
    res = me1._eval_derivative(me2)
    # KroneckerDelta(0,0)*KroneckerDelta(0,1) => 1*0 = 0
    assert res == KroneckerDelta(Integer(0), Integer(0)) * KroneckerDelta(Integer(0), Integer(1))
    assert res.doit() == Integer(0)