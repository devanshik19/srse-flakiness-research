import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db import models

class TestCollector:

    @pytest.fixture
    def setup_users(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        return user1, user2, user3

    def test_collect_fast_delete(self, setup_users):
        user1, user2, user3 = setup_users
        collector = Collector(using=None)
        collector.fast_deletes = []

        # Simulate a straightforward fast delete scenario
        assert collector.can_fast_delete([user1, user2])
        collector.collect([user1, user2], collect_related=False)
        assert collector.fast_deletes == [[user1, user2]]

    def test_collect_no_fast_delete(self, setup_users):
        user1, user2, user3 = setup_users
        collector = Collector(using=None)
        collector.fast_deletes = []

        # Break a fast delete condition by adding a new user
        collector.add([user3], None, False, False)
        
        # Now it should not fast delete
        collector.collect([user1, user2], collect_related=False)
        assert collector.fast_deletes == []

    def test_collect_with_keep_parents(self, setup_users):
        user1, user2, user3 = setup_users
        collector = Collector(using=None)

        # Collect user1 and user2 without deleting parent objects
        collector.collect([user1, user2], keep_parents=True)
        
        # Ensure that no fast delete was performed
        assert len(collector.fast_deletes) == 0

    def test_collect_with_related_objects(self, setup_users):
        user1, user2, user3 = setup_users
        collector = Collector(using=None)
        
        # Assuming there exists a related model, we simulate it
        user1.profile = Profile.objects.create(user=user1)
        user2.profile = Profile.objects.create(user=user2)

        collector.collect([user1, user2], collect_related=True)
        
        # Assert that related objects are collected for deletion as well
        assert len(collector.fast_deletes) == 0  # Fast delete should not happen
        # Check relations/workload; needs a way to validate if profiles are queued for delete
        
    def test_collect_reverse_dependency(self, setup_users):
        user1, user2, user3 = setup_users
        collector = Collector(using=None)

        collector.collect([user1], source=user2, reverse_dependency=True)
        
        # Check that user1 is collected for deletion 
        assert user1 in collector.fast_deletes

    def test_collect_with_nullable(self, setup_users):
        user1, user2, user3 = setup_users
        collector = Collector(using=None)

        # Collect with nullable dependencies thus emulating related deletions under nullable constraints
        collector.collect([user1, user2], nullable=True)
        
        # Expected behavior based on model constraints
        assert user1 in collector.fast_deletes or user2 in collector.fast_deletes