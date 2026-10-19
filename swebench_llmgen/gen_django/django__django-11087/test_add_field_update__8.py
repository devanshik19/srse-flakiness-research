import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture()
def user_instances():
    return [User(username=f"user{i}") for i in range(3)]

def test_add_field_update_with_no_objects():
    collector = Collector(using='default')
    initial_field_updates = collector.field_updates.copy()
    
    collector.add_field_update(field='email', value='test@example.com', objs=[])
    
    assert collector.field_updates == initial_field_updates

def test_add_field_update_with_homogeneous_objects(user_instances):
    collector = Collector(using='default')
    for user in user_instances:
        user.save()  # Save to create database instances

    collector.add_field_update(field='email', value='test@example.com', objs=user_instances)

    assert len(collector.field_updates) == 1
    assert ('email', 'test@example.com') in collector.field_updates[User]
    assert len(collector.field_updates[User][('email', 'test@example.com')]) == 3
    assert all(user in collector.field_updates[User][('email', 'test@example.com')] for user in user_instances)

def test_add_field_update_with_different_field_value(user_instances):
    collector = Collector(using='default')
    for user in user_instances:
        user.save()  # Save to create database instances

    collector.add_field_update(field='email', value='first@example.com', objs=[user_instances[0]])
    collector.add_field_update(field='email', value='second@example.com', objs=[user_instances[1]])

    assert len(collector.field_updates) == 1
    assert ('email', 'first@example.com') in collector.field_updates[User]
    assert ('email', 'second@example.com') in collector.field_updates[User]
    assert len(collector.field_updates[User][('email', 'first@example.com')]) == 1
    assert len(collector.field_updates[User][('email', 'second@example.com')]) == 1