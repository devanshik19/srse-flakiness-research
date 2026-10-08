import pytest
from sympy.combinatorics.permutations import Permutation, _af_rmul

def test_mul_basic_mapping_and_order():
    # a(i) then b(...) => b(a(i))
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    prod = a * b
    # list(prod) gives array_form
    assert list(prod) == [2, 0, 1]
    # explicit check b(a(i))
    assert [b(a(i)) for i in range(3)] == [2, 0, 1]

def test_mul_padding_shorter():
    # shorter on right gets padded when right is shorter
    a = Permutation([1, 0, 2])
    b = Permutation([1, 0])    # length 2
    # a * b : b is on right, so b is extended to match a then composed
    left_comp = a * b
    # compute expected: extend b to length 3 -> [1,0,2]; then b[a[i]]
    expected = [1, 2, 0]  # b extended applied to a: b[a[0]]=b[1]=0? careful compute:
    # Let's compute explicitly to avoid confusion:
    b_ext = [1,0,2]
    expected = [b_ext[i] for i in list(a)]
    assert list(left_comp) == expected

    # shorter on left: left is shorter will be padded by __rmul__ before mul,
    # emulate by using a Permutation on left with larger length when multiplied on left
    # Here test b * a where a is longer
    right_comp = b * a
    # b is left, a is right in product: result is a(b(i))
    # But __mul__ implementation assumes left=self, right=other with mapping b(a(i)).
    # For b * a we expect list(b*a) == [a[b[i]] for i in range(maxlen)]
    maxlen = max(len(list(b)), len(list(a)))
    b_list = list(b) + list(range(len(list(b)), maxlen))
    a_list = list(a) + list(range(len(list(a)), maxlen))
    expected2 = [a_list[b_list[i]] for i in range(maxlen)]
    assert list(right_comp) == expected2

def test_mul_with_empty_other():
    # if other.array_form is empty, __mul__ should return self.array_form
    a = Permutation([2, 0, 1])
    # create a Permutation that represents the empty array_form (identity of length 0)
    empty = Permutation([])  # array_form == []
    prod = a * empty
    assert list(prod) == list(a)
    # also empty * a should behave (coercion via __rmul__)
    prod2 = empty * a
    # empty is treated as identity padded to a's length -> yields a
    assert list(prod2) == list(a)

def test_mul_with_list_coercion_like_behavior():
    # The docstring shows lists can appear on left via __rmul__ coercion.
    # Simulate by constructing Permutation from list and using __rmul__ behavior:
    a = Permutation([1,0,2])
    # Emulate [0,1] * a -> coercion should treat [0,1] as a 2-element identity then padded
    left_list = [0,1]
    # Convert to a Permutation as __rmul__ would have done
    left_perm = Permutation(left_list)
    res = left_perm * a
    # Expect that left identity padded to length 3 then composed with a yields a
    assert list(res) == list(a)

def test_mul_multiple_lengths_and_contents():
    # test more combinations, random small permutations to exercise branches
    import random
    for size_a in range(1,5):
        for size_b in range(0,5):
            # create random permutations array forms (not necessarily valid permutation arrays)
            # but use Permutation to canonicalize
            arr_a = list(range(size_a))
            arr_b = list(range(size_b))
            random.shuffle(arr_a)
            random.shuffle(arr_b)
            A = Permutation(arr_a)
            B = Permutation(arr_b)
            C = A * B
            # manual composition with padding as in __mul__:
            a = list(A)
            b = list(B)
            if not b:
                expected = a
            else:
                b = b[:]  # copy
                b.extend(list(range(len(b), len(a))))
                expected = [b[i] for i in a] + b[len(a):]
            assert list(C) == expected