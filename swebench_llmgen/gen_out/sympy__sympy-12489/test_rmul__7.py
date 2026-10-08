import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_two_permutations():
    # a(i) = [1,0,2] means a: 0->1,1->0,2->2
    a = Permutation([1, 0, 2])
    # b(i) = [0,2,1] means b: 0->0,1->2,2->1
    b = Permutation([0, 2, 1])

    # rmul applies right-to-left: result(i) = a(b(i))
    r = Permutation.rmul(a, b)
    assert isinstance(r, Permutation)
    assert list(r) == [1, 2, 0]
    # verify element-wise application
    assert [a(b(i)) for i in range(3)] == list(r)

def test_rmul_with_tuple_operand():
    # first arg must be a Permutation instance; later args may be sequences
    a = Permutation([2, 0, 1])  # a: 0->2,1->0,2->1
    b_seq = [1, 2, 0]           # b: 0->1,1->2,2->0
    # rmul should accept the tuple/list as a permutation for operands after the first
    r = Permutation.rmul(a, b_seq)
    # expected: a(b(i))
    expected = [a(Permutation(b_seq)(i)) for i in range(3)]
    assert list(r) == expected

def test_rmul_multiple_operands_ordering():
    # Test with three permutations to ensure correct fold order: args[0], args[1], args[2]
    # rmul returns args[2] * (args[1] * args[0])? According to implementation:
    # rv = args[0]; for i in 1..: rv = args[i] * rv  => final is args[n-1]*...*args[0]
    p0 = Permutation([1, 0, 2, 3])  # swaps 0 and 1
    p1 = Permutation([0, 2, 1, 3])  # swaps 1 and 2
    p2 = Permutation([3, 1, 2, 0])  # moves 0->3,3->0

    # Compute expected by explicit composition: apply p0, then p1, then p2: result(i) = p2(p1(p0(i)))
    composed = Permutation.rmul(p0, p1, p2)
    expected = [p2(p1(p0(i))) for i in range(4)]
    assert list(composed) == expected

def test_rmul_identity_and_singleton():
    # Identity permutation should act neutrally when placed as any operand
    id_perm = Permutation(list(range(5)))
    p = Permutation([1, 2, 3, 4, 0])  # cyclic shift

    # rmul(id, p) -> p applied after id => p(id(i)) == p(i)
    assert list(Permutation.rmul(id_perm, p)) == list(p)
    # rmul(p, id) -> id applied after p => id(p(i)) == p(i)
    assert list(Permutation.rmul(p, id_perm)) == list(p)

def test_rmul_returns_first_when_single_arg():
    p = Permutation([1, 0])
    # rmul with single argument should return that argument unchanged
    r = Permutation.rmul(p)
    assert r is p  # implementation returns args[0] (same object)

def test_rmul_raises_if_first_not_permutation():
    # The implementation assumes first arg is a Permutation. If it's not, subsequent
    # operations will try to use * operator and may raise. We test that a non-Permutation
    # first argument leads to appropriate TypeError when multiplication is attempted.
    not_perm = [1, 0, 2]
    p = Permutation([0, 2, 1])
    with pytest.raises(TypeError):
        # rmul will try to do p0 = args[0]; then args[1]*p0 -> Permutation * list -> TypeError
        Permutation.rmul(not_perm, p)

def test_rmul_with_more_types_and_sizes():
    # Ensure rmul handles permutations with different internal sizes by relying on
    # Permutation multiplication behavior (it will extend as necessary)
    a = Permutation([1, 0])         # acts on 0..1
    b = Permutation([0, 2, 1, 3])   # acts on 0..3
    # rmul(a, b) -> b * a
    r = Permutation.rmul(a, b)
    # compute expected via explicit composition wrapped to Permutation instances
    expected = [b(a(i)) for i in range(max(a.size, b.size))]
    assert list(r) == expected