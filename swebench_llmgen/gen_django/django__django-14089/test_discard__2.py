import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

class TestOrderedSet:
    def test_discard_existing_item(self):
        ordered_set = OrderedSet([1, 2, 3])
        ordered_set.discard(2)
        assert 2 not in ordered_set

    def test_discard_non_existing_item(self):
        ordered_set = OrderedSet([1, 2, 3])
        ordered_set.discard(4)  # Should not raise an error
        assert len(ordered_set) == 3

    def test_discard_multiple_times(self):
        ordered_set = OrderedSet([1, 2, 3])
        ordered_set.discard(1)
        ordered_set.discard(1)  # Calling discard again should not raise an error
        assert 1 not in ordered_set
        assert len(ordered_set) == 2