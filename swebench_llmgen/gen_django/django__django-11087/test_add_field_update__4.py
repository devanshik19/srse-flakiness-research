import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update():
    # Arrange
    user1 = User(username='user1', email='user1@example.com')
    user2 = User(username='user2', email='user2@example.com')
    user1.save()
    user2.save()
    
    collector = Collector(using='default')  # Instance of Collector
    field = 'email'
    value = 'updated@example.com'
    
    # Act
    collector.add_field_update(field, value, [user1, user2])
    
    # Assert
    assert (field, value) in collector.field_updates[User]
    assert user1 in collector.field_updates[User][(field, value)]
    assert user2 in collector.field_updates[User][(field, value)]
    
    # Test with empty objs list
    collector.add_field_update(field, value, [])
    assert (field, value) in collector.field_updates[User]  # Should not change anything

    # Test with another model
    user3 = User(username='user3', email='user3@example.com')
    user3.save()
    different_field = 'username'
    collector.add_field_update(different_field, 'updated_user', [user3])
    assert (different_field, 'updated_user') in collector.field_updates[User]
    assert user3 in collector.field_updates[User][(different_field, 'updated_user')]