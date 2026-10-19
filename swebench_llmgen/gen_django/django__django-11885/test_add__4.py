import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_new_objects(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')
    user3 = User(username='user3')

    # Add first user
    new_objects = collector.add([user1])
    assert new_objects == [user1]
    
    # Add second user
    new_objects = collector.add([user2])
    assert new_objects == [user2]
    
    # Attempt to add the same user again
    new_objects = collector.add([user1])
    assert new_objects == []

def test_add_no_objects(collector):
    new_objects = collector.add([])
    assert new_objects == []

def test_add_with_source(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')

    # Add user1 with a source and nullable set to False
    new_objects = collector.add([user1], source=user2, nullable=False)
    assert new_objects == [user1]
    
    # Verify dependencies
    assert user2._meta.concrete_model in collector.dependencies
    assert user1._meta.concrete_model in collector.dependencies[user2._meta.concrete_model]

def test_add_with_reverse_dependency(collector):
    user1 = User(username='user1')
    user2 = User(username='user2')

    # Add user1 with a source and reverse dependency set to True
    new_objects = collector.add([user1], source=user2, nullable=False, reverse_dependency=True)
    assert new_objects == [user1]
    
    # Verify dependencies
    assert user1._meta.concrete_model in collector.dependencies
    assert user2._meta.concrete_model in collector.dependencies[user1._meta.concrete_model]