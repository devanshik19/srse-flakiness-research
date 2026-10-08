import pytest
# Required dependencies (kept to mirror module environment; not all used directly here)
from __future__ import print_function, division
import random
from collections import defaultdict
from sympy.core import Basic
from sympy.core.compatibility import is_sequence, reduce, range, as_int
from sympy.utilities.iterables import (flatten, has_variety, minlex,
    has_dups, runs)
from sympy.polys.polytools import lcm
from sympy.matrices import zeros
from mpmath.libmp.libintmath import ifac

# Import the Permutation class from the target module
from sympy.combinatorics.permutations import Permutation

# Helpers to construct permutations easily in array form:
# Permutation in sympy accepts sequence to create permutation; ensure behavior.
def af_from_list(lst):
    # SymPy Permutation accepts a list directly
    return Permutation(lst)

def invert_array_form(perm):
    # Use Python-level inverse by applying permutation then inverting mapping
    # Permutation has .array_form() which returns list mapping 0..n-1 -> image
    af = perm.array_form
    # Build inverse array
    inv = [0] * len(af)
    for i, v in enumerate(af):
        inv[v] = i
    return Permutation(inv)

def mul_inv_expected(self_perm, other_perm):
    # Expected result is other * (~self)
    inv_self = invert_array_form(self_perm)
    # Multiply: other_perm * inv_self
    return other_perm * inv_self

def assert_perm_equal(p1, p2):
    # Compare array forms for equality and identity
    assert p1.array_form == p2.array_form
    # also compare cycle structure if available
    if hasattr(p1, "cycle_structure") and hasattr(p2, "cycle_structure"):
        assert p1.cycle_structure == p2.cycle_structure

def test_mul_inv_identity_behavior():
    # identity permutation size 5
    id_perm = Permutation(list(range(5)))
    # pick a random permutation other
    other = Permutation([2,0,4,1,3])
    # id.mul_inv(other) should compute other * ~id = other * id = other
    result = id_perm.mul_inv(other)
    assert_perm_equal(result, other)

def test_mul_inv_with_self_inverse():
    # self is its own inverse (a product of disjoint transpositions)
    self_perm = Permutation([1,0,3,2])  # (0 1)(2 3)
    # other arbitrary
    other = Permutation([2,3,0,1])
    # expected = other * ~self (but ~self == self)
    expected = other * self_perm
    res = self_perm.mul_inv(other)
    assert_perm_equal(res, expected)

def test_mul_inv_general_cases():
    # Several random tests with small sizes to cover different branches
    tests = [
        ([1,2,0], [2,0,1]),        # 3-cycle combinations
        ([0,2,1,4,3], [4,3,2,1,0]),# mix of fixed points and swaps
        ([3,0,1,2], [1,3,0,2]),    # differing sizes and shuffles
        (list(range(6)), [5,4,3,2,1,0]) # self identity vs reversed
    ]
    for self_af, other_af in tests:
        self_p = Permutation(self_af)
        other_p = Permutation(other_af)
        res = self_p.mul_inv(other_p)
        expected = mul_inv_expected(self_p, other_p)
        assert_perm_equal(res, expected)

def test_mul_inv_raises_on_mismatched_sizes():
    # mul_inv expects both to have internal array_form; differing sizes may raise
    a = Permutation([1,0,2])  # size 3
    b = Permutation([1,0,3,2])  # size 4
    # Behavior: attempt to invert and right-multiply; this should raise due to mismatched sizes
    with pytest.raises(Exception):
        a.mul_inv(b)

def test_mul_inv_does_not_mutate_operands():
    # Ensure original permutations are not changed
    self_af = [2,0,1,3]
    other_af = [1,3,0,2]
    self_p = Permutation(self_af)
    other_p = Permutation(other_af)
    # copy originals
    orig_self = list(self_p.array_form)
    orig_other = list(other_p.array_form)
    _ = self_p.mul_inv(other_p)
    assert self_p.array_form == orig_self
    assert other_p.array_form == orig_other