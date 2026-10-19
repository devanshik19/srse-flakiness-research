import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.deletion import Collector

def test_add_field_update():
    # Initialize the Collector
    collector = Collector(using='default')
    
    # Create test users
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Test with an empty list
    collector.add_field_update('email', 'new_email@example.com', [])
    assert 'User' not in collector.field_updates

    # Test with a single user
    collector.add_field_update('email', 'new_email@example.com', [user1])
    assert 'User' in collector.field_updates
    assert ('email', 'new_email@example.com') in collector.field_updates['User']
    assert {user1} == collector.field_updates['User'][('email', 'new_email@example.com')]
    
    # Test with multiple users
    collector.add_field_update('email', 'new_email@example.com', [user1, user2])
    assert {user1, user2} == collector.field_updates['User'][('email', 'new_email@example.com')]
    
    # Test adding the same field update with different value
    collector.add_field_update('email', 'another_email@example.com', [user1])
    assert ('another_email@example.com',) == tuple(collector.field_updates['User'].keys())[1]
    assert {user1} == collector.field_updates['User'][('another_email@example.com',)]

    # Ensure previous updates are unaffected
    assert {user2} == collector.field_updates['User'][('email', 'new_email@example.com')]