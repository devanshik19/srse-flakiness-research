import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_new_objects(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')
    new_objs = collector.add([user1, user2])
    assert new_objs == [user1, user2]

def test_add_existing_object(collector):
    user1 = User(username='user1')
    collector.add([user1])
    new_objs = collector.add([user1])
    assert new_objs == []

def test_add_nullable_relationship(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')
    collector.add([user1])
    new_objs = collector.add([user2], source=user1, nullable=True)
    assert new_objs == [user2]

def test_add_non_nullable_relationship(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')
    collector.add([user1])
    new_objs = collector.add([user2], source=user1, nullable=False)
    assert new_objs == [user2]

def test_add_reverse_dependency(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')
    collector.add([user1])
    new_objs = collector.add([user2], source=user1, nullable=False, reverse_dependency=True)
    assert new_objs == [user2]
    
def test_add_multiple_objects(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')
    user3 = User(username='user3')
    new_objs = collector.add([user1, user2, user3])
    assert new_objs == [user1, user2, user3]