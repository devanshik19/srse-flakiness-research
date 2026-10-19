import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_no_objects(collector):
    result = collector.add([])
    assert result == []

def test_add_single_object(collector):
    user = User(username='testuser')
    result = collector.add([user])
    assert result == [user]
    assert user in collector.data[User]

def test_add_multiple_new_objects(collector):
    user1 = User(username='testuser1')
    user2 = User(username='testuser2')
    result = collector.add([user1, user2])
    assert result == [user1, user2]
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]

def test_add_existing_object(collector):
    user = User(username='testuser')
    collector.add([user])
    result = collector.add([user])
    assert result == []
    assert len(collector.data[User]) == 1

def test_add_source_dependency(collector):
    user1 = User(username='testuser1')
    user2 = User(username='testuser2')
    collector.add([user1], source=user2, nullable=False)
    assert user1 in collector.dependencies[user2.__class__]
    assert user2.__class__ in collector.dependencies[User]

def test_add_reverse_dependency(collector):
    user1 = User(username='testuser1')
    user2 = User(username='testuser2')
    collector.add([user1], source=user2, nullable=False, reverse_dependency=True)
    assert user2.__class__ in collector.dependencies[user1.__class__]
    assert user1.__class__ in collector.dependencies[User]