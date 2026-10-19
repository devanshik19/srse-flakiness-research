import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_with_new_objects():
    collector = Collector(using='default')
    user1 = User(username='user1')
    user2 = User(username='user2')
    
    # Simulate the collection of new users
    new_users = collector.add([user1, user2])
    
    assert new_users == [user1, user2]
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]

def test_add_with_existing_objects():
    collector = Collector(using='default')
    user1 = User(username='user1')
    user2 = User(username='user2')
    
    collector.add([user1])
    new_users = collector.add([user1, user2])
    
    assert new_users == [user2]
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]

def test_add_with_nullable_relationship():
    collector = Collector(using='default')
    user1 = User(username='user1')
    
    # Add object without source and nullable being False
    new_users = collector.add([user1], source=None, nullable=True)
    
    assert new_users == [user1]
    assert user1 in collector.data[User]

def test_add_with_source_and_reverse_dependency():
    collector = Collector(using='default')
    user1 = User(username='user1')
    user2 = User(username='user2')
    user3 = User(username='user3')  # This acts as a different source

    collector.add([user1], source=user3, nullable=False, reverse_dependency=True)

    assert user1 in collector.data[User]
    assert user3._meta.concrete_model in collector.dependencies
    assert User._meta.concrete_model in collector.dependencies[user3._meta.concrete_model]

def test_add_with_empty_input():
    collector = Collector(using='default')
    
    new_users = collector.add([])
    
    assert new_users == []