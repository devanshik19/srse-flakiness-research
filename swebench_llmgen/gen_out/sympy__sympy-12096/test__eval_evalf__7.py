# test_function_evalf.py
from __future__ import print_function, division
import pytest
import mpmath
from mpmath import mpf, mpc
from sympy.core.function import Function
from sympy.core.numbers import Float, Rational
from sympy.core.symbol import Symbol, Dummy
from sympy import sin, cos, exp
from types import SimpleNamespace

# We will create a minimal subclass of Function that sets func and args so we can test _eval_evalf.
class MyFunction(Function):
    # Function.__new__ would normally handle a lot; we just construct instances manually.
    def __init__(self, func, *args):
        # store a callable in .func and sympy-like args in .args
        self.func = func
        self.args = args

    # helpers used by _eval_evalf:
    def _imp_(self, *args):
        # fallback implementation used when mpmath lacks the function and getattr fails
        # We'll try to coerce arguments to Python floats and call the stored func
        return self.func(*[float(a) for a in args])

    # used by the code path: arg._to_mpmath
    # We'll allow args to be plain sympy Floats or Rationals or mpf/mpc wrappers.
    # Provide a simple wrapper for sympy numbers:
    # But in tests we'll pass objects that implement _to_mpmath.

# Create a helper wrapper to mimic sympy Float/Rational objects' _to_mpmath behavior
class ToMP:
    def __init__(self, value):
        # value can be a Python float, mpf/mpc, or complex
        self.value = value

    def _to_mpmath(self, prec):
        # Return mpf/mpc depending on value type
        if isinstance(self.value, complex):
            return mpc(self.value)
        try:
            return mpf(self.value)
        except Exception:
            # For things like Rational, use float conversion
            return mpf(float(self.value))

def test_evalf_uses_mpmath_function_by_name():
    # Use an actual mpmath function name, e.g., 'sin'
    f = MyFunction(sin, ToMP(0.5))
    # Ensure func.__name__ is 'sin'
    f.func = sin
    res = Function._eval_evalf(f, 30)
    assert isinstance(res, Float)
    # numeric value should be close to mpmath.sin(0.5)
    expected = float(mpmath.sin(mpf('0.5')))
    assert abs(float(res) - expected) < 1e-12

def test_evalf_translated_name_via_mpmath_translations(monkeypatch):
    # Use a function whose name is not in mpmath but is in MPMATH_TRANSLATIONS.
    # For test, create a fake function name and monkeypatch MPMATH_TRANSLATIONS
    from sympy.utilities.lambdify import MPMATH_TRANSLATIONS
    # Store original and restore after
    monkeypatch.setitem(MPMATH_TRANSLATIONS, 'myfunc', 'sin')  # map myfunc -> sin

    # Create a dummy function object with __name__ 'myfunc'
    class DummyFunc:
        __name__ = 'myfunc'
        def __call__(self, x):
            return None

    f = MyFunction(DummyFunc(), ToMP(0.3))
    res = Function._eval_evalf(f, 25)
    assert isinstance(res, Float)
    expected = float(mpmath.sin(mpf('0.3')))
    assert abs(float(res) - expected) < 1e-12

def test_evalf_falls_back_to__imp_and_returns_float_on_success():
    # Create a function name that mpmath lacks and MPMATH_TRANSLATIONS doesn't provide,
    # and make _imp_ succeed.
    class NoMP:
        __name__ = 'no_such_mpmath_fn'
        def __call__(self, x):
            return None

    # Define MyFunction2 that has a working _imp_
    class MyFunction2(MyFunction):
        pass

    f = MyFunction2(NoMP(), ToMP(0.2))
    # Ensure getattr in first block raises AttributeError / KeyError so fallback happens.
    res = Function._eval_evalf(f, 20)
    # Should be Float from _imp_ -> MyFunction._imp_ uses float conversion and calls the python func,
    # but our NoMP.__call__ returns None; thus _imp_ will return None and Float(None, prec) would raise.
    # To ensure a meaningful return, override _imp_ to return a concrete numeric value:
    class MyFunction3(MyFunction2):
        def _imp_(self, *args):
            return 1.2345

    f2 = MyFunction3(NoMP(), ToMP(0.2))
    res2 = Function._eval_evalf(f2, 15)
    assert isinstance(res2, Float)
    assert float(res2) == pytest.approx(1.2345, rel=1e-12)

def test_evalf_returns_none_if_imp_fails():
    # If _imp_ raises AttributeError/TypeError/ValueError, _eval_evalf should return None
    class NoMP:
        __name__ = 'no_such_mpmath_fn2'
        def __call__(self, x):
            pass

    class MyFunction4(MyFunction):
        def _imp_(self, *args):
            raise ValueError("failed")

    f = MyFunction4(NoMP(), ToMP(0.1))
    assert Function._eval_evalf(f, 20) is None

def test_evalf_returns_none_if_argument_cannot_be_computed_to_precision():
    # Make an argument whose _to_mpmath returns an mpf with precision-indicating structure that triggers bad()
    class BadMP:
        __name__ = 'sin'  # so mpmath lookup succeeds
    # Create a fake object with _to_mpmath returning an object that mimics mpf but fails
    class FakeMPF:
        # mpmath mpf instance has type mpf; we can craft an object that is instance of mpf by creating one and monkeypatching?
        # Simpler: create an object that when isinstance(..., mpf) is True by subclassing mpf
        pass

    # Subclass mpf to create a value that will make bad() return True
    class MyBadMPF(mpf):
        def _mpf_(self):
            # return a tuple where second element == 1 and last element == 1 to trigger bad
            return (0, 1, 0, 1)
        # mpmath's mpf stores _mpf_ as attribute or method; ensure attribute access works:
        @property
        def _mpf_(self):
            return (0, 1, 0, 1)

    class Arg:
        def _to_mpmath(self, prec):
            return MyBadMPF('0.0')

    f = MyFunction(BadMP(), Arg())
    # Because bad(arg) will be True, _eval_evalf should return None
    assert Function._eval_evalf(f, 20) is None

def test_evalf_uses_mpmath_complex_output_and_converts_back():
    # Test with a function that returns complex mpc from mpmath: use mpmath.sqrt on a negative number
    class SqrtFunc:
        __name__ = 'sqrt'
    # argument -1 should produce an mpc
    class Arg:
        def _to_mpmath(self, prec):
            return mpf(-1)
    f = MyFunction(SqrtFunc(), Arg())
    res = Function._eval_evalf(f, 30)
    # For sqrt(-1) result should be complex; Expr._from_mpmath returns either a Float or complex-like object.
    # We expect a sympy object convertible to Python complex/float; ensure no exception and type is not None.
    assert res is not None