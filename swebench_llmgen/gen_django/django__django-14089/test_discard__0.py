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
        os.discard(4)  # should not raise an error
        assert 1 in os
        assert 2 in os
        assert 3 in os

    def test_discard_item_twice(self):
        os = OrderedSet([1, 2, 3])
        os.discard(2)
        os.discard(2)  # second discard should also not raise an error
        assert 2 not in os

    def test_discard_on_empty_set(self):
        os = OrderedSet()
        os.discard(1)  # should not raise an error
        assert len(os) == 0