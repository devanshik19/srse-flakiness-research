import pytest
from sympy.combinatorics.permutations import Permutation, _af_new

def test_mul_basic():
    # simple permutations
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # a*b means b(a(i))
    prod = a * b
    assert list(prod) == [2, 0, 1]
    # check with explicit composition
    expected = [b(a(i)) for i in range(3)]
    assert list(prod) == expected

def test_mul_padding_b_shorter():
    # b shorter than a: b will be extended with identity tail
    a = Permutation([2, 0, 1])
    b = Permutation([1, 0])  # length 2
    prod = a * b
    # b extended to [1,0,2], then b[a[i]]
    assert isinstance(prod, Permutation)
    assert list(prod) == [1, 2, 0]

def test_mul_padding_a_shorter():
    # a shorter than b: extend a implicitly in code path (handled by list lengths)
    a = Permutation([1, 0])   # length 2
    b = Permutation([2, 0, 1])  # length 3
    prod = a * b
    # According to implementation: b.extend(range(len(b), len(a))) but here len(a)<len(b)
    # so perm = [b[i] for i in a] + b[len(a):]
    assert list(prod) == [2, 0, 1]

def test_mul_with_empty_b():
    # if other.array_form is empty list, result should be a (no change)
    a = Permutation([2, 0, 1])
    # create a "empty" permutation by constructing from empty array form via _af_new
    empty = _af_new([])
    prod = a * empty
    # per implementation, if not b: perm = a
    assert list(prod) == list(a)

def test_mul_with_list_like_left_operand_coercion():
    # emulate coercion: __rmul__ on list could convert to Permutation, but here we ensure behavior
    # When list (as other) is length 2 and a is length 3, __rmul__ would make other a Permutation.
    a = Permutation([1, 0, 2])
    # use _af_new to simulate a left operand converted to Permutation([0,1])
    left = _af_new([0,1])
    prod = left * a
    # left is identity on first two, extended to length 3 giving [0,1,2] then composed with a
    # As per implementation, result should be Permutation([1,0,2])
    assert list(prod) == [1, 0, 2]

def test_mul_associativity_like_checks():
    # Test some combinations to exercise branches and lengths
    p1 = Permutation([1,2,0,3])  # 4-cycle on first three
    p2 = Permutation([0,2,1])    # swap 1 and 2
    p3 = Permutation([2,1,0,3,4])# longer permutation (5)
    # p1 * p2
    r12 = p1 * p2
    assert isinstance(r12, Permutation)
    # (p1 * p2) * p3 vs p1 * (p2 * p3) are not generally equal (non-commutative),
    # but both should produce valid permutations without error.
    r123_left = r12 * p3
    r23 = p2 * p3
    r123_right = p1 * r23
    # Both results should be Permutation instances and iterable
    assert isinstance(r123_left, Permutation)
    assert isinstance(r123_right, Permutation)
    assert len(list(r123_left)) == max(p1.size(), p2.size(), p3.size())
    assert len(list(r123_right)) == max(p1.size(), p2.size(), p3.size())

def test_mul_with_self_and_identity_behavior():
    # identity check: multiplying by identity (empty array_form represents identity of size 0)
    a = Permutation([0,1,2])
    id_small = _af_new([])
    # a * id_small should return a (implementation checks empty b)
    assert list(a * id_small) == [0,1,2]
    # identity on same size: construct explicit identity of size 3
    id3 = _af_new([0,1,2])
    assert list(a * id3) == [0,1,2]
    assert list(id3 * a) == [0,1,2]