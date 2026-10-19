import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update():
    # Create a Collector instance
    collector = Collector(using='default')

    # Prepare test data
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')
    users = [user1, user2, user3]

    # Test scheduling field updates with a non-empty list of user instances
    collector.add_field_update('username', 'updated_user', users)

    # Accessing the internal state of Collector to verify the field update
    assert 'username' in collector.field_updates[User]
    assert ('username', 'updated_user') in collector.field_updates[User]
    assert len(collector.field_updates[User][('username', 'updated_user')]) == 3
    assert user1 in collector.field_updates[User][('username', 'updated_user')]
    assert user2 in collector.field_updates[User][('username', 'updated_user')]
    assert user3 in collector.field_updates[User][('username', 'updated_user')]

    # Test scheduling field updates with an empty list
    collector.add_field_update('username', 'another_update', [])
    # Ensure no change in state
    assert len(collector.field_updates[User][('username', 'updated_user')]) == 3