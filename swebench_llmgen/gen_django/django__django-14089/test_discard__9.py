import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

class TestOrderedSet:
    
    @pytest.fixture
    def ordered_set(self):
        return OrderedSet([1, 2, 3])

    def test_discard_existing_item(self, ordered_set):
        ordered_set.discard(2)
        assert len(ordered_set) == 2
        assert 2 not in ordered_set

    def test_discard_non_existing_item(self, ordered_set):
        initial_length = len(ordered_set)
        ordered_set.discard(99)  # Attempt to discard a non-existing item
        assert len(ordered_set) == initial_length  # Length should not change

    def test_discard_item_not_in_set(self, ordered_set):
        assert 4 not in ordered_set
        ordered_set.discard(4)  # Discard item not in the set
        assert len(ordered_set) == 3  # Length remains the same