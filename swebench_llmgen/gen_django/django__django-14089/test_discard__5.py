import pytest
from django.contrib.auth.models import User
from django.utils.datastructures import OrderedSet

class TestOrderedSet:
    def setup_method(self):
        self.ordered_set = OrderedSet()

    def test_discard_existing_item(self):
        user = User(username='testuser')
        user.save()
        self.ordered_set.add(user)
        assert user in self.ordered_set

        self.ordered_set.discard(user)
        assert user not in self.ordered_set

    def test_discard_non_existing_item(self):
        user1 = User(username='testuser1')
        user1.save()
        user2 = User(username='testuser2')
        user2.save()

        self.ordered_set.add(user1)
        assert user1 in self.ordered_set
        assert user2 not in self.ordered_set

        self.ordered_set.discard(user2)  # Should not raise an error

        # Ensure the state of ordered_set remains unchanged for user1
        assert user1 in self.ordered_set