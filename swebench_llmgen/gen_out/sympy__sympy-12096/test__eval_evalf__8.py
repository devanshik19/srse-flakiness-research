import pytest
from types import SimpleNamespace
import mpmath
from mpmath import mpf, mpc
from sympy.core.function import Function
from sympy.core.numbers import Float
from sympy import Basic

# We'll create a minimal subclass of Function to set func and args
class DummyFunction(Function):
    """
    Minimal concrete Function-like object for testing _eval_evalf.
    We'll bypass full sympy construction and just set attributes used by _eval_evalf.
    """

    def __init__(self, func, args):
        # store a .func that has a __name__, and .args sequence of objects
        self.func = func
        self.args = tuple(args)

    # The real Function._eval_evalf expects ._imp_ and ._to_mpmath on args sometimes.
    # Provide a simple passthrough implementation if needed by tests.
    def _imp_(self, *args):
        # pretend the imperative (numeric) implementation adds arguments as floats
        return float(sum(args))

# Helper fake argument classes to emulate _to_mpmath behavior
class GoodArg:
    def __init__(self, value):
        self.value = value
    def _to_mpmath(self, prec):
        # return an mpf or mpc consistent with mpmath
        if isinstance(self.value, complex):
            re = mpf(self.value.real)
            im = mpf(self.value.imag)
            return mpc(re, im)
        return mpf(self.value)

class BadArg:
    def _to_mpmath(self, prec):
        # intentionally create an mpf with precision-failure pattern:
        # create a custom object that mimics mpf but has _mpf_ attribute with bad flags.
        class FakeMPF:
            def __init__(self):
                # structure similar to mpf._mpf_: (sign, bc, ... , bc)
                # set second element to 1 to trigger the "bad" detection in bad()
                self._mpf_ = (0, 1, 0)
        return FakeMPF()

def test_evalf_uses_mpmath_function_name_direct():
    # Use mpmath 'sin' directly
    func = SimpleNamespace(__name__='sin')
    # argument that provides _to_mpmath
    a = GoodArg(0.5)
    f = DummyFunction(func, [a])
    res = f._eval_evalf(20)
    # Expect an Expr-like object returned from Expr._from_mpmath;
    # _eval_evalf returns SymPy Expr (Float/complex) via that pathway.
    # Here ensure we got something (not None) and it is Basic or Float-ish
    assert res is not None
    # numeric value should be close to mpmath.sin(0.5)
    mpres = mpmath.sin(a._to_mpmath(25))
    # Convert returned SymPy object to mpf via its _to_mpmath or string compare
    # Many SymPy Expr types implement _to_mpmath; try to use it if present
    if hasattr(res, '_to_mpmath'):
        val = res._to_mpmath(20)
        # compare real parts (works for mpf/mpc)
        if isinstance(val, mpmath.mpc):
            assert abs(val.real - mpres.real) < mpf('1e-10')
            assert abs(val.imag - mpres.imag) < mpf('1e-10')
        else:
            assert abs(val - mpres) < mpf('1e-10')
    else:
        # fallback: ensure it's a Float or Basic
        assert isinstance(res, Basic) or isinstance(res, Float)

def test_evalf_falls_back_to_translations():
    # Use a function name not in mpmath but present in MPMATH_TRANSLATIONS
    # e.g., 'log10' is translated to 'log10' in some mappings; pick 'acos' (exists)
    # To force translation path, give a fake name not in mpmath module but present
    from sympy.utilities.lambdify import MPMATH_TRANSLATIONS
    # pick a real mapped name from translations; if none, skip this test
    # find a mapping whose value exists in mpmath
    mapping_item = None
    for k, v in MPMATH_TRANSLATIONS.items():
        if hasattr(mpmath, v):
            mapping_item = (k, v)
            break
    if mapping_item is None:
        pytest.skip("No suitable MPMATH_TRANSLATIONS entry found")
    fake_name, real_name = mapping_item
    func = SimpleNamespace(__name__=fake_name)
    a = GoodArg(0.3)
    f = DummyFunction(func, [a])
    res = f._eval_evalf(15)
    assert res is not None

def test_evalf_uses__imp__when_no_mpmath_and_imp_ok():
    # Create a func name that is not in mpmath and not in translations to trigger AttributeError/KeyError
    func = SimpleNamespace(__name__='this_function_does_not_exist_12345')
    # Provide args that will not be converted to mpmath (so code will try _imp_)
    # The DummyFunction._imp_ will sum the args; provide simple numbers
    f = DummyFunction(func, [1, 2, 3])
    # Monkeypatch args to be plain numbers so _to_mpmath code path is not needed
    # But since the mpmath branch will raise and then the code tries self._imp_(*self.args)
    res = f._eval_evalf(10)
    # Expect a Float result representing sum 6.0
    assert isinstance(res, Float)
    assert abs(float(res) - 6.0) < 1e-12

def test_evalf_returns_None_when_args_fail_to_mpmath():
    # Use a real mpmath function name but provide an argument whose _to_mpmath indicates failure
    func = SimpleNamespace(__name__='sin')
    bad = BadArg()
    f = DummyFunction(func, [bad])
    res = f._eval_evalf(20)
    assert res is None

def test_evalf_handles_mpc_arguments_and_complex_results():
    # Use 'exp' which accepts complex numbers
    func = SimpleNamespace(__name__='exp')
    a = GoodArg(complex(1, 1))
    f = DummyFunction(func, [a])
    res = f._eval_evalf(25)
    assert res is not None
    if hasattr(res, '_to_mpmath'):
        val = res._to_mpmath(25)
        mpres = mpmath.exp(a._to_mpmath(30))
        if isinstance(val, mpmath.mpc):
            assert abs(val.real - mpres.real) < mpf('1e-8')
            assert abs(val.imag - mpres.imag) < mpf('1e-8')
        else:
            # If returned as mpf (unlikely), compare real part
            assert abs(val - mpres.real) < mpf('1e-8')