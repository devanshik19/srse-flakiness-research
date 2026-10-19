import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_with_non_empty_objs():
    collector = Collector(using='default')
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User(username='user3')  # Not saved to DB

    result = collector.add([user1, user2, user3])
    
    assert result == [user1, user2, user3]  # user1 and user2 are new, user3 is not saved
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]
    
def test_add_with_empty_objs():
    collector = Collector(using='default')
    result = collector.add([])
    
    assert result == []  # Should return an empty list

def test_add_with_already_collected_objs():
    collector = Collector(using='default')
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    collector.add([user1, user2])  # First addition
    result = collector.add([user1])  # Adding user1 again
    
    assert result == []  # user1 was already collected
    assert len(collector.data[User]) == 2  # Only user1 and user2 should be collected

def test_add_with_source_and_nullable_false():
    collector = Collector(using='default')
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    result = collector.add([user1, user2], source=user1, nullable=False)
    
    assert result == [user1, user2]
    assert user2 in collector.dependencies[user1._meta.concrete_model]
    
def test_add_with_reverse_dependency():
    collector = Collector(using='default')
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    result = collector.add([user1], source=user2, nullable=False, reverse_dependency=True)
    
    assert result == [user1]
    assert user1 in collector.dependencies[user2._meta.concrete_model]