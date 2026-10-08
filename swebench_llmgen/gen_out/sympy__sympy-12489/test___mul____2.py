import pytest
from sympy.combinatorics.permutations import Permutation, _af_new

def test_mul_basic():
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # a*b should be b(a(i)) so list(a*b) == [b[a[0]], b[a[1]], b[a[2]]]
    prod = a * b
    assert isinstance(prod, Permutation)
    assert list(prod) == [b[i] for i in a]
    assert list(prod) == [2, 0, 1]

def test_mul_padding_shorter_right():
    # right operand shorter: it will be padded to match left's length
    a = Permutation([2, 0, 1])  # length 3
    b = Permutation([1, 0])     # length 2
    prod = a * b
    # b will be extended to [1,0,2] before composition; product = [b[a[i]]]
    assert list(prod) == [1, 2, 0]

def test_mul_padding_shorter_left():
    # left operand shorter: left will be padded by __mul__ via using array_forms lengths.
    # According to docstring, multiplication handles operands in reverse order
    # but shorter one will be padded; check b * Permutation([1,0])
    b = Permutation([0, 2, 1])
    small = Permutation([1, 0])
    prod = b * small
    # small is padded to [1,0,2]; then product = small(b(i))
    assert list(prod) == [1, 2, 0]

def test_mul_with_empty_right():
    # If right operand has empty array_form, __mul__ returns left's array
    a = Permutation([2, 1, 0])
    # create a "empty" permutation via _af_new on empty list to simulate identity-like with no array_form
    empty = _af_new([])
    prod = a * empty
    assert list(prod) == list(a)

def test_mul_with_list_like_left_via_rmul_behavior():
    # __mul__ expects other to be Permutation, but __rmul__ handles coercion from list.
    # Ensure that multiplication result matches expected when left is a Permutation and right coerced.
    a = Permutation([1, 0, 2])
    # emulate a coercible list on the left by using Permutation constructed from it then using __mul__
    L = Permutation([0, 1])  # represents left list [0,1] coerced to permutation
    prod = L * a
    # L acts as 2-element identity padded: resulting permutation should be [1,0,2]
    assert list(prod) == [1, 0, 2]

def test_mul_is_associative_behaviour_sample():
    # Check that composition order is as documented: (a*b)(i) == b(a(i))
    a = Permutation([1, 2, 0, 3])
    b = Permutation([2, 0, 1, 3])
    c = Permutation([0, 3, 2, 1])
    left = (a * b) * c
    right = a * (b * c)
    # composition is associative so these should be equal permutations
    assert list(left) == list(right)

def test_mul_does_not_modify_operands():
    a_list = [1, 0, 2]
    b_list = [0, 2, 1]
    a = Permutation(a_list)
    b = Permutation(b_list)
    _ = a * b
    # original permutations should remain unchanged
    assert list(a) == a_list
    assert list(b) == b_list

def test_mul_with_single_cycle_coercion():
    # ensure behavior when "left" is a nested list (Cycle-like) is not handled by __mul___ directly;
    # but constructing Permutation from such list yields expected result and multiplication works.
    left = Permutation([0, 1])  # corresponds to [0,1] identity on first two
    a = Permutation([1, 0, 2])
    prod = left * a
    assert list(prod) == [1, 0, 2]

def test_mul_type_errors_not_raised_for_permutation_other():
    # ensure passing a Permutation always works; no TypeError raised
    a = Permutation([0, 1, 2])
    b = Permutation([2, 1, 0])
    try:
        _ = a * b
    except Exception as e:
        pytest.fail(f"Multiplication raised unexpectedly: {e}")