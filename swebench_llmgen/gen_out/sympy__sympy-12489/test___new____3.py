import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Permutation as PermClass  # not used but ensure imports
from sympy.combinatorics.cycles import Cycle
from sympy.core import Basic

def test_new_empty_and_identity():
    # no args -> empty permutation
    p = Permutation()
    assert isinstance(p, Basic)
    assert p.array_form == []
    assert p.size == 0

    # single integer -> identity of that size (0..n)
    q = Permutation(3)  # should create [0,1,2,3]
    assert q.array_form == [0,1,2,3]
    assert q.size == 4

def test_new_array_form_valid_and_invalid():
    # valid array form
    p = Permutation([0,2,1])
    assert p.array_form == [0,2,1]
    assert p.size == 3

    # missing 0 should raise
    with pytest.raises(ValueError):
        Permutation([2,1])

    # repeated elements in array form should raise
    with pytest.raises(ValueError):
        Permutation([0,1,1])

def test_new_cycle_form_basic():
    # cycle form as list of lists
    p = Permutation([[4,5,6],[0,1]])
    # expected array form from docstring
    assert p.array_form == [1,0,2,3,5,6,4]
    assert p.size == 7

    # cycle form with explicit singleton giving size
    p2 = Permutation([[4,5,6],[0,1],[19]], size=20)
    assert p2.size == 20
    # array_form should have length 20 and agree on first part
    assert p2.array_form[:7] == [1,0,2,3,5,6,4]
    assert len(p2.array_form) == 20
    # values beyond given cycles should be identity
    assert p2.array_form[7:] == list(range(7,20))

def test_new_cycle_sequence_without_singletons_but_with_size():
    # cycles not specifying singletons but size provided
    p = Permutation([[1,4],[3,5,2]], size=10)
    assert p.array_form == [0,4,3,5,1,2,6,7,8,9]
    assert p.size == 10

def test_new_from_cycle_and_from_permutation_objects():
    # from Cycle object directly
    c = Cycle()
    c = c(4,5,6)
    c = c(0,1)
    p = Permutation(c)
    assert p.array_form == [1,0,2,3,5,6,4]

    # from Permutation object returns copy or same depending on size
    orig = Permutation([0,1,2])
    same = Permutation(orig)
    assert same is orig  # returns the same object when size matches

    # if size differs, a new Permutation is returned with extended size
    extended = Permutation(orig, size=5)
    assert extended is not orig
    assert extended.array_form == [0,1,2,3,4]
    assert extended.size == 5

def test_new_invalid_argument_types():
    # non-sequence single argument that's not int should raise via flow:
    # pass an object that is sequence-like variety to trigger ValueError path
    # create a heterogeneous sequence (sequence of sequences and ints) to set has_variety True
    with pytest.raises(ValueError):
        Permutation([ [0,1], 2 ])

def test_new_array_form_extend_size():
    # providing array-form and larger size should extend with identity entries
    p = Permutation([0,2,1], size=5)
    assert p.size == 5
    assert p.array_form == [0,2,1,3,4]

def test_new_type_checks_and_copy_behavior():
    # Passing a Cycle instance with size argument creates correct size
    c = Cycle()(0,1,2)
    p = Permutation(c, size=6)
    assert p.size == 6
    # array form should be a list of ints and length matches size
    assert isinstance(p.array_form, list)
    assert all(isinstance(i, int) for i in p.array_form)
    assert len(p.array_form) == 6

    # Passing a plain integer 0 returns identity [0]
    p0 = Permutation(0)
    assert p0.array_form == [0]
    assert p0.size == 1