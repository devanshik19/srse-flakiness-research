import pytest
from sympy.combinatorics.permutations import Permutation, _af_new

def test_mul_basic():
    # simple permutations a and b
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # a*b should be b(a(i)) for each i
    prod = a * b
    assert isinstance(prod, Permutation)
    assert list(prod) == [2, 0, 1]
    # verify by direct application
    assert [b(a(i)) for i in range(3)] == list(prod)

def test_mul_padding_longer_left():
    # Left (self) longer than right (other) -> right is padded
    a = Permutation([2, 0, 1, 3])  # length 4
    b = Permutation([1, 0])        # length 2
    prod = a * b
    # b is padded to length 4: b -> [1,0,2,3]; result is b(a(i))
    assert list(prod) == [prod_i for prod_i in [1,0,2,3]][:len(prod)]  # sanity check format
    # compute expected explicitly
    padded_b = [1, 0, 2, 3]
    expected = [padded_b[a_i] for a_i in a.array_form] + padded_b[len(a.array_form):]
    assert list(prod) == expected

def test_mul_padding_longer_right():
    # Right (other) longer than left (self) -> left is padded via b.extend in code path
    a = Permutation([1, 0])        # length 2
    b = Permutation([2, 0, 1])     # length 3
    prod = a * b
    # According to implementation, b is extended to max length and result is [b[i] for i in a] + b[len(a):]
    # Compute expected
    b_af = list(b)
    b_af.extend(list(range(len(b_af), len(list(a)))))  # this won't change here but emulate logic
    expected = [b_af[i] for i in list(a)] + b_af[len(list(a)):]
    assert list(prod) == expected
    # For these particular a,b expected equals [2,0,1]
    assert list(prod) == [2, 0, 1]

def test_mul_with_empty_other():
    # other is identity / empty array_form in the sense of [] -> result should be self.array_form
    a = Permutation([2, 1, 0])
    class FakePerm:
        # mimic a Permutation with empty array_form
        def __init__(self):
            self.array_form = []
    other = FakePerm()
    # __mul__ expects 'other' to be a Permutation (the code comment says __rmul__ makes sure),
    # but the implementation only accesses other.array_form, so this is sufficient.
    prod = a * other
    assert list(prod) == list(a)

def test_mul_with_list_coercion_like_behavior():
    # The code assumes other is a Permutation and uses other.array_form.
    # Simulate coercion from a list by wrapping list into a Permutation-like object.
    class WrapList:
        def __init__(self, lst):
            self.array_form = list(lst)
    a = Permutation([1, 0, 2])
    wrapped = WrapList([0, 1])  # 2-element identity-like list
    prod = wrapped * a  # uses Permutation.__rmul__ in real usage; here ensure __mul__ works when left is Permutation
    # We cannot directly call __mul__ with left non-Permutation, but ensure that Permutation * wrapped fails as expected
    with pytest.raises(AttributeError):
        # wrapped has array_form, but __mul__ expects 'other' to be Permutation; however implementation uses only array_form.
        # To ensure realistic behavior, attempt to call Permutation.__mul__ with other lacking methods normally present.
        _ = a * wrapped

def test_mul_commutation_difference_from_af_rmul():
    # demonstrate that __mul__ applies b(a(i)) ordering (different from _af_rmul)
    a = Permutation([1, 2, 0])
    b = Permutation([2, 0, 1])
    prod = a * b
    assert list(prod) == [1, 2, 0]  # b(a(i))
    # check against applying a then b by indexing manually matches
    assert [b(a(i)) for i in range(3)] == list(prod)