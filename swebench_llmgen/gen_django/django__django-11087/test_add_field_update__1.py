import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.mark.django_db
def test_add_field_update():
    # Create instances of User
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    user3 = User.objects.create(username='user3', email='user3@example.com')

    # Create an instance of the Collector class
    collector = Collector(using='default')

    # Test case 1: Adding field update with valid objects
    collector.add_field_update('email', 'new_email@example.com', [user1, user2])
    assert 'auth.User' in collector.field_updates
    assert ('email', 'new_email@example.com') in collector.field_updates['auth.User']
    assert {user1, user2} == collector.field_updates['auth.User'][('email', 'new_email@example.com')]

    # Test case 2: Adding field update with the same value, should not duplicate
    collector.add_field_update('email', 'new_email@example.com', [user3])
    assert {user1, user2, user3} == collector.field_updates['auth.User'][('email', 'new_email@example.com')]

    # Test case 3: Adding field update with an empty list
    collector.add_field_update('email', 'another_email@example.com', [])
    assert len(collector.field_updates['auth.User']) == 2  # Should remain unchanged

    # Test case 4: Adding field update with a different field
    collector.add_field_update('username', 'new_username', [user1])
    assert 'auth.User' in collector.field_updates
    assert ('username', 'new_username') in collector.field_updates['auth.User']
    assert {user1} == collector.field_updates['auth.User'][('username', 'new_username')]