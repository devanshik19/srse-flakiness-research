import pytest
from sympy.combinatorics.permutations import Permutation

def test_rmul_basic_with_permutations():
    # a(b(c(i))) ordering: rmul(a, b) should compute b*a as functions applied right-to-left
    a = Permutation([1, 0, 2])  # transposition (0 1)
    b = Permutation([0, 2, 1])  # transposition (1 2)
    # Using rmul: result should be a(b(i)) for each i (args handled left-to-right but multiplication inside is args[i]*rv)
    res = Permutation.rmul(a, b)
    assert isinstance(res, Permutation)
    assert list(res) == [1, 2, 0]  # a(b(0))=1, a(b(1))=2, a(b(2))=0

    # Compare with explicit composition using call
    expected = Permutation([a(b(i)) for i in range(3)])
    assert list(res) == list(expected)

def test_rmul_with_tuple_and_permutation():
    # First arg must be a Permutation object; others can be sequences (tuples/lists)
    a = Permutation([2, 0, 1])  # cycle (0 2 1)
    tup = (1, 2, 0)             # same as permutation mapping 0->1,1->2,2->0
    res = Permutation.rmul(a, tup)  # should parse tup as Permutation and compute tup*a
    # Verify by explicit application
    assert list(res) == [a(tup[i]) for i in range(3)]

def test_rmul_multiple_arguments_and_associativity_like_order():
    # Check with three permutations: rmul(a, b, c) computes c*b*a (i.e., apply c then b then a)
    a = Permutation([1, 0, 2, 3])   # swap 0<->1
    b = Permutation([0, 2, 1, 3])   # swap 1<->2
    c = Permutation([0, 1, 3, 2])   # swap 2<->3
    res = Permutation.rmul(a, b, c)
    # Apply stepwise: first c, then b, then a: result[i] = a(b(c(i)))
    expected_list = [a(b(c(i))) for i in range(4)]
    assert list(res) == expected_list

def test_rmul_single_argument_returns_same_perm():
    p = Permutation([2, 1, 0])
    res = Permutation.rmul(p)
    assert res is p  # when only one arg, should return that object (no composition done)

def test_rmul_raises_if_first_not_permutation():
    # When the first argument is not a Permutation, composition in rmul expects it to be
    # a Permutation so that subsequent args can be parsed relative to it.
    # We craft a non-Permutation first argument (a plain list) and expect that attempting
    # to call rmul will raise an error when it tries to multiply.
    not_perm = [0, 1, 2]
    with pytest.raises(TypeError):
        # second arg is a Permutation, but the function tries to do args[i]*rv where rv is list
        Permutation.rmul(not_perm, Permutation([0, 1, 2]))

def test_rmul_with_identity_behaviour():
    # Identity permutation should act neutrally depending on position in rmul
    id3 = Permutation(list(range(3)))
    p = Permutation([1, 2, 0])  # 3-cycle
    # rmul(id, p) should be p applied after id: p(id(i)) == p(i)
    assert list(Permutation.rmul(id3, p)) == list(p)
    # rmul(p, id) should be id applied after p: id(p(i)) == p(i)
    assert list(Permutation.rmul(p, id3)) == list(p)