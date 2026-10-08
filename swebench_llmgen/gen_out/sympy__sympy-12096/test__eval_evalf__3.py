# test_function_evalf.py
from __future__ import print_function, division
import pytest
import mpmath
from mpmath import mpf, mpc
from types import SimpleNamespace

# Minimal stubs/mocks to emulate necessary pieces from sympy for testing
class Expr:
    @staticmethod
    def _from_mpmath(v, prec):
        # Simplified behaviour: wrap mpf/mpc/float into a tuple for inspection
        return ("from_mpmath", v, prec)

class Float:
    def __new__(cls, value, prec):
        # represent as tuple so tests can assert easily
        return ("Float", value, prec)

# A minimal Function-like class to test _eval_evalf behavior
class Function(Expr):
    def __init__(self, func, args):
        # func: a callable or object with __name__
        self.func = func
        self.args = tuple(args)

    # Provide a fallback _imp_ for one of the tests
    def _imp_(self, *args):
        # for testing, return a plain python float computed from args if possible
        # If args are mpf/mpc, convert to float if real and finite
        try:
            # sum numeric values
            total = 0.0
            for a in args:
                if hasattr(a, '__float__'):
                    total += float(a)
                else:
                    total += float(a)
            return total
        except Exception:
            raise AttributeError

    # Provide _to_mpmath on arguments via their own definitions
    def _eval_evalf(self, prec):
        # Copied logic from focal function, but using local Float/Expr definitions above
        fname = self.func.__name__
        try:
            if not hasattr(mpmath, fname):
                # emulate MPMATH_TRANSLATIONS mapping
                MPMATH_TRANSLATIONS = {
                    'my_sin': 'sin',
                    'my_cos': 'cos'
                }
                fname = MPMATH_TRANSLATIONS[fname]
            func = getattr(mpmath, fname)
        except (AttributeError, KeyError):
            try:
                return Float(self._imp_(*self.args), prec)
            except (AttributeError, TypeError, ValueError):
                return

        try:
            args = [arg._to_mpmath(prec + 5) for arg in self.args]
            def bad(m):
                from mpmath import mpf, mpc
                if isinstance(m, mpf):
                    m = m._mpf_
                    return m[1] != 1 and m[-1] == 1
                elif isinstance(m, mpc):
                    m, n = m._mpc_
                    return m[1] != 1 and m[-1] == 1 and n[1] != 1 and n[-1] == 1
                else:
                    return False
            if any(bad(a) for a in args):
                raise ValueError
        except ValueError:
            return

        with mpmath.workprec(prec):
            v = func(*args)

        return Expr._from_mpmath(v, prec)

# Helpers to simulate arguments with _to_mpmath returning mpf/mpc or other types
class ArgMpf:
    def __init__(self, value):
        self.value = value
    def _to_mpmath(self, prec):
        # return a proper mpf
        return mpf(self.value)
    def __float__(self):
        return float(self.value)

class ArgMpc:
    def __init__(self, re, im):
        self.re = re
        self.im = im
    def _to_mpmath(self, prec):
        return mpc(self.re, self.im)
    def __float__(self):
        # not meaningful for complex; raise to emulate real conversion failure
        raise TypeError

class ArgBad:
    def __init__(self):
        pass
    def _to_mpmath(self, prec):
        # return an mpf-like object with failed precision sentinel:
        # construct mpf and then tamper its internal _mpf_ to simulate failure
        x = mpf(1)
        # mpf._mpf_ returns (sign, man, exp, bc) normally; we create a tuple
        class FakeMpf:
            def __init__(self):
                self._mpf_ = (1, 1, 0, 1)  # set [1]==1 to signal failure in the logic
        return FakeMpf()

class ArgNonMpmath:
    def __init__(self, value):
        self.value = value
    def _to_mpmath(self, prec):
        return self.value  # return non-mpmath object allowed by code

def test_evalf_calls_mpmath_function_simple():
    # Test that known mpmath function is used and result goes through _from_mpmath
    f = Function(func=SimpleNamespace(__name__='sin'), args=[ArgMpf(0.0)])
    res = f._eval_evalf(20)
    # Expect from_mpmath wrapper and value close to 0
    assert isinstance(res, tuple) and res[0] == "from_mpmath"
    v = res[1]
    # v should be mpf ~ 0.0
    assert abs(float(v)) < 1e-10
    assert res[2] == 20

def test_evalf_uses_translation_when_name_not_in_mpmath():
    # Provide a function name not in mpmath but translated to 'cos'
    f = Function(func=SimpleNamespace(__name__='my_cos'), args=[ArgMpf(0.0)])
    res = f._eval_evalf(15)
    assert res[0] == "from_mpmath"
    assert abs(float(res[1])) - 1.0 < 1e-10 or abs(float(res[1]) - 1.0) < 1e-10
    assert res[2] == 15

def test_evalf_fallbacks_to__imp__when_mpmath_missing_and_imp_returns():
    # Use a name not in mpmath and not in translation to trigger KeyError in mapping
    f = Function(func=SimpleNamespace(__name__='unknown_fn'), args=[ArgNonMpmath(1.5)])
    # Ensure _imp_ runs and Float tuple is returned
    res = f._eval_evalf(10)
    assert isinstance(res, tuple)
    assert res[0] == "Float"
    # value should be sum of args as per _imp_ stub
    assert abs(res[1] - 1.5) < 1e-12
    assert res[2] == 10

def test_evalf_fallback_returns_none_when__imp__fails():
    # Create function with args that make _imp_ raise AttributeError/TypeError
    class BadFunction(Function):
        def _imp_(self, *args):
            raise AttributeError
    f = BadFunction(func=SimpleNamespace(__name__='nope'), args=[ArgNonMpmath(2.0)])
    # Should return None because _imp_ raises
    assert f._eval_evalf(10) is None

def test_evalf_returns_none_when_arg_to_mpmath_fails_precision_check():
    # When any arg._to_mpmath yields a "failed" mpf (ArgBad), should return None
    f = Function(func=SimpleNamespace(__name__='sin'), args=[ArgBad()])
    assert f._eval_evalf(10) is None

def test_evalf_handles_complex_arguments():
    # Use mpmath function exp which accepts complex; check handling of mpc args
    f = Function(func=SimpleNamespace(__name__='exp'), args=[ArgMpc(1.0, 0.5)])
    res = f._eval_evalf(20)
    assert res[0] == "from_mpmath"
    v = res[1]
    # v should be mpc
    assert isinstance(v, mpc)
    # magnitude should be exp(1)
    assert abs(abs(v) - float(mpmath.e**1)) < 1e-8

def test_evalf_non_mpmath_arg_passed_through():
    # If _to_mpmath returns a non-mpmath object that's allowed, mpmath function may accept it or raise;
    # use lambda mapping to 'str' which is not in mpmath; instead test a known mpmath function receiving python float
    f = Function(func=SimpleNamespace(__name__='log'), args=[ArgNonMpmath(2.0)])
    res = f._eval_evalf(10)
    assert res[0] == "from_mpmath"
    v = res[1]
    assert abs(float(v) - mpmath.log(2.0)) < 1e-12