import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Cycle  # Cycle used by constructor paths
from sympy.core import Basic

def test_new_no_args_creates_empty():
    p = Permutation()
    assert isinstance(p, Permutation)
    assert p._array_form == []
    assert p._size == 0
    assert repr(p).startswith("Permutation(")

def test_new_integer_creates_identity():
    p = Permutation(3)  # should create identity of size 4: 0..3
    assert p._array_form == [0,1,2,3]
    assert p._size == 4
    # check that constructing same size returns same object (or equal)
    q = Permutation(p)
    assert isinstance(q, Permutation)
    assert q._array_form == p._array_form

def test_new_array_form_valid_and_invalid():
    p = Permutation([0,2,1])
    assert p._array_form == [0,2,1]
    assert p._size == 3

    # missing zero or missing integers should raise
    with pytest.raises(ValueError):
        Permutation([2,1])  # 0..2 must be present

    # duplicate elements in array form should raise
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_cycle_form_and_size_extension():
    # cycle form as list of lists
    p = Permutation([[4,5,6],[0,1]])
    # array form should be produced and size should be 7 (max element +1)
    assert isinstance(p, Permutation)
    assert p._array_form == [1,0,2,3,5,6,4]
    assert p._size == 7

    # specifying a larger size should extend with fixed points
    p2 = Permutation([[1,4],[3,5,2]], size=10)
    assert p2._size == 10
    assert p2._array_form[:6] == [0,4,3,5,1,2]
    assert p2._array_form[6:] == [6,7,8,9]

def test_new_cycle_with_singleton_size_hint():
    # singletons can be used to indicate larger size
    p = Permutation([[4,5,6],[0,1],[19]])
    assert p._size == 20
    assert p._array_form == [1,0,2,3,5,6,4] + list(range(7,20))

def test_new_with_cycle_objects_and_perm_objects():
    # create a Cycle object and pass it
    c = Cycle([0,1,2])
    p = Permutation(c)
    # Cycle.list() gives array form for the cycle; check type and content
    assert isinstance(p, Permutation)
    assert p._array_form[0:3] == c.list()[:3]

    # pass an existing Permutation and request increased size -> new object
    base = Permutation([0,1])
    bigger = Permutation(base, size=4)
    assert bigger._size == 4
    assert bigger._array_form[:2] == [0,1]
    assert bigger._array_form[2:] == [2,3]

def test_invalid_argument_types_raise():
    # non-sequence but not int should raise via path that checks is_sequence
    with pytest.raises(ValueError):
        Permutation(object())

def test_dup_in_cycle_raises_message():
    # repeated elements in cycle form produce a helpful message
    with pytest.raises(ValueError) as exc:
        Permutation([[0,1],[1,2]])
    assert 'repeated elements' in str(exc.value)

def test_sequence_of_sequences_misuse():
    # Passing nested sequences incorrectly triggers ValueError earlier
    with pytest.raises(ValueError):
        # Provide a mixture that confuses has_variety check (list of mixed)
        Permutation([ [0,1], 2 ])

# Ensure Basic subclassing behavior: created object is an instance of Basic
def test_basic_subclass():
    p = Permutation([0,1,2])
    assert isinstance(p, Basic)