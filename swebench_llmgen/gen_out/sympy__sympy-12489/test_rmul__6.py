import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_permutations():
    # simple permutations as lists
    a = Permutation([1, 0, 2])  # swap 0 and 1
    b = Permutation([0, 2, 1])  # swap 1 and 2
    # rmul processes right-to-left: result(i) = a(b(i))
    r = Permutation.rmul(a, b)
    assert isinstance(r, Permutation)
    assert list(r) == [1, 2, 0]
    # verify element-wise application: a(b(i))
    assert [a(b(i)) for i in range(3)] == [1, 2, 0]

def test_rmul_with_tuple_and_permutation():
    # first argument must be a Permutation object; subsequent args may be tuples
    a = Permutation([2, 0, 1])  # cycle (0 2 1)
    tup = (1, 2, 0)             # tuple form same as Permutation([1,2,0])
    # mixing types: first is Permutation, second is tuple
    r = Permutation.rmul(a, tup)
    # rmul does tup * a (i.e., a applied after parsing tup), since implementation iterates args[i]*rv
    # but args[0] is rv, then rv = args[1]*rv => tup * a
    # convert tup to Permutation and compute expected
    expected = Permutation(tup) * a
    assert list(r) == list(expected)

def test_rmul_multiple_operands_order():
    # check associative chain / order: rmul(a,b,c) -> c*b*a (applies a after b after c? check implementation)
    # Implementation sets rv=args[0]; for i in 1..: rv = args[i]*rv
    # So rmul(a,b,c) returns c*b*a (function value = a(b(c(i))) per docstring)
    a = Permutation([1, 0, 2, 3])
    b = Permutation([0, 2, 1, 3])
    c = Permutation([0, 1, 3, 2])
    r = Permutation.rmul(a, b, c)
    # compute expected by explicit composition a(b(c(i)))
    expected_list = [a(b(c(i))) for i in range(4)]
    assert list(r) == expected_list

def test_rmul_single_argument_returns_itself():
    # single argument should be returned unchanged
    a = Permutation([2, 1, 0])
    r = Permutation.rmul(a)
    assert r is a  # implementation returns args[0] directly

def test_rmul_error_if_first_not_permutation():
    # If first argument is not a Permutation, subsequent items won't be parsed;
    # the implementation expects that the first is a Permutation for safe behavior.
    # We ensure that passing a non-Permutation first still raises when trying to multiply.
    with pytest.raises(TypeError):
        # e.g., first arg is a tuple; then args[i] * rv will attempt Permutation.__mul__ with rv tuple
        Permutation.rmul((1, 0), Permutation([0, 1]))

def test_rmul_with_identity_and_noop():
    # identity composed should leave permutation unchanged
    a = Permutation([1, 0, 2])
    identity = Permutation([0, 1, 2])
    r = Permutation.rmul(a, identity)
    # returns identity * a -> a (since rv starts as a, then identity * a)
    assert list(r) == list(Permutation([0,1,2]) * a)

def test_rmul_commutativity_not_assumed():
    # ensure rmul order differs from __mul__
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    rmul_res = Permutation.rmul(a, b)  # a(b(i))
    mul_res = a * b                    # a*b is different (left then right depending on implementation)
    assert list(rmul_res) != list(mul_res)