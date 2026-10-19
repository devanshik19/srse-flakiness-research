import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

class TestOrderedSet:
    def test_discard_existing_item(self):
        os = OrderedSet([1, 2, 3])
        os.discard(2)
        assert 2 not in os

    def test_discard_non_existing_item(self):
        os = OrderedSet([1, 2, 3])
        os.discard(4)  # Should not raise an error
        assert len(os) == 3  # Size should remain unchanged

    def test_discard_multiple_times(self):
        os = OrderedSet([1, 2, 3])
        os.discard(2)
        os.discard(2)  # Discarding again, should not raise error
        assert len(os) == 2
        assert 2 not in os

    def test_discard_on_empty_set(self):
        os = OrderedSet()
        os.discard(1)  # Should not raise an error
        assert len(os) == 0  # Size should remain unchanged