import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

def test_discard_existing_item():
    ordered_set = OrderedSet([1, 2, 3])
    ordered_set.discard(2)
    assert 2 not in ordered_set

def test_discard_non_existent_item():
    ordered_set = OrderedSet([1, 2, 3])
    ordered_set.discard(4)  # This should not raise an error
    assert 1 in ordered_set
    assert 2 in ordered_set
    assert 3 in ordered_set

def test_discard_no_item_in_empty_set():
    ordered_set = OrderedSet()
    ordered_set.discard(1)  # This should also not raise an error
    assert len(ordered_set) == 0