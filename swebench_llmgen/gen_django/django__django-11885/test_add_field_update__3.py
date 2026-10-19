import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update():
    # Create instances of User
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Instantiate the Collector
    collector = Collector(using='default')
    
    # Test with empty objs
    collector.add_field_update('email', 'updated@example.com', [])
    assert 'user1' not in collector.field_updates
    assert 'user2' not in collector.field_updates

    # Test with one user object
    collector.add_field_update('email', 'updated@example.com', [user1])
    assert User in collector.field_updates
    assert ('email', 'updated@example.com') in collector.field_updates[User]
    assert user1 in collector.field_updates[User][('email', 'updated@example.com')]
    
    # Test with multiple user objects
    collector.add_field_update('email', 'updated@example.com', [user1, user2])
    assert len(collector.field_updates[User][('email', 'updated@example.com')]) == 2
    assert user1 in collector.field_updates[User][('email', 'updated@example.com')]
    assert user2 in collector.field_updates[User][('email', 'updated@example.com')]