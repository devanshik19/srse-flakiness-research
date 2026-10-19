import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

class TestOrderedSet:
    @pytest.fixture
    def ordered_set(self):
        os = OrderedSet()
        os.add('item1')
        os.add('item2')
        return os

    def test_discard_existing_item(self, ordered_set):
        ordered_set.discard('item1')
        assert 'item1' not in ordered_set

    def test_discard_non_existing_item(self, ordered_set):
        initial_length = len(ordered_set)
        ordered_set.discard('item3')
        assert len(ordered_set) == initial_length