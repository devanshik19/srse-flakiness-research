import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_field_update_empty_objs(collector):
    initial_field_updates = collector.field_updates.copy()
    collector.add_field_update(field='username', value='new_username', objs=[])
    assert collector.field_updates == initial_field_updates

def test_add_field_update_single_instance(collector):
    user = User.objects.create(username='user1')
    collector.add_field_update(field='username', value='new_username', objs=[user])
    assert (user.__class__, ('username', 'new_username')) in collector.field_updates
    assert collector.field_updates[user.__class__][('username', 'new_username')] == {user}

def test_add_field_update_multiple_instances(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    collector.add_field_update(field='username', value='new_username', objs=[user1, user2])
    
    assert (user1.__class__, ('username', 'new_username')) in collector.field_updates
    assert collector.field_updates[user1.__class__][('username', 'new_username')] == {user1, user2}

def test_add_field_update_different_values(collector):
    user = User.objects.create(username='user1')
    collector.add_field_update(field='username', value='new_username', objs=[user])
    collector.add_field_update(field='username', value='another_username', objs=[user])

    assert len(collector.field_updates[user.__class__]) == 2
    assert (user.__class__, ('username', 'new_username')) in collector.field_updates
    assert (user.__class__, ('username', 'another_username')) in collector.field_updates
    assert collector.field_updates[user.__class__][('username', 'new_username')] == {user}
    assert collector.field_updates[user.__class__][('username', 'another_username')] == {user}