import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

class TestOrderedSet:
    @pytest.fixture
    def ordered_set(self):
        return OrderedSet()

    def test_discard_existing_item(self, ordered_set):
        ordered_set.add('item1')
        ordered_set.discard('item1')
        assert 'item1' not in ordered_set

    def test_discard_non_existing_item(self, ordered_set):
        ordered_set.add('item1')
        ordered_set.discard('item2')  # No error should occur
        assert 'item1' in ordered_set

    def test_discard_none_item(self, ordered_set):
        ordered_set.add('item1')
        ordered_set.discard(None)  # Should handle None gracefully
        assert 'item1' in ordered_set

    def test_discard_empty_set(self, ordered_set):
        ordered_set.discard('item1')  # Should not raise an error
        assert len(ordered_set) == 0