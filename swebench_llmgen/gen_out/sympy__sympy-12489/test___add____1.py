import pytest
from sympy.combinatorics.permutations import Permutation, Perm
from sympy.core.compatibility import range

def test_add_basic_identity():
    # identity plus any permutation by adding its rank should return that permutation
    Permutation.print_cyclic = False
    I = Permutation([0, 1, 2, 3])
    a = Permutation([2, 1, 3, 0])
    # Verify rank and cardinality properties used by __add__
    assert isinstance(a.rank(), int)
    assert isinstance(a.cardinality(), int)
    # I has rank 0 so I + a.rank() should be a
    res = I + a.rank()
    assert isinstance(res, Permutation)
    assert res.array_form == a.array_form
    # also verify that adding using another permutation-like numeric other (e.g., its rank)
    res2 = I + a.rank()
    assert res2 == a

def test_add_wraparound_and_rank_property():
    # test wraparound when rank + other >= cardinality
    Permutation.print_cyclic = False
    p = Permutation([1, 0, 2])  # size 3, small permutation
    # get current rank and cardinality
    r = p.rank()
    c = p.cardinality()
    # choose other such that (r + other) >= c to force modulo wrap
    other = (c - r) + 1  # results in rank = 1 after modulo
    res = p + other
    # Compute expected via unrank_lex
    expected_rank = (r + other) % c
    expected = Perm.unrank_lex(p.size, expected_rank)
    expected._rank = expected_rank
    assert res.array_form == expected.array_form
    assert res._rank == expected_rank

def test_add_with_zero_and_full_cycle():
    # adding zero should return permutation with same array_form but new object
    Permutation.print_cyclic = False
    p = Permutation([2, 0, 1, 3])
    res = p + 0
    assert isinstance(res, Permutation)
    assert res.array_form == p.array_form
    # ensure that changing returned object's _rank does not mutate original
    old_rank = getattr(p, "_rank", None)
    res._rank = (res._rank + 1) % res.cardinality()
    assert getattr(p, "_rank", None) == old_rank

def test_add_invalid_type_raises():
    # __add__ expects an integer-like other; passing incompatible type should raise
    Permutation.print_cyclic = False
    p = Permutation([0, 1, 2])
    with pytest.raises(TypeError):
        # strings or objects that cannot be used in arithmetic with int should error
        _ = p + "not an int"

def test_add_uses_unrank_lex_and_sets_rank():
    # ensure that the returned permutation has its _rank set to the computed value
    Permutation.print_cyclic = False
    p = Permutation([0, 2, 1, 3])
    other = 5
    rank_before = p.rank()
    c = p.cardinality()
    computed = (rank_before + other) % c
    res = p + other
    assert hasattr(res, "_rank")
    assert res._rank == computed
    # Also verify that unrank_lex produced permutation of requested size
    assert res.size == p.size

# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__])