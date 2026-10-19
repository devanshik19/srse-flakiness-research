import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update():
    collector = Collector(using='default')
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Test case 1: Adding updates for users
    collector.add_field_update('email', 'updated@example.com', [user1, user2])
    assert len(collector.field_updates) == 1
    assert (('email', 'updated@example.com') in collector.field_updates[User])
    assert user1 in collector.field_updates[User][('email', 'updated@example.com')]
    assert user2 in collector.field_updates[User][('email', 'updated@example.com')]

    # Test case 2: Adding updates with empty objs
    collector.add_field_update('email', 'not_updated@example.com', [])
    assert len(collector.field_updates) == 1  # No change should occur

    # Test case 3: Adding updates for single user
    user3 = User.objects.create(username='user3', email='user3@example.com')
    collector.add_field_update('email', 'single_update@example.com', [user3])
    assert len(collector.field_updates) == 1
    assert (('email', 'single_update@example.com') in collector.field_updates[User])
    assert user3 in collector.field_updates[User][('email', 'single_update@example.com')]