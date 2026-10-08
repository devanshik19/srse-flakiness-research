import pytest
from mpmath import mpf, mpc
import mpmath
from sympy import Float, sin, Function, Symbol
from sympy.core.function import Function as FunctionClass
from sympy import sympify

# We will craft minimal Function subclasses to test _eval_evalf behavior.

class MyFunc(Function):
    """
    A simple Function subclass that uses mpmath's sin by name resolution.
    """
    @classmethod
    def eval(cls, *args):
        return None

class CustomImplFunc(Function):
    """
    A Function subclass that does not have a corresponding mpmath function
    but provides an _imp_ implementation to compute a float result.
    """
    @classmethod
    def eval(cls, *args):
        return None

    def _imp_(self, *args):
        # simply sum numeric args as Python floats
        return float(sum(float(a) for a in args))

class BadArgsFunc(Function):
    """
    A Function subclass that will produce arguments that fail to convert to
    mpmath precision (simulate by returning objects that when _to_mpmath called
    raise ValueError or produce mpf with precision failure).
    """
    @classmethod
    def eval(cls, *args):
        return None

# Helper to create instances without relying on sympy's full parsing
x = Symbol('x')

def test_evalf_uses_mpmath_function_by_name(monkeypatch):
    # Use sympy's sin (which is a Function subclass with .func.__name__ == 'sin')
    # Create sin(0) and evaluate numerically via _eval_evalf
    f = sin(0)
    # call underlying implementation
    res = f._eval_evalf(20)
    assert isinstance(res, Float)
    # sin(0) should be 0.0
    assert abs(float(res)) == 0.0

def test_evalf_uses_mpmath_translations_for_alias(monkeypatch):
    # Create a fake Function subclass whose name is known to MPMATH_TRANSLATIONS
    # We'll use 'acos' which maps to 'acos' in mpmath; construct instance via sin to reuse code
    # Instead, we'll simulate by creating an object whose func.__name__ is 'sin'
    # Create sin(pi/2) and expect 1.0
    from sympy import pi
    f = sin(pi/2)
    res = f._eval_evalf(30)
    assert isinstance(res, Float)
    # numeric close to 1
    assert abs(float(res) - 1.0) < 1e-10

def test_evalf_falls_back_to__imp__when_mpmath_missing(monkeypatch):
    # Make a dummy function name that mpmath doesn't have and map it to our CustomImplFunc
    # We'll create an instance of CustomImplFunc by constructing it via FunctionClass.__new__
    # Build a "function instance" with func attribute whose __name__ is something unknown.
    class DummyFuncObj:
        __name__ = "nonexistent_mpmath_func"

    # Create instance: manually set func and args
    inst = object.__new__(CustomImplFunc)
    inst.func = DummyFuncObj
    inst.args = (1, 2.5)
    # Ensure mpmath doesn't have that name and MPMATH_TRANSLATIONS doesn't map it
    # Call _eval_evalf: should call _imp_ and return Float
    res = CustomImplFunc._eval_evalf(inst, 15)
    assert isinstance(res, Float)
    assert float(res) == pytest.approx(3.5)

def test_evalf_returns_None_on_imp_failure(monkeypatch):
    # Create a class with _imp_ that raises TypeError to trigger return None
    class BadImpFunc(Function):
        def _imp_(self, *args):
            raise TypeError("bad")

    class DummyFuncObj:
        __name__ = "nonexistent2"

    inst = object.__new__(BadImpFunc)
    inst.func = DummyFuncObj
    inst.args = (1,)
    res = BadImpFunc._eval_evalf(inst, 10)
    assert res is None

def test_evalf_returns_None_when_arg_conversion_fails(monkeypatch):
    # Create an instance whose args' _to_mpmath will raise ValueError
    class ArgBad:
        def _to_mpmath(self, prec):
            raise ValueError("cannot convert")

    class DummyFuncObj:
        __name__ = "sin"  # so mpmath lookup succeeds

    inst = object.__new__(MyFunc)
    inst.func = DummyFuncObj
    inst.args = (ArgBad(),)
    res = MyFunc._eval_evalf(inst, 10)
    assert res is None

def test_bad_mpmath_precision_detection(monkeypatch):
    # Simulate _to_mpmath returning mpf/mpc with low precision flags.
    # mpmath.mp.mpf and mpc wrapper objects created from floats should be fine.
    # To simulate failure, craft a fake mpf-like object with _mpf_ attribute set to a tuple
    class FakeMpf:
        def __init__(self, tup):
            self._mpf_ = tup

    class FakeArg:
        def __init__(self, tup):
            self._val = FakeMpf(tup)
        def _to_mpmath(self, prec):
            return self._val

    class DummyFuncObj:
        __name__ = "sin"

    inst = object.__new__(MyFunc)
    inst.func = DummyFuncObj
    # Create a mpf-like tuple where the precision indicator (last element) is 1 meaning failure.
    # For detection: bad checks m[1] != 1 and m[-1] == 1 -> to be bad we need m[1] == 1 or m[-1] !=1
    # To trigger bad returning True, set m[1] == 1 (first condition false) but m[-1] == 1 -> not bad.
    # Instead the code marks bad if m[1] !=1 and m[-1] ==1. So to be bad we set m[1] !=1 and m[-1] ==1.
    tup = (0, 2, 0, 1)  # m[1]=2 !=1 and m[-1]=1 -> bad True
    inst.args = (FakeArg(tup),)
    res = MyFunc._eval_evalf(inst, 20)
    assert res is None

def test_evalf_uses_mpmath_and_converts_back(monkeypatch):
    # Test that when mpmath function returns an mpf or mpc, Expr._from_mpmath is used and returns something
    from sympy.core.expr import Expr as SymExpr
    class DummyFuncObj:
        __name__ = "sin"

    inst = object.__new__(MyFunc)
    inst.func = DummyFuncObj
    # Use a real numeric arg that has _to_mpmath method: use sympy Float
    from sympy import Float as SymFloat
    arg = SymFloat(0.5)
    inst.args = (arg,)
    res = MyFunc._eval_evalf(inst, 30)
    # Should return an Expr (Float)
    assert isinstance(res, sympy.Float) or isinstance(res, Float)