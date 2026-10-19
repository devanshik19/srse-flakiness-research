import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

class TestOrderedSet:

    def test_discard_existing_item(self):
        os = OrderedSet()
        os.add('item1')
        os.discard('item1')
        assert 'item1' not in os

    def test_discard_non_existing_item(self):
        os = OrderedSet()
        os.add('item2')
        os.discard('item3')  # Discarding an item that does not exist
        assert 'item2' in os

    def test_discard_item_not_in_set(self):
        os = OrderedSet()
        os.discard('item4')  # Discarding an item that was never added
        assert len(os) == 0
    
    def test_discard_multiple_items(self):
        os = OrderedSet()
        os.add('item5')
        os.add('item6')
        os.discard('item5')
        os.discard('item6')
        assert len(os) == 0