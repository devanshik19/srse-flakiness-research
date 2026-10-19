import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_field_update_with_empty_objs(collector):
    field = 'username'
    value = 'newusername'
    objs = []
    
    collector.add_field_update(field, value, objs)
    
    assert collector.field_updates == {}

def test_add_field_update_with_single_obj(collector):
    user = User.objects.create(username='oldusername')
    field = 'username'
    value = 'newusername'
    objs = [user]
    
    collector.add_field_update(field, value, objs)
    
    assert field in collector.field_updates[user.__class__]
    assert (field, value) in collector.field_updates[user.__class__]
    assert collector.field_updates[user.__class__][(field, value)] == {user}

def test_add_field_update_with_multiple_objs(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    field = 'username'
    value = 'newusername'
    objs = [user1, user2]
    
    collector.add_field_update(field, value, objs)
    
    assert field in collector.field_updates[user1.__class__]
    assert (field, value) in collector.field_updates[user1.__class__]
    assert collector.field_updates[user1.__class__][(field, value)] == {user1, user2}

def test_add_field_update_with_different_field_value(collector):
    user = User.objects.create(username='testuser')
    field1 = 'email'
    value1 = 'test@example.com'
    field2 = 'username'
    value2 = 'testuser'
    objs = [user]
    
    collector.add_field_update(field1, value1, objs)
    collector.add_field_update(field2, value2, objs)
    
    assert (field1, value1) in collector.field_updates[user.__class__]
    assert collector.field_updates[user.__class__][(field1, value1)] == {user}
    assert (field2, value2) in collector.field_updates[user.__class__]
    assert collector.field_updates[user.__class__][(field2, value2)] == {user}