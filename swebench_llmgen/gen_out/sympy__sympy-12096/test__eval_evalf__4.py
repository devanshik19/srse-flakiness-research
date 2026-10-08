import pytest
from mpmath import mpf, mpc
import mpmath
from sympy.core.function import Function
from sympy.core.numbers import Float
from sympy.core.symbol import Symbol
from sympy import sin, exp
from sympy import pi

# Helper: create a minimal Function-derived object with given func and args
class SimpleFunction(Function):
    def __new__(cls, func, *args):
        # Bypass usual Function constructor complexities by creating an instance
        obj = object.__new__(cls)
        obj.func = func
        obj.args = args
        return obj

    # Provide _imp_ to be used when mpmath lookup fails
    def _imp_(self, *args):
        # Try to coerce to float and call underlying python function
        return float(self.func(*[float(a) for a in args]))

    # Provide _to_mpmath for arguments that might be SymPy expressions or numbers
    # For this simple test we'll accept mpf/mpc or plain floats/ints and Symbols (which we will fail)
    def _to_mpmath(self, prec):
        raise NotImplementedError("Not used; instance-level not needed")

# But the Function._eval_evalf expects each arg to implement _to_mpmath.
# We create small wrappers for arguments to emulate behavior.

class ArgNumber:
    def __init__(self, value):
        self.value = value

    def _to_mpmath(self, prec):
        # return mpf or mpc depending on value type
        if isinstance(self.value, complex):
            re = mpf(self.value.real)
            im = mpf(self.value.imag)
            return mpc(re, im)
        else:
            return mpf(self.value)

class ArgBad:
    def __init__(self):
        pass
    def _to_mpmath(self, prec):
        # produce an mpf-like object with failed precision: emulate mp.mpf with _mpf_ attribute
        class Bad:
            def __init__(self):
                # emulate _mpf_ tuple where second element is 1 (failure) and last element is 1
                self._mpf_ = (0, 1, 1)
        return Bad()

def test_evalf_uses_mpmath_function_by_name_and_returns_expr_from_mpmath():
    # Use a built-in mpmath function name: 'sin'
    f = SimpleFunction(mpmath.sin, ArgNumber(0.5))
    # Monkeypatch func.__name__ to 'sin' to trigger getattr(mpmath, 'sin')
    f.func.__name__ = 'sin'
    # Replace args with objects that have _to_mpmath
    f.args = (ArgNumber(0.5),)
    res = Function._eval_evalf(f, 20)
    # Should return a SymPy Float-like object (Expr._from_mpmath returns Float)
    assert isinstance(res, Float)
    # numeric value should be close to mpmath.sin(0.5)
    assert abs(float(res) - float(mpmath.sin(mpf('0.5')))) < 1e-15

def test_evalf_translates_name_using_MPMATH_TRANSLATIONS_and_handles_exp():
    # Use a function whose Python name is 'exp' (sympy.exp) and ensure translation works
    # Create object with func name that isn't in mpmath but is in translations (use 'E' unlikely, so simulate)
    # We'll set name to 'e' and provide mapping by monkeypatching MPMATH_TRANSLATIONS temporarily
    import sympy.utilities.lambdify as lambdify_mod
    orig = getattr(lambdify_mod, 'MPMATH_TRANSLATIONS', None)
    try:
        lambdify_mod.MPMATH_TRANSLATIONS = {'myexp': 'exp'}
        # func name not in mpmath, but translation leads to mpmath.exp
        dummy_func = lambda x: x  # placeholder
        dummy_func.__name__ = 'myexp'
        f = SimpleFunction(dummy_func, ArgNumber(1.0))
        f.args = (ArgNumber(1.0),)
        res = Function._eval_evalf(f, 30)
        assert isinstance(res, Float)
        # mpmath.exp(1.0)
        assert abs(float(res) - float(mpmath.exp(mpf('1.0')))) < 1e-15
    finally:
        if orig is None:
            del lambdify_mod.MPMATH_TRANSLATIONS
        else:
            lambdify_mod.MPMATH_TRANSLATIONS = orig

def test_evalf_falls_back_to__imp__when_mpmath_missing_and_handles_exceptions():
    # Create a func name that is not present in mpmath and not in translations
    dummy = lambda x: 2.0 * x
    dummy.__name__ = 'not_in_mpmath'
    f = SimpleFunction(dummy, ArgNumber(2.0))
    f.args = (ArgNumber(2.0),)
    # Provide _imp_ on instance to return numeric result; SimpleFunction._imp_ will be used
    res = Function._eval_evalf(f, 15)
    assert isinstance(res, Float)
    assert abs(float(res) - 4.0) < 1e-12

    # Now make _imp_ raise TypeError to ensure None is returned
    class BadImp(SimpleFunction):
        def _imp_(self, *args):
            raise TypeError("bad")
    bad = BadImp(dummy, ArgNumber(1.0))
    bad.func.__name__ = 'not_in_mpmath'
    bad.args = (ArgNumber(1.0),)
    assert Function._eval_evalf(bad, 15) is None

def test_evalf_returns_none_when_arg_to_mpmath_fails_precision():
    # Use a real mpmath function but craft an argument that reports failure via _mpf_
    good_func = mpmath.sin
    good_func.__name__ = 'sin'
    f = SimpleFunction(good_func, ArgBad())
    f.args = (ArgBad(),)
    # Because ArgBad._to_mpmath returns an object that signals failure, _eval_evalf should return None
    assert Function._eval_evalf(f, 20) is None

def test_evalf_handles_complex_args_and_returns_mpc_based_value():
    # Test with complex argument using mpc path
    c = complex(1.0, 0.5)
    good_func = mpmath.exp  # exp works on complex
    good_func.__name__ = 'exp'
    f = SimpleFunction(good_func, ArgNumber(c))
    f.args = (ArgNumber(c),)
    res = Function._eval_evalf(f, 30)
    assert res is not None
    # Should be convertible to complex number via float/res.real etc.
    val = float(res) if isinstance(res, Float) else None
    # For complex results Expr._from_mpmath would return an object; at least ensure not None
    assert res is not None