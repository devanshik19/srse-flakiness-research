import pytest
from mpmath import mpf, mpc
import mpmath
from sympy.core.function import Function
from sympy import Float, pi, sin, Symbol
from sympy.utilities.lambdify import MPMATH_TRANSLATIONS

# Create a simple subclass to construct Function instances with desired behavior
class MyFunc(Function):
    @classmethod
    def __new__(cls, *args):
        # Function normally stores .func attribute on the instance where .func is the
        # class itself (or something with __name__). We emulate a simple callable-like
        # descriptor by setting func to a simple object with a __name__.
        obj = Function.__new__(cls)
        obj.args = args
        # set func to the class so .func.__name__ exists
        obj.func = cls
        return obj

# Create a dummy function class with a particular name that maps to mpmath
class my_sin(Function):
    pass

class my_custom(Function):
    pass

def test_eval_evalf_uses_mpmath_function_by_name():
    # Ensure that a function whose name exists in mpmath will be used.
    # Use 'sin' which exists in mpmath. Create a subclass named 'sin'
    # so that .func.__name__ == 'sin'.
    class sin_fn(Function):
        pass
    # instantiate with a numeric argument that has _to_mpmath
    x = Float(0.5)
    inst = sin_fn(x)
    # Call the private evalf method with precision; expect result matches mpmath
    res = inst._eval_evalf(30)
    # Compare numeric values: convert to float with enough precision
    assert isinstance(res, type(Float(1.0)))
    # res is a SymPy Float; compare to mpmath sin
    mp_res = mpmath.sin(x._to_mpmath(35))
    from sympy.core.evalf import mpmathify
    # Ensure result numerical closeness
    assert abs(float(res) - float(mp_res)) < 1e-10

def test_eval_evalf_uses_translations_mapping_when_name_missing(monkeypatch):
    # Create a function whose name is not in mpmath but is in MPMATH_TRANSLATIONS
    class myfunc(Function):
        pass

    # find some mapping key in MPMATH_TRANSLATIONS that maps to an mpmath name
    # e.g., 'acos' should map to 'acos' — but to ensure translation path is used,
    # create a fake mapping entry temporarily.
    monkeypatch.setitem(MPMATH_TRANSLATIONS, 'my_special', 'sin')
    # Create a class with name 'my_special'
    MySpecial = type('my_special', (Function,), {})
    inst = MySpecial(Float(0.2))
    # Now call _eval_evalf; should use mpmath.sin via the translation
    res = inst._eval_evalf(30)
    assert isinstance(res, Float)
    assert abs(float(res) - float(mpmath.sin(inst.args[0]._to_mpmath(35)))) < 1e-10

def test_eval_evalf_falls_back_to__imp_and_handles_exceptions(monkeypatch):
    # If mpmath doesn't have the function and MPMATH_TRANSLATIONS doesn't map it,
    # the code calls self._imp_(*self.args) and wraps in Float. If _imp_ raises,
    # the function should return None.
    class no_mpmath(Function):
        pass

    inst = no_mpmath(Float(1.23))
    # Ensure mpmath has no attribute with this name and no translation
    name = inst.func.__name__
    from sympy.utilities.lambdify import MPMATH_TRANSLATIONS
    # Remove any translation if present
    monkeypatch.setitem(MPMATH_TRANSLATIONS, name, name)  # ensure KeyError path not used
    # Provide an _imp_ that returns a numeric value
    def imp_ok(x):
        return 3.14159
    inst._imp_ = imp_ok
    res = inst._eval_evalf(15)
    assert isinstance(res, Float)
    assert abs(float(res) - 3.14159) < 1e-12

    # Now have _imp_ raise an AttributeError: result should be None
    def imp_bad(x):
        raise AttributeError("bad")
    inst._imp_ = imp_bad
    res2 = inst._eval_evalf(15)
    assert res2 is None

def test_eval_evalf_returns_none_when_argument_cannot_be_converted(monkeypatch):
    # If argument _to_mpmath raises ValueError, _eval_evalf should return None
    class fn(Function):
        pass
    inst = fn(Symbol('x'))  # Symbol does not have _to_mpmath method used here
    # Monkeypatch the argument to have a _to_mpmath that raises ValueError
    class Bad:
        def _to_mpmath(self, prec):
            raise ValueError("cannot convert")
    inst = fn(Bad())
    assert inst._eval_evalf(20) is None

def test_eval_evalf_detects_bad_mpmath_result_structure(monkeypatch):
    # Test the 'bad' inner function branch: create an argument whose _to_mpmath
    # returns an mpf-like object with bad precision marker.
    class fn(Function):
        pass

    class BadMPF:
        # emulate mpf with _mpf_ attribute where second element == 1 to signal failure
        def __init__(self):
            class _M:
                pass
        @property
        def _mpf_(self):
            # Return a tuple where second element equals 1 (bad) and last element equals 1
            return (0, 1, 1)
    class GoodArg:
        def _to_mpmath(self, prec):
            return BadMPF()
    inst = fn(GoodArg())
    # In this case, bad() should detect the failure and _eval_evalf returns None
    assert inst._eval_evalf(30) is None