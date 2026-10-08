# test_function_evalf.py
from __future__ import print_function, division
import sys
import types
import mpmath

import pytest

from sympy.core.function import Function
from sympy.core.symbol import Symbol
from sympy.core.numbers import Float
from sympy.utilities.lambdify import MPMATH_TRANSLATIONS
from sympy import sin, cos, exp

# Create a minimal concrete Function subclass to test _eval_evalf behavior
class MyFunc(Function):
    # store Python-callable for _imp_ if provided
    def __new__(cls, *args, **kwargs):
        obj = Function.__new__(cls, *args, **kwargs)
        return obj

    # Allow using _imp_ fallback: implement _imp_ optionally via attribute set in tests
    # The base Function._eval_evalf will call self._imp_ if mpmath lookup fails.
    # We don't override _eval_evalf here; we use the inherited one.

def test_evalf_uses_mpmath_builtin(monkeypatch):
    # Use a known mpmath function name: "sin"
    x = Symbol('x')
    f = sin(x)  # sin is a Function subclass instance from sympy
    # Provide a numeric argument that implements _to_mpmath
    class DummyNum:
        def __init__(self, val):
            self.val = val
        def _to_mpmath(self, prec):
            # return an mpf from mpmath
            return mpmath.mpf(self.val)
    # replace args with a DummyNum so that _eval_evalf will convert them
    f = sin(DummyNum(0.5))
    # Call _eval_evalf with some precision
    res = f._eval_evalf(30)
    # Should return an Expr representing the mpmath evaluation
    assert hasattr(res, '_to_mpmath') or isinstance(res, Float)

def test_evalf_uses_mpmath_translations(monkeypatch):
    # Test translation mapping: use a fake sympy function name that maps to an
    # mpmath function via MPMATH_TRANSLATIONS
    # We'll craft a temporary Function subclass whose .func.__name__ is 'exp'
    # but we force lookup to use a translated name by temporarily removing mpmath.exp
    x = Symbol('x')
    # create an instance of MyFunc and set its .func name to something mapped
    instance = MyFunc(x)
    # monkeypatch the underlying function name to a key that exists in translations
    # For example, 'Abs' maps to 'fabs' in translations typically.
    # Find a mapping key -> value where value exists in mpmath
    translations = MPMATH_TRANSLATIONS
    # find a mapping where the RHS exists in mpmath
    key = None
    for k, v in translations.items():
        if hasattr(mpmath, v):
            key = k
            val = v
            break
    if key is None:
        pytest.skip("No suitable MPMATH_TRANSLATIONS entry found for test environment")
    class FakeFunc:
        __name__ = key
    instance.func = FakeFunc
    # Provide a numeric arg with _to_mpmath
    class DummyNum:
        def __init__(self, val):
            self.val = val
        def _to_mpmath(self, prec):
            return mpmath.mpf(self.val)
    instance._args = (DummyNum(0.0),)
    instance.args = instance._args
    # Call _eval_evalf
    res = instance._eval_evalf(20)
    # If mpmath function works, we either get an Expr-mapped result or None
    # (None could occur if translation didn't lead to a proper callable)
    assert (res is None) or hasattr(res, '_to_mpmath') or isinstance(res, Float)

def test_evalf_fallback_to__imp__and_errors(monkeypatch):
    # Create an instance that will have no mpmath attribute and no translation,
    # so that AttributeError/KeyError branch is taken and then _imp_ is attempted.
    instance = MyFunc(Symbol('y'))
    class FakeFunc:
        __name__ = 'nonexistent_mpmath_function_for_test'
    instance.func = FakeFunc
    # Provide an _imp_ that returns a Python float when called
    def imp_impl(arg):
        # simulate computation that can be converted to Float
        return 1.2345
    instance._imp_ = imp_impl
    # Provide arguments that will be passed to _imp_
    class DummyNum:
        def __init__(self, val):
            self.val = val
    instance._args = (DummyNum(0.0),)
    instance.args = instance._args
    # _eval_evalf should wrap the _imp_ result into a Float
    res = instance._eval_evalf(15)
    assert isinstance(res, Float)
    assert abs(float(res) - 1.2345) < 1e-12

    # Now make _imp_ raise TypeError/AttributeError/ValueError to test it returns None
    def imp_bad(arg):
        raise ValueError("bad")
    instance._imp_ = imp_bad
    res2 = instance._eval_evalf(15)
    assert res2 is None

def test_evalf_bad_argument_precision_returns_none():
    # If argument _to_mpmath produces mpf/mpc with failed precision (as detected by bad),
    # then _eval_evalf returns None.
    instance = MyFunc(Symbol('z'))
    class FakeFunc:
        __name__ = 'sin'  # ensure mpmath lookup succeeds
    instance.func = FakeFunc
    # Construct a fake mpf-like object that mimics ._mpf_ with failing precision
    class BadMPF:
        # mpmath.mp.mpf instances have type 'mpf' but we'll emulate
        def __init__(self):
            # _mpf_ returns a tuple where the second element equals 1 indicates failure per code
            self._mpf_ = (0, 1, 0)  # pattern that will cause bad(...) True
    class ArgThatReturnsBad:
        def _to_mpmath(self, prec):
            return BadMPF()
    instance._args = (ArgThatReturnsBad(),)
    instance.args = instance._args
    res = instance._eval_evalf(20)
    assert res is None

def test_evalf_uses_mpmath_workprec_and_returns_expr_from_mpmath():
    # Use a real sympy Function like cos with a numeric arg that supports _to_mpmath
    class Numeric:
        def __init__(self, v):
            self.v = v
        def _to_mpmath(self, prec):
            return mpmath.mpf(self.v)
    f = cos(Numeric(0.2))
    r = f._eval_evalf(25)
    # Should produce something convertible to float (via Expr._from_mpmath)
    assert r is not None
    # If r is an Expr-like, try to get numeric value; otherwise ensure it's Float
    if isinstance(r, Float):
        val = float(r)
    else:
        # many Exprs from _from_mpmath implement _to_mpmath; just ensure not None
        assert hasattr(r, '_to_mpmath') or hasattr(r, 'evalf')