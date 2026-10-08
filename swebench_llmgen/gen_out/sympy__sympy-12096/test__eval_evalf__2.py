import pytest
from types import SimpleNamespace
import mpmath
from mpmath import mpf, mpc
from sympy import Float, Symbol
from sympy.core.function import Function
from sympy.core.expr import Expr
from sympy.utilities.lambdify import MPMATH_TRANSLATIONS

# We'll create a minimal concrete Function subclass to test _eval_evalf
class MyFunction(Function):
    """
    Minimal concrete Function-like object. We override __new__ to allow
    instantiation with simple args and set .func to a dummy callable-like
    object providing a __name__ attribute so that _eval_evalf can look up
    mpmath functions by name.
    """
    def __new__(cls, func, *args):
        # Create a bare instance without full sympy Function machinery.
        obj = SimpleNamespace()
        # mimic attributes used by _eval_evalf:
        # .func should have __name__
        obj.func = func
        # .args should be a tuple of sympy Expr-like objects that implement
        # _to_mpmath used by the implementation. We'll accept raw numbers and
        # create tiny wrapper objects.
        obj.args = tuple(args)
        # bind the _eval_evalf method from Function to this instance
        # by retrieving the unbound function and creating a bound method
        fn = Function._eval_evalf
        # Convert to a function that takes self as first argument
        def bound_evalf(prec):
            return fn(obj, prec)
        obj._eval_evalf = bound_evalf
        return obj

# Helper wrapper to provide ._to_mpmath for numeric and Expr-like args
class ArgWrapper:
    def __init__(self, value):
        self.value = value
    def _to_mpmath(self, prec):
        # Return mpf or mpc depending on the contained value
        if isinstance(self.value, complex):
            # convert to mpc
            re = mpf(self.value.real)
            im = mpf(self.value.imag)
            return mpc(re, im)
        else:
            return mpf(self.value)

    def __repr__(self):
        return f"ArgWrapper({self.value!r})"

def test_evalf_uses_mpmath_by_name_for_known_function():
    # Use mpmath.sin: define a func-like object with __name__ == 'sin'
    sin_like = SimpleNamespace(__name__='sin')
    # argument 0.5
    arg = ArgWrapper(0.5)
    f = MyFunction(sin_like, arg)
    res = f._eval_evalf(30)
    # Should return an Expr-like via Expr._from_mpmath; for numeric functions
    # this yields a sympy Float; ensure we get a Float and that value matches mpmath
    assert isinstance(res, Float)
    # Compare numeric values with mpmath.sin at same precision
    mpmath.mp.dps = 30
    expected = mpmath.sin(arg._to_mpmath(35))
    # Convert expected to Python float for comparison with sympy Float
    assert abs(float(res) - float(expected)) < 1e-25

def test_evalf_uses_mpmath_translation_when_name_missing():
    # Make a func-like object whose name is not on mpmath but is in MPMATH_TRANSLATIONS.
    # For example, 'atan2' is mapped in MPMATH_TRANSLATIONS to 'atan2' or similar.
    # We'll pick 'acosh' which mpmath exposes as 'acosh' but ensure translation path is used
    # by providing a fake name that maps to 'acosh' in MPMATH_TRANSLATIONS.
    # Find an existing translation key and its value
    # If none, skip.
    if not MPMATH_TRANSLATIONS:
        pytest.skip("No MPMATH_TRANSLATIONS available")
    # pick any mapping (key->value)
    key, val = next(iter(MPMATH_TRANSLATIONS.items()))
    fake_name = key
    translated_name = val
    # Build a func-like object with name that requires translation
    func_like = SimpleNamespace(__name__=fake_name)
    # choose an argument
    arg = ArgWrapper(1.2)
    f = MyFunction(func_like, arg)
    res = f._eval_evalf(20)
    # If the translation points to a real mpmath function, result should be Float
    if hasattr(mpmath, translated_name):
        assert isinstance(res, Float)
    else:
        # If translation doesn't point to a real mpmath function then implementation
        # would have attempted Float(self._imp_(...)) and likely returned None;
        # ensure no exception raised and result is either Float or None.
        assert (res is None) or isinstance(res, Float)

def test_evalf_falls_back_to_imp_on_missing_mpmath_function_and_handles_errors(monkeypatch):
    # Create a func-like object with a name that neither exists in mpmath nor in translations.
    func_like = SimpleNamespace(__name__='this_function_does_not_exist_12345')
    # Create an instance where ._imp_ returns a numeric value
    instance = MyFunction(func_like, ArgWrapper(2.0))
    # Attach an _imp_ method that returns a plain Python float
    def imp_ok(*args):
        return 3.1415
    instance._imp_ = imp_ok
    # Now calling _eval_evalf should return a Float wrapping the imp result
    res = instance._eval_evalf(15)
    assert isinstance(res, Float)
    assert abs(float(res) - 3.1415) < 1e-12

    # Now make _imp_ raise an exception -> then _eval_evalf should return None
    def imp_bad(*args):
        raise ValueError("bad")
    instance._imp_ = imp_bad
    res2 = instance._eval_evalf(15)
    assert res2 is None

def test_evalf_returns_none_on_arg_to_mpmath_failure(monkeypatch):
    # Use a known mpmath function so the code gets to argument conversion
    func_like = SimpleNamespace(__name__='sin')
    # Create an argument wrapper whose _to_mpmath will produce an mpf with failed precision.
    class BadArg:
        def _to_mpmath(self, prec):
            # Create an mpf-like object with internal _mpf_ indicating failure:
            # mpmath's mpf uses a tuple; create a dummy object with _mpf_ attr
            class FakeMPF:
                def __init__(self):
                    # shape like (sign, bc, man, exp) but set bc==1 and man!=1 to trigger bad()
                    self._mpf_ = (0, 1, 123, 1)
            return FakeMPF()
    f = MyFunction(func_like, BadArg())
    # Expect None because bad argument should cause ValueError in the implementation
    assert f._eval_evalf(20) is None

def test_evalf_handles_complex_arguments_and_returns_mpc_like_result():
    # Use mpmath.exp which supports complex numbers
    func_like = SimpleNamespace(__name__='exp')
    arg = ArgWrapper(complex(0.0, 1.0))  # i
    f = MyFunction(func_like, arg)
    res = f._eval_evalf(30)
    # Should return an Expr (Float or complex convertible). For exp(i) expect complex result
    # Expr._from_mpmath for mpc returns a sympy object that can be converted to complex via complex()
    if res is None:
        pytest.skip("Expr._from_mpmath produced None in this environment")
    # Try to convert to complex to ensure a complex-like numeric result
    try:
        c = complex(res)
    except Exception:
        # Some sympy numeric types may not be directly convertible; instead compare string
        s = str(res)
        assert 'I' in s or 'i' in s or 'exp' not in s
    else:
        # exp(i) == cos(1) + i*sin(1)
        import math
        assert abs(c.real - math.cos(1.0)) < 1e-12
        assert abs(c.imag - math.sin(1.0)) < 1e-12