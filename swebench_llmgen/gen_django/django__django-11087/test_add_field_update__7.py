import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_field_update_with_non_empty_objs(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')
    user1.save()
    user2.save()

    # Call the focal function
    collector.add_field_update('username', 'new_username', [user1, user2])

    # Check if field_updates is correctly populated
    assert len(collector.field_updates) == 1
    assert ('username', 'new_username') in collector.field_updates[User]
    assert {user1, user2} == collector.field_updates[User][('username', 'new_username')]

def test_add_field_update_with_empty_objs(collector):
    # Call the focal function with an empty list
    collector.add_field_update('username', 'new_username', [])

    # Check if field_updates is still empty
    assert not collector.field_updates

def test_add_field_update_with_single_user(collector):
    user = User(username='single_user')
    user.save()

    # Call the focal function
    collector.add_field_update('username', 'updated_username', [user])

    # Validate that the User instance was added
    assert len(collector.field_updates) == 1
    assert ('username', 'updated_username') in collector.field_updates[User]
    assert {user} == collector.field_updates[User][('username', 'updated_username')]