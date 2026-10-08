import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle, Permutation as Perm
from sympy.combinatorics.permutations import Permutation as PermutationClass

def test_new_empty_and_identity():
    # no args -> empty permutation
    p = Permutation()
    assert p.array_form == []
    assert p.size == 0

    # single integer -> identity of size a+1
    q = Permutation(3)
    assert q.array_form == [0,1,2,3]
    assert q.size == 4

def test_new_array_form_valid_and_invalid():
    # valid array form that includes 0..n-1
    p = Permutation([0,2,1,3])
    assert p.array_form == [0,2,1,3]
    assert p.size == 4

    # missing 0 should raise
    with pytest.raises(ValueError):
        Permutation([2,1])

    # duplicate elements in array form should raise
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_cycle_form_and_size_extension():
    # cyclic form: list of cycles
    p = Permutation([[4,5,6],[0,1]])
    # array form should be of length 7 mapping as docstring example
    assert isinstance(p.array_form, list)
    assert p.array_form[:7] == [1,0,2,3,5,6,4]
    assert p.size == 7

    # providing explicit size larger than max element should extend with singletons
    p2 = Permutation([[1,4],[3,5,2]], size=10)
    assert p2.size == 10
    # first six entries as expected, rest are singletons
    assert p2.array_form[:6] == [0,4,3,5,1,2]
    assert p2.array_form[6:] == [6,7,8,9]

def test_new_from_cycle_object_and_permutation_object():
    # Cycle object conversion: using Cycle to create cycles and pass it
    c = Cycle()
    c = c(0,1)
    c = c(2,3,4)
    p = Permutation(c)
    # permutation array form should reflect the cycles
    assert p.array_form[0:5] == [1,0,3,4,2]

    # Passing an existing Permutation instance (from Perm import) should
    # return the same when size matches
    base = Perm([0,2,1])
    p_same = Permutation(base)
    assert p_same is base

    # If size differs, should return new Permutation with requested size
    larger = Permutation(base.array_form, size=5)
    assert larger.size == 5
    assert larger.array_form[:3] == base.array_form
    assert larger.array_form[3:] == [3,4]

def test_new_non_sequence_arg_behavior():
    # non-sequence argument treated as integer identity
    p = Permutation(0)
    assert p.array_form == [0]
    assert p.size == 1

def test_new_invalid_argument_types():
    # mixed sequence/non-sequence in args should raise ValueError
    with pytest.raises(ValueError):
        Permutation([ [0,1], 2, [3] ])

    # completely invalid type should raise ValueError via final check
    class Dummy: pass
    with pytest.raises(ValueError):
        Permutation(Dummy())

# Ensure attributes referenced in __new__ are present and accessible
def test_internal_attributes_present():
    p = Permutation([0,1,2])
    assert hasattr(p, "_array_form")
    assert hasattr(p, "_size")
    # representation should not error
    r = repr(p)
    assert "Permutation" in r

if __name__ == "__main__":
    pytest.main([__file__])