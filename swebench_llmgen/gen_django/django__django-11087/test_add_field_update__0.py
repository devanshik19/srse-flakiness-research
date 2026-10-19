import pytest
from collections import Counter
from django.db import IntegrityError, connections, transaction
from django.db.models import signals, sql
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

class TestCollector:
    @pytest.fixture
    def collector(self):
        return Collector(using='default')

    @pytest.fixture
    def user_instances(self):
        return [User(username=f'user{i}') for i in range(5)]

    def test_add_field_update_with_empty_objs(self, collector):
        # Test with an empty list of objects
        collector.add_field_update('username', 'new_value', [])
        assert not collector.field_updates

    def test_add_field_update_with_single_object(self, collector, user_instances):
        # Test with a single object
        user = user_instances[0]
        user.save()
        collector.add_field_update('username', 'new_username', [user])
        assert len(collector.field_updates) == 1
        assert 'username' in collector.field_updates[user.__class__]
        assert collector.field_updates[user.__class__][('username', 'new_username')] == {user}

    def test_add_field_update_with_multiple_objects(self, collector, user_instances):
        # Test with multiple objects
        for user in user_instances:
            user.save()
        collector.add_field_update('username', 'new_username', user_instances)
        assert len(collector.field_updates) == 1
        assert 'username' in collector.field_updates[User]
        assert collector.field_updates[User][('username', 'new_username')] == set(user_instances)

    def test_add_field_update_with_different_fields(self, collector, user_instances):
        # Test with different field updates
        for user in user_instances:
            user.save()
        collector.add_field_update('username', 'new_username', user_instances)
        collector.add_field_update('email', 'new_email@example.com', user_instances[:2])
        
        assert len(collector.field_updates) == 1
        assert 'username' in collector.field_updates[User]
        assert 'email' in collector.field_updates[User]
        assert collector.field_updates[User][('username', 'new_username')] == set(user_instances)
        assert collector.field_updates[User][('email', 'new_email@example.com')] == set(user_instances[:2])