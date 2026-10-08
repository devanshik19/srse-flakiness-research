import pytest
from sympy.combinatorics.permutations import Permutation, _af_new, _af_rmul

def test_mul_basic_composition():
    # a(i) then b(...) so (a*b)(i) == b(a(i))
    a = Permutation([1, 0, 2])  # swaps 0 and 1
    b = Permutation([0, 2, 1])  # swaps 1 and 2
    prod = a * b
    # check list form equals applying a then b
    expected = [b(a(i)) for i in range(3)]
    assert list(prod) == expected
    # also ensure underlying array length and type
    assert isinstance(prod, Permutation)
    assert prod.size() == 3

def test_mul_padding_shorter_left_and_right():
    # left shorter than right: Permutation([1,0]) * b
    small = Permutation([1, 0])
    big = Permutation([0, 2, 1])
    # small * big: shorter (2) padded to 3 before composing: result should be big after mapping
    res1 = small * big
    # compute expected via arrays with padding
    a = list(small)
    b = list(big)
    a.extend(range(len(a), len(b)))
    expected1 = [b[i] for i in a] + b[len(a):]
    assert list(res1) == expected1

    # right shorter: big * small
    res2 = big * small
    a = list(big)
    b = list(small)
    b.extend(range(len(b), len(a)))
    expected2 = [b[i] for i in a] + b[len(a):]
    assert list(res2) == expected2

def test_mul_with_empty_other():
    # other.array_form empty should return self.array_form
    a = Permutation([2, 0, 1])
    # create a Permutation with empty array_form using _af_new([])
    empty = _af_new([])
    res = a * empty
    # per implementation, if not b: perm = a
    assert list(res) == list(a)

def test_mul_coercion_like_list_on_left():
    # The __rmul__ of Permutation allows lists on left; ensure multiplication uses other's array_form
    a = Permutation([1, 0, 2])
    # list as left operand: [0,1] should be converted by __rmul__ to a Permutation of size 2 (identity),
    # then coerced/padded when composing with a on right. Use Python's mul which will call __rmul__.
    left = [0, 1]
    prod = left * a  # calls Permutation.__rmul__ internally
    # For left identity of size 2, when composed with a of size 3 the result should be size 3 and equal to a
    assert isinstance(prod, Permutation)
    assert list(prod) == list(a)

    # If left is nested list indicating a cycle-like coercion: [[0,1]]*a should swap first two positions only
    left_cycle = [[0, 1]]
    prod2 = left_cycle * a
    # [[0,1]] coerces to permutation that swaps 0 and 1 but leaves others fixed -> expected [0,1,2] then applied by a
    # So compute expected by using __rmul__ behavior: build permutation from left_cycle then compose
    # We can simulate by creating a Permutation from the flattened cycle (as __rmul__ would)
    from sympy.combinatorics.permutations import Permutation as P
    coerced = P([0,1,2])  # swapping first two elements of [0,1,2] yields identity on positions beyond 1
    # Actually [[0,1]] should produce a permutation exchanging 0 and 1: that's Permutation([1,0,2])
    coerced = P([1,0,2])
    expected = coerced * a
    assert list(prod2) == list(expected)

def test_mul_commutation_with_af_rmul_difference():
    # Demonstrate that __mul__ composes in reverse order compared to _af_rmul
    a = Permutation([1, 2, 0])
    b = Permutation([2, 0, 1])
    al = list(a)
    bl = list(b)
    # _af_rmul does a right multiplication of arrays: returns array representing b o a? ensure difference
    r = _af_rmul(al, bl)
    # __mul__ does b(a(i)): compute expected_mul_array
    # but note: __mul__ pads shorter to longer then computes [b[i] for i in a] + b[len(a):]
    a_list = al[:]
    b_list = bl[:]
    if len(b_list) < len(a_list):
        b_list.extend(range(len(b_list), len(a_list)))
    perm_mul = [b_list[i] for i in a_list] + b_list[len(a_list):]
    # Ensure that _af_rmul and __mul__ produce different results for these arrays
    assert r != perm_mul

def test_mul_identity_behavior():
    # Multiplying by identity of same size yields composition equal to other perm appropriately
    p = Permutation([2, 0, 1, 4, 3])
    identity_same = Permutation(list(range(p.size())))
    assert list(p * identity_same) == [identity_same(p(i)) for i in range(p.size())]
    assert list(identity_same * p) == [p(identity_same(i)) for i in range(p.size())]