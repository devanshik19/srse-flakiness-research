import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_new_objects(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    added = collector.add([user1, user2])
    assert added == [user1, user2]
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]

def test_add_existing_objects(collector):
    user1 = User.objects.create(username='user1')
    collector.add([user1])
    added = collector.add([user1])
    assert added == []
    assert len(collector.data[User]) == 1

def test_add_with_source(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    added = collector.add([user1, user2], source=user1.__class__)
    assert added == [user1, user2]
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]

def test_add_with_nullable(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    added = collector.add([user1, user2], source=user1.__class__, nullable=True)
    assert added == [user1, user2]
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]

def test_add_with_reverse_dependency(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    added = collector.add([user1], source=user2, reverse_dependency=True)
    assert added == [user1]
    assert user1 in collector.data[User]
    assert user2 in collector.dependencies

def test_add_empty_list(collector):
    added = collector.add([])
    assert added == []
    assert len(collector.data) == 0