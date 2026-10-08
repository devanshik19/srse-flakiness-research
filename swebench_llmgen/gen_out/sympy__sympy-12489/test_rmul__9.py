import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_permutations():
    # simple permutations as lists/tuples
    a = Permutation([1, 0, 2])   # swaps 0 and 1
    b = Permutation([0, 2, 1])   # swaps 1 and 2
    # rmul applies in reverse order: a(b(i))
    res = Permutation.rmul(a, b)
    assert isinstance(res, Permutation)
    assert list(res) == [1, 2, 0]
    # verify element-wise application matches definition
    expected = [a(b(i)) for i in range(3)]
    assert list(res) == expected

def test_rmul_with_mixed_input_types():
    # first arg must be a Permutation; others can be sequences
    a = Permutation([2, 0, 1])
    seq = [0, 2, 1]  # equivalent to Permutation([0,2,1])
    res1 = Permutation.rmul(a, seq)
    res2 = Permutation.rmul(a, Permutation(seq))
    assert list(res1) == list(res2)
    # check composition order: a(seq(i)) should match
    exp = [a(Permutation(seq)(i)) for i in range(3)]
    assert list(res1) == exp

def test_rmul_multiple_operands():
    # chain multiple operands: rmul(a, b, c) = a*(b*c) but applied as a(b(c(i)))
    a = Permutation([1, 0, 2, 3])
    b = Permutation([0, 2, 1, 3])
    c = Permutation([0, 1, 3, 2])
    res = Permutation.rmul(a, b, c)
    # compute by nested application
    nested = [a(b(c(i))) for i in range(4)]
    assert list(res) == nested
    # compare with pairwise rmul calls to ensure associativity of this function's behavior
    res_pair = Permutation.rmul(Permutation.rmul(a, b), c)
    # Note: rmul handles operands in reverse to __mul__, so these may differ;
    # assert that our rmul(a,b,c) equals a*(b*c) as implemented by rmul
    assert list(res) == list(res_pair)

def test_rmul_single_operand_returns_same():
    # If only one argument provided, rmul should return it unchanged
    a = Permutation([1, 0, 2])
    res = Permutation.rmul(a)
    assert res is a  # should be same object reference as returned (as implemented)

def test_rmul_raises_if_first_not_permutation():
    # The docstring states the first item must be a Permutation; if not,
    # behavior in code uses args[0] as rv and then attempts args[i]*rv,
    # which will raise TypeError if rv is not a Permutation. Ensure that happens.
    with pytest.raises(TypeError):
        # first arg is a plain list -> not a Permutation; multiplying by Permutation should fail
        Permutation.rmul([1, 0, 2], Permutation([0, 2, 1]))

def test_rmul_with_identity():
    # identity should behave neutrally: a(id) -> a applied to identity yields a(id(i)) = a(i)
    a = Permutation([2, 0, 1])
    identity = Permutation(range(3))
    res = Permutation.rmul(a, identity)
    assert list(res) == list(a)
    # identity on left with rmul (must be Permutation first arg) yields identity after composition
    res2 = Permutation.rmul(identity, a)
    assert list(res2) == [identity(a(i)) for i in range(3)]