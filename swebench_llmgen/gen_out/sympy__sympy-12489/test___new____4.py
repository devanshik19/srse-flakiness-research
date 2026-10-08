import pytest
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import Permutation as Perm  # alias if needed
from sympy.combinatorics.cycles import Cycle
from sympy.core import Basic

def test_new_empty_and_identity():
    # no args -> empty permutation
    p = Permutation()
    assert isinstance(p, Basic)
    assert p.array_form == []
    assert p.size == 0

    # single int -> identity of size n+1
    q = Permutation(2)
    assert q.array_form == [0, 1, 2]
    assert q.size == 3

def test_new_array_form_valid_and_invalid():
    # valid array form
    p = Permutation([0, 2, 1])
    assert p.array_form == [0, 2, 1]
    assert p.size == 3

    # missing 0 should raise
    with pytest.raises(ValueError):
        Permutation([2, 1])

    # repeated elements should raise
    with pytest.raises(ValueError):
        Permutation([0, 1, 1])

def test_new_cycle_form_and_size_extension():
    # cycle form list of lists
    p = Permutation([[4, 5, 6], [0, 1]])
    # expected array form from docstring example
    assert p.array_form == [1, 0, 2, 3, 5, 6, 4]
    assert p.size == 7

    # cycle form with explicit size larger than max element
    p2 = Permutation([[4, 5, 6], [0, 1], [19]], size=20)
    assert p2.array_form[:7] == [1, 0, 2, 3, 5, 6, 4]
    assert p2.size == 20
    # positions beyond filled are singletons
    assert p2.array_form[7] == 7 and p2.array_form[19] == 19

def test_new_cycle_with_size_fill():
    # cycle notation with provided size fills the rest as fixed points
    p = Permutation([[1, 4], [3, 5, 2]], size=10)
    assert p.size == 10
    # ensure first part matches example
    assert p.array_form[:6] == [0, 4, 3, 5, 1, 2]
    # remaining entries are identity positions
    assert p.array_form[6:] == [6,7,8,9]

def test_new_from_cycle_object_and_permutation_copy_and_resize():
    # from Cycle instance
    c = Cycle()
    c = c(0, 2, 1)
    p = Permutation(c)
    # Cycle list() produces array form
    assert isinstance(p, Permutation)
    assert p.array_form == [2, 0, 1]

    # from Permutation instance returns same object if size matches
    orig = Permutation([0,1,2,3])
    same = Permutation(orig)
    assert same is orig

    # but with different size returns new with extended identity part
    bigger = Permutation(orig, size=6)
    assert bigger is not orig
    assert bigger.size == 6
    assert bigger.array_form == [0,1,2,3,4,5]

def test_new_non_sequence_arg_raises_or_handles():
    # non-sequence (int handled above), test a Falsey non-sequence negative to ensure behavior
    # negative integer produces identity of length n+1 where n negative -> range(-1+1)=range(0)
    p = Permutation(0)
    assert p.array_form == [0]

    # invalid argument type: e.g., object that is sequence-like mixed -> should raise
    class BadSeq:
        def __iter__(self):
            yield [1]
        def __len__(self):
            return 1
    # The constructor expects sequences of ints/lists; providing a nested mix with variety leads to ValueError
    with pytest.raises(ValueError):
        Permutation(BadSeq())

def test_new_incorrect_argument_counts():
    # multiple positional arguments are treated as cycle elements (Cycle(*args).list)
    p = Permutation(0, 1)  # creates cycle (0 1)
    assert isinstance(p, Permutation)
    # cycle (0 1) as array form on two elements swaps them
    assert p.array_form == [1, 0]

def test_new_size_truncation_not_allowed():
    # ensure that providing size smaller than array length does not truncate (it ignores size smaller)
    p = Permutation([0,1,2,3], size=2)
    # size is set to len(aform) not the provided smaller size
    assert p.size == 4
    assert p.array_form == [0,1,2,3]