# test_function_evalf.py
from __future__ import print_function, division
import pytest
import mpmath
from mpmath import mpf, mpc
from sympy.core.function import Function
from sympy.core.numbers import Float, Rational, Float as SymFloat
from sympy.core.symbol import Symbol
from sympy import sin, exp
from sympy.utilities.lambdify import MPMATH_TRANSLATIONS

# We'll create small dummy Function subclasses to exercise different branches
class SimpleFunc(Function):
    # Give a python-level name for lookup in mpmath: use 'sin' which exists
    @property
    def func(self):
        # use the existing sympy sin wrapper (a FunctionClass), but only its .__name__
        return sin.func

    def __new__(cls, *args):
        obj = Function.__new__(cls, *args)
        return obj

class TranslatedFunc(Function):
    # name that isn't directly in mpmath but is in MPMATH_TRANSLATIONS
    @property
    def func(self):
        class Dummy:
            __name__ = 'E'  # MPMATH_TRANSLATIONS maps 'E' -> 'e' typically
        return Dummy()

    def __new__(cls, *args):
        obj = Function.__new__(cls, *args)
        return obj

class NoMpmathFunc(Function):
    # a function with no mpmath equivalent and without _imp_
    @property
    def func(self):
        class Dummy:
            __name__ = 'this_function_does_not_exist'
        return Dummy()

    def __new__(cls, *args):
        obj = Function.__new__(cls, *args)
        return obj

class ImpFunc(Function):
    # this will rely on _imp_ existing on the instance to compute value
    @property
    def func(self):
        class Dummy:
            __name__ = 'not_in_mpmath_but_has_imp'
        return Dummy()

    def __new__(cls, *args):
        obj = Function.__new__(cls, *args)
        # attach an _imp_ implementation that accepts numeric args
        def _imp_(*args_imp):
            # simply return sum of args as Python float
            return float(sum(args_imp))
        obj._imp_ = _imp_
        return obj

class BadImpFunc(Function):
    # has _imp_ but that raises TypeError to test fallback
    @property
    def func(self):
        class Dummy:
            __name__ = 'bad_imp'
        return Dummy()

    def __new__(cls, *args):
        obj = Function.__new__(cls, *args)
        def _imp_(*args_imp):
            raise TypeError("cannot compute")
        obj._imp_ = _imp_
        return obj

def test_evalf_with_mpmath_function_existing():
    # Use SimpleFunc wrapping sin; pass a numeric SymPy Float
    f = SimpleFunc(SymFloat(0.5))
    # request a precision of 20 bits (mpmath works with bits)
    res = f._eval_evalf(30)
    # result should be an Expr produced by _from_mpmath; check it's close to mpmath.sin
    expected = Expr._from_mpmath(mpmath.sin(mpf('0.5')), 30)
    assert res == expected

def test_evalf_with_translated_mpmath_name(monkeypatch):
    # Ensure translation mapping maps 'E' to 'e' (mpmath.e exists)
    # Create instance with no args: value should be mpmath.e
    t = TranslatedFunc()
    # The MPMATH_TRANSLATIONS mapping is used by the code; ensure mapping contains key
    # If not present in environment, emulate mapping temporarily
    from sympy.utilities.lambdify import MPMATH_TRANSLATIONS
    if 'E' not in MPMATH_TRANSLATIONS:
        monkeypatch.setitem(MPMATH_TRANSLATIONS, 'E', 'e')
    res = t._eval_evalf(30)
    expected = Expr._from_mpmath(mpmath.e, 30)
    assert res == expected

def test_evalf_no_mpmath_but_has_imp():
    # ImpFunc has _imp_ ; args are simple floats
    g = ImpFunc(1.5, 2.5)
    res = g._eval_evalf(30)
    # _imp_ returns sum = 4.0 -> Float with given precision
    exp = Float(4.0, 30)
    assert isinstance(res, Float)
    # numeric equality
    assert float(res) == float(exp)

def test_evalf_no_mpmath_and_imp_fails_returns_none():
    # NoMpmathFunc has no mpmath and no _imp_ -> attempt to get attribute should raise and then return None
    h = NoMpmathFunc(1.0)
    assert h._eval_evalf(20) is None

def test_evalf_imp_raises_and_returns_none():
    b = BadImpFunc(1.0)
    assert b._eval_evalf(20) is None

def test_evalf_argument_to_mpmath_bad_precision(monkeypatch):
    # Create a Function whose arg._to_mpmath produces an mpf with failed precision marker:
    class Arg:
        def _to_mpmath(self, prec):
            # produce an mpf-like object that mpmath.mpf recognizes
            from mpmath import mpf
            # Construct an mpf then tamper its internals to simulate failure.
            x = mpf('0.1')
            # mpf has _mpf_ attribute; set it to a tuple where element 1 == 1 (failure)
            x._mpf_ = (0, 1, 1)  # m[1] == 1 indicates failure per code logic
            return x

    class FuncWithBadArg(Function):
        @property
        def func(self):
            class Dummy:
                __name__ = 'sin'
            return Dummy()
        def __new__(cls, *args):
            return Function.__new__(cls, *args)

    f = FuncWithBadArg(Arg())
    # Should return None because bad arg causes ValueError and thus returns
    assert f._eval_evalf(30) is None

def test_evalf_handles_mpc_results():
    # Use sin with a complex argument so result is mpc; wrap real and imag parts
    z = SymFloat(0.1)  # small real part; we'll create a complex by combining with Symbol? easier to create expression
    class FuncComplex(Function):
        @property
        def func(self):
            class Dummy:
                __name__ = 'sin'
            return Dummy()
        def __new__(cls, *args):
            return Function.__new__(cls, *args)

    # Provide an argument object whose _to_mpmath returns an mpc
    class ArgMpc:
        def _to_mpmath(self, prec):
            return mpc(mpf('0.1'), mpf('0.2'))

    f = FuncComplex(ArgMpc())
    res = f._eval_evalf(30)
    # result should be an Expr converted from mpmath results
    assert res == Expr._from_mpmath(mpmath.sin(mpc(mpf('0.1'), mpf('0.2'))), 30)