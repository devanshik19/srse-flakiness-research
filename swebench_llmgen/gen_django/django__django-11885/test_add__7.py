import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_new_objects(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    new_objs = collector.add([user1, user2])
    assert new_objs == [user1, user2]
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]

def test_add_existing_object(collector):
    user1 = User.objects.create(username='user1')
    
    collector.add([user1])
    new_objs = collector.add([user1])
    assert new_objs == []
    assert len(collector.data[User]) == 1

def test_add_objects_with_source(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    new_objs = collector.add([user1], source=user2)
    assert new_objs == [user1]
    assert user1 in collector.data[User]
    assert user2 not in collector.data[User]

def test_add_objects_with_nullable_false(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    collector.add([user1], source=user2, nullable=False)
    assert user1 in collector.data[User]
    assert user2 not in collector.data[User]

def test_add_objects_with_reverse_dependency(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    collector.add([user1], source=user2, nullable=False, reverse_dependency=True)
    assert user1 in collector.data[User]
    assert user2 not in collector.data[User]
    assert user2 in collector.dependencies
    assert User in collector.dependencies[user2._meta.concrete_model]