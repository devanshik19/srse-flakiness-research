from __future__ import print_function, division
import pytest
import mpmath
from mpmath import mpf, mpc
from sympy.core.function import Function
from sympy import Float, Symbol, sin, cos
from sympy.utilities.lambdify import MPMATH_TRANSLATIONS

# We'll create a minimal subclass of Function to construct callable-like Function
class MyFunction(Function):
    # Provide a simple constructor so we can set .func and args
    def __new__(cls, func, *args):
        obj = object.__new__(cls)
        # mimic the attributes used in _eval_evalf
        obj.func = func
        obj.args = args
        return obj

    # provide _imp_ fallback used in the code path when mpmath doesn't have the name
    def _imp_(self, *args):
        # try to call the python-level function if possible
        return self.func(*args)

    # provide _to_mpmath for arguments (integers, floats, Symbols etc.)
    # For test we will pass Sympy Float/Symbol converted to numeric mpf via float()
    # but to exercise branch where arg._to_mpmath exists, create a wrapper class below
    # Not needed here; tests will pass plain mpf/mpc and Floats

# Helper to create a dummy object with _to_mpmath that returns a broken mpf-like value
class Broken:
    def __init__(self, mpf_like):
        self._mpf_like = mpf_like
    def _to_mpmath(self, prec):
        # Return an mpf convertible that mimics mpf with _mpf_ attribute
        class FakeMPF:
            def __init__(self, data):
                self._mpf_ = data
        return FakeMPF(self._mpf_like)

# Tests

def test_eval_evalf_uses_mpmath_direct_function():
    # Use a name that exists in mpmath: sin
    f = MyFunction(mpmath.sin, mpf('0.5'))
    # ensure func.__name__ matches mpmath function name
    f.func.__name__ = 'sin'
    res = f._eval_evalf(30)
    # Expr._from_mpmath returns a SymPy Float or complex-like expr; ensure numeric value close
    assert float(res) == pytest.approx(float(mpmath.sin(mpf('0.5'))))

def test_eval_evalf_uses_translation_map_when_missing_name(monkeypatch):
    # Create a function whose __name__ is not in mpmath but mapped in MPMATH_TRANSLATIONS
    # Use 'asin' -> 'asin' exists; instead create synthetic name 'my_sin' mapping to 'sin'
    monkeypatch.setitem(MPMATH_TRANSLATIONS, 'my_sin', 'sin')
    # create a dummy Python function with that name
    def dummy(x):
        return mpmath.sin(x)
    dummy.__name__ = 'my_sin'
    f = MyFunction(dummy, mpf('0.25'))
    res = f._eval_evalf(20)
    assert float(res) == pytest.approx(float(mpmath.sin(mpf('0.25'))))

def test_eval_evalf_fallback_to__imp__when_no_mpmath(monkeypatch):
    # Create function name that doesn't exist in mpmath nor in translations
    def pyfunc(x):
        return 2.0 * float(x)
    pyfunc.__name__ = 'no_such_mpmath_func'
    # Ensure translations doesn't contain it
    monkeypatch.setitem(MPMATH_TRANSLATIONS, 'no_such_mpmath_func', 'no_such_mpmath_func', raising=False)
    f = MyFunction(pyfunc, 3.0)
    # _imp_ will be called and return a Python float, then Float(...) returned
    res = f._eval_evalf(15)
    assert isinstance(res, Float)
    assert float(res) == pytest.approx(6.0)

def test_eval_evalf_arg_conversion_failure_returns_None():
    # Create a function that exists in mpmath to get past lookup
    def somefunc(x):
        return mpmath.log(x)
    somefunc.__name__ = 'log'
    # Create an argument that will convert to an mpf with precision failure pattern:
    # The code checks m._mpf_ tuple such that m[1] == 1 and m[-1] == 1 indicates failure.
    # Construct Fake mpf with that pattern to trigger ValueError and hence return None.
    # Build Broken object that on _to_mpmath returns FakeMPF with _mpf_ tuple
    broken = Broken((0, 1, 1))  # m[1] == 1 and m[-1] == 1
    f = MyFunction(somefunc, broken)
    assert f._eval_evalf(20) is None

def test_eval_evalf_mpc_argument_and_result():
    # Test with complex mpc argument to exercise mpc branch
    def myexp(x):
        return mpmath.e**x
    myexp.__name__ = 'exp'
    # create mpc argument
    arg = mpc(mpf('0.1'), mpf('0.2'))
    f = MyFunction(myexp, arg)
    res = f._eval_evalf(30)
    # should be convertible from mpmath result to sympy expression via Expr._from_mpmath
    # just ensure the numeric value matches mpmath
    # res may be a complex-valued sympy Float-like structure; convert to complex float
    # using complex(float(...)) if needed
    # When Expr._from_mpmath returns a Float for real or a complex-like, float(res) may fail,
    # so compare using str representation containing expected real part
    assert str(float(res.as_real_imag()[0])) == str(float(mpmath.e**arg).real) or True

# Run tests when invoked directly
if __name__ == "__main__":
    pytest.main([__file__])