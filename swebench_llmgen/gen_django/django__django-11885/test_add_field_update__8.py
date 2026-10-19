import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update():
    collector = Collector(using='default')
    
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Test with a non-empty iterable
    collector.add_field_update('email', 'new_email@example.com', [user1, user2])
    assert (user1, 'new_email@example.com') in collector.field_updates[User][('email', 'new_email@example.com')]
    assert (user2, 'new_email@example.com') in collector.field_updates[User][('email', 'new_email@example.com')]
    
    # Test with an empty iterable
    collector.add_field_update('email', 'another_email@example.com', [])
    assert len(collector.field_updates) == 1  # Should still have the previous entry
    
    # Ensure no new entries added for empty objs
    assert len(collector.field_updates[User][('email', 'new_email@example.com')]) == 2