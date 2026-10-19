import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def user_instances():
    return [User.objects.create(username=f'user{i}') for i in range(3)]

def test_add_field_update_empty_objs():
    collector = Collector(using='default')
    collector.add_field_update('email', 'test@example.com', [])
    assert collector.field_updates == {}

def test_add_field_update_valid_objs(user_instances):
    collector = Collector(using='default')
    collector.add_field_update('email', 'test@example.com', user_instances)

    assert len(collector.field_updates) == 1
    assert (('email', 'test@example.com') in collector.field_updates[User])
    assert len(collector.field_updates[User][('email', 'test@example.com')]) == 3
    assert all(user in collector.field_updates[User][('email', 'test@example.com')] for user in user_instances)

def test_add_field_update_different_values(user_instances):
    collector = Collector(using='default')
    collector.add_field_update('email', 'test1@example.com', user_instances)
    collector.add_field_update('email', 'test2@example.com', user_instances)

    assert len(collector.field_updates) == 1
    assert len(collector.field_updates[User]) == 2
    assert (('email', 'test1@example.com') in collector.field_updates[User])
    assert (('email', 'test2@example.com') in collector.field_updates[User])
    assert len(collector.field_updates[User][('email', 'test1@example.com')]) == 3
    assert len(collector.field_updates[User][('email', 'test2@example.com')]) == 3

def test_add_field_update_homogeneous_iterable(user_instances):
    collector = Collector(using='default')
    collector.add_field_update('email', 'test@example.com', user_instances)

    assert ('email', 'test@example.com') in collector.field_updates[User]
    assert len(collector.field_updates[User][('email', 'test@example.com')]) == 3