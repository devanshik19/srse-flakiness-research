import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update():
    # Create a Collector instance
    collector = Collector(using='default')

    # Create a list of User instances
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    user3 = User.objects.create(username='user3', email='user3@example.com')

    # Test with a homogeneous iterable of User instances
    objs = [user1, user2, user3]
    
    # Add field update for the 'email' field
    collector.add_field_update('email', 'new_email@example.com', objs)

    # Verify that the field_updates are correctly set
    assert len(collector.field_updates) == 1
    assert ('email', 'new_email@example.com') in collector.field_updates[User]
    assert objs[0] in collector.field_updates[User][('email', 'new_email@example.com')]
    assert objs[1] in collector.field_updates[User][('email', 'new_email@example.com')]
    assert objs[2] in collector.field_updates[User][('email', 'new_email@example.com')]

    # Test when objs is empty
    collector.add_field_update('email', 'another_email@example.com', [])
    
    # Verify that no updates were added for empty objs
    assert len(collector.field_updates) == 1