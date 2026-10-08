import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_permutations():
    # simple example from docstring: a = [1,0,2], b = [0,2,1]
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # rmul(a, b) computes a(b(i)) for each i
    res = Permutation.rmul(a, b)
    assert list(res) == [1, 2, 0]
    # confirm that ordering is reversed compared to a*b
    assert list(a * b) == [2, 0, 1]
    assert list(Permutation.rmul(b, a)) == [2, 0, 1]

def test_rmul_with_mixture_of_types():
    # first argument must be a Permutation; others can be sequences
    a = Permutation([2, 0, 1, 3])  # cycle (0 2 1)
    seq = [1, 3, 0, 2]             # another representation
    # Using a mix: first is Permutation, second is plain sequence
    res = Permutation.rmul(a, seq)
    # compute expected by applying seq then a: a(seq(i))
    expected = [a(Permutation(seq)(i)) for i in range(4)]
    assert list(res) == expected
    # also verify that multiple arguments are composed right-to-left
    b = Permutation([0, 2, 1, 3])
    c = [3, 1, 2, 0]
    res2 = Permutation.rmul(a, b, c)
    # manual composition c -> b -> a
    composed = Permutation(a)  # copy
    composed = Permutation.rmul(composed, b)
    composed = Permutation.rmul(composed, c)
    assert list(res2) == list(composed)

def test_rmul_identity_and_singleton():
    # identity permutation should act as identity on rmul when placed appropriately
    id4 = Permutation(list(range(4)))
    p = Permutation([1, 0, 2, 3])
    assert list(Permutation.rmul(id4, p)) == list(p)  # id then p -> p
    # when only one argument is given, rmul should return it unchanged
    single = Permutation([2, 1, 0])
    assert Permutation.rmul(single) is single

def test_rmul_type_errors_and_edge_cases():
    # If first argument isn't a Permutation, behaviour should be as defined:
    # The implementation assumes args[0] supports multiplication by others.
    # Passing a non-Permutation as first arg should raise when trying to use .__mul__.
    class Weird:
        def __mul__(self, other):
            return "ok"
    w = Weird()
    with pytest.raises(AttributeError):
        # since rmul expects permutation-like, using Weird will likely fail when
        # other * rv is attempted because other is a Permutation and tries to call __mul__
        # resulting in a type mismatch; ensure an exception is raised
        Permutation.rmul(w, Permutation([0, 1, 2]))