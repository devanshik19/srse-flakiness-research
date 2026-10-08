import pytest
from sympy.combinatorics.permutations import Permutation, _af_new

def test_mul_basic():
    # simple permutations a and b
    a = Permutation([1, 0, 2])
    b = Permutation([0, 2, 1])
    # a*b should be b(a(i)) for each i: compute expected explicitly
    expected = [b(a(i)) for i in range(3)]
    res = a * b
    assert isinstance(res, Permutation)
    assert list(res) == expected
    # Also ensure commutativity does not hold in general
    res2 = b * a
    assert list(res2) != list(res)

def test_mul_with_different_lengths():
    # b shorter than a: will be padded
    a = Permutation([2, 0, 1])  # length 3
    b = Permutation([1, 0])     # length 2
    prod1 = b * a
    prod2 = a * b
    # Check that both return Permutation and have expected lengths
    assert isinstance(prod1, Permutation)
    assert isinstance(prod2, Permutation)
    assert len(list(prod1)) == 3
    assert len(list(prod2)) == 3
    # Explicitly compute expected behaviour per implementation:
    # For b * a: a = a.array_form, b = b.array_form padded to len(a)
    a_af = a.array_form
    b_af = b.array_form.copy()
    b_af.extend(list(range(len(b_af), len(a_af))))
    expected1 = [b_af[i] for i in a_af] + b_af[len(a_af):]
    assert list(prod1) == expected1
    # For a * b: a is padded if needed
    a_af2 = a.array_form.copy()
    a_af2.extend(list(range(len(a_af2), len(b.array_form))))
    expected2 = [a_af2[i] for i in b.array_form] + a_af2[len(b.array_form):]
    assert list(prod2) == expected2

def test_mul_with_empty_other():
    # other.array_form empty means other is identity of length 0: product should be a
    a = Permutation([1, 0, 2])
    class DummyPerm:
        # mimic minimal interface: array_form attribute
        def __init__(self, af):
            self.array_form = af
    other = DummyPerm([])
    # __rmul__ in real code ensures conversion; here test __mul__ path when other.array_form == []
    res = a * other
    assert list(res) == a.array_form

def test_mul_with_list_coercion_like_behavior():
    # The code expects other to be a Permutation (or at least have array_form).
    # Simulate passing a list wrapped in an object with array_form to mimic coercion.
    a = Permutation([2, 1, 0])
    # simulate a left list [0,1] * a case from doc: when list is on left, __rmul__ usually converts
    left = type("L", (), {})()
    left.array_form = [0, 1]  # shorter than a
    res = left * a  # relies on __rmul__ of Permutation in real usage; here left has no __mul__, so use a.__rmul__
    # To actually test a.__rmul__, call Permutation.__rmul__ directly if available
    res_direct = Permutation.__rmul__(a, left)
    assert isinstance(res_direct, Permutation)
    # Result should be permutation of length max(len(left), len(a))
    assert len(list(res_direct)) == max(len(left.array_form), len(a.array_form))

def test_mul_edge_cases_identity():
    # identity times permutation and vice versa
    p = Permutation([2, 0, 1])
    id_small = Permutation([])
    # according to implementation, if other.array_form is empty, return self.array_form
    assert list(p * id_small) == p.array_form
    # but id * p when id is shorter should pad and produce potentially different result
    id_two = Permutation([0, 1])
    res = id_two * p
    # compute expected via implementation semantics
    a_af = id_two.array_form.copy()
    b_af = p.array_form.copy()
    a_af.extend(list(range(len(a_af), len(b_af))))
    expected = [a_af[i] for i in b_af] + a_af[len(b_af):]
    assert list(res) == expected

# Run the tests if executed as a script (useful for manual runs)
if __name__ == "__main__":
    pytest.main([__file__])