import pytest
from sympy.combinatorics.permutations import Permutation, _af_new

def test_mul_basic_composition():
    # a(i) = [1,0,2] means 0->1,1->0,2->2
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # product a*b: i -> a(i) then b(...)
    prod = a * b
    assert isinstance(prod, Permutation)
    assert list(prod) == [2, 0, 1]
    # verify definition: b(a(i)) for each i
    assert [b(a(i)) for i in range(3)] == list(prod)

def test_mul_padding_shorter_left_and_right():
    # different lengths: shorter is padded
    a = Permutation([1, 0])        # size 2
    b = Permutation([0, 2, 1])     # size 3
    # b * a: uses __rmul__ coercion so here we test left as Permutation * Permutation
    # According to __mul__ doc: a*b's ith value is b(a(i)).
    res1 = b * a
    # compute expected by padding a to length 3: a extended -> [1,0,2] then b[a[i]]
    assert list(res1) == [1, 2, 0]
    # now a * b: a is shorter; will be padded to match b
    res2 = a * b
    # pad b to length of a? actual behavior: in code a = self.array_form, b = other.array_form,
    # then b.extend(range(len(b), len(a))) -> since len(a)=2,len(b)=3 no extend; perm = [b[i] for i in a] + b[len(a):]
    # So perm = [b[1], b[0]] + b[2:] = [2,0] + [1] = [2,0,1]
    assert list(res2) == [2, 0, 1]

def test_mul_with_empty_other():
    # other.array_form empty -> returns self.array_form
    a = Permutation([2, 0, 1])
    # create a fake "other" permutation with empty array_form by using _af_new on []
    other = _af_new([])
    res = a * other
    assert list(res) == list(a)

def test_mul_with_list_coercion_like_behavior():
    # Permutation supports coercion when other is sequence via __rmul__; emulate left list * Permutation
    # But here we ensure that multiplication of Permutation by a permutation built from a list behaves as docs
    a = Permutation([1, 0, 2])
    left = Permutation([0, 1])  # represents a 2-element permutation
    # left * a: should result in a permutation of length 3 according to docs
    res = left * a
    # compute expected: a = self.array_form -> here left is self, a is other: left.array_form = [0,1], other.array_form=[1,0,2]
    # In __mul__: a = self.array_form (left), b = other.array_form (a). b.extend(range(len(b), len(a))) -> len(b)=3,len(a)=2 no extend
    # perm = [b[i] for i in a] + b[len(a):] => [b[0], b[1]] + b[2:] = [1,0] + [2] = [1,0,2]
    assert list(res) == [1, 0, 2]

def test_mul_nontrivial_padding_behavior():
    # create arrays where other is shorter, forcing extend of b in code path
    # self.array_form longer than other.array_form -> b.extend(range(len(b), len(a)))
    a = Permutation([2, 0, 1, 4, 3])
    # other with length 3; will be extended to length of a
    other = Permutation([1, 2, 0])
    # compute expected manually: b extended -> [1,2,0,3,4]; perm = [b[i] for i in a] + b[len(a):] -> len(a)=5 so b[len(a):]=[]
    expected_b_extended = [1,2,0,3,4]
    expected = [expected_b_extended[i] for i in list(a)]
    res = a * other
    assert list(res) == expected

def test_mul_idempotent_and_associativity_like_checks():
    # check identity behavior and consistent repeated multiplication
    id3 = Permutation(list(range(3)))
    p = Permutation([2, 0, 1])
    assert list(id3 * p) == list(p)
    assert list(p * id3) == list(p)
    # repeated multiplication p*p
    pp = p * p
    # p = (0 2 1) cycle of length 3; p^2 should be inverse (same as p inverse here)
    assert list(pp) == [1, 2, 0]

def test_mul_returns_new_object_not_aliasing_internal_lists():
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    res = a * b
    # mutate original array_forms to ensure result not affected
    a.array_form[:] = [0,1,2]
    b.array_form[:] = [0,1,2]
    assert list(res) == [2, 0, 1]