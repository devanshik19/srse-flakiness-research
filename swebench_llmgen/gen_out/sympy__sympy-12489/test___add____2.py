import pytest
from sympy.combinatorics.permutations import Permutation

def test_add_basic_rank_and_unrank_lex():
    # identity plus another permutation's rank should return that permutation
    Permutation.print_cyclic = False
    I = Permutation([0, 1, 2, 3])
    a = Permutation([2, 1, 3, 0])
    # ensure rank works and addition follows docstring example
    assert (I + a.rank()) == a

def test_add_with_permutation_operand_and_wrapping():
    # addition when other is a Permutation instance should treat 'other' as integer via rank()
    p = Permutation([1, 0, 2])  # size 3
    q = Permutation([2, 1, 0])  # size 3
    # p.rank() + q.rank() may exceed cardinality; __add__ should wrap modulo cardinality
    sum1 = p + q.rank()
    # compute expected by unranking lex of (p.rank()+q.rank()) % cardinality
    expected_rank = (p.rank() + q.rank()) % p.cardinality
    expected = Permutation.unrank_lex(p.size, expected_rank)
    expected._rank = expected_rank
    assert sum1 == expected

def test_add_with_integer_other_and_zero_identity():
    # adding an integer rank to identity yields permutation with that rank
    I = Permutation([0,1,2,3,4])
    r = 5
    # ensure wrapping modulo cardinality
    result = I + r
    expected_rank = (I.rank() + r) % I.cardinality
    expected = Permutation.unrank_lex(I.size, expected_rank)
    expected._rank = expected_rank
    assert result == expected

def test_add_preserves_size_and_sets_rank_attribute():
    # ensure returned permutation has correct size and _rank attribute set
    p = Permutation([2,0,1,3])
    other_rank = 6
    res = p + other_rank
    assert res.size == p.size
    assert hasattr(res, "_rank")
    assert res._rank == (p.rank() + other_rank) % p.cardinality

def test_add_invalid_type_raises_attribute_error():
    # passing an object without integer conversion that doesn't behave as expected
    p = Permutation([0,1,2])
    class Bad:
        def __int__(self):
            raise TypeError("cannot convert")
        def __index__(self):
            raise TypeError("cannot convert")

    bad = Bad()
    with pytest.raises(TypeError):
        # __add__ expects other to be usable in arithmetic; using a bad object should raise
        _ = p + bad