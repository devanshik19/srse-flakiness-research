import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

class TestOrderedSet:

    @pytest.fixture
    def ordered_set(self):
        return OrderedSet([1, 2, 3])

    def test_discard_existing_item(self, ordered_set):
        ordered_set.discard(2)
        assert 2 not in ordered_set

    def test_discard_non_existing_item(self, ordered_set):
        initial_length = len(ordered_set)
        ordered_set.discard(4)  # Discarding an item that doesn't exist
        assert len(ordered_set) == initial_length  # Length should remain the same
        assert all(item in ordered_set for item in [1, 2, 3])  # All other items should remain

    def test_discard_multiple_times(self, ordered_set):
        ordered_set.discard(1)
        assert 1 not in ordered_set
        ordered_set.discard(1)  # Discarding again
        assert 1 not in ordered_set  # Should still not be present