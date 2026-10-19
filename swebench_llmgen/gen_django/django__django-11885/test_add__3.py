import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_with_no_objects(collector):
    result = collector.add(objs=[])
    assert result == []

def test_add_single_object(collector):
    user = User(username='testuser')
    user.save()
    result = collector.add(objs=[user])
    assert result == [user]
    assert user in collector.data[User]

def test_add_multiple_objects(collector):
    user1 = User(username='testuser1')
    user2 = User(username='testuser2')
    user1.save()
    user2.save()
    result = collector.add(objs=[user1, user2])
    assert set(result) == {user1, user2}
    assert user1 in collector.data[User]
    assert user2 in collector.data[User]

def test_add_duplicates(collector):
    user1 = User(username='testuser1')
    user1.save()
    collector.add(objs=[user1])
    
    result = collector.add(objs=[user1])
    assert result == []  # No new objects added
    assert user1 in collector.data[User]

def test_add_with_source_and_nullable_false(collector):
    user1 = User(username='testuser1')
    user2 = User(username='testuser2')
    user1.save()
    user2.save()
    
    result = collector.add(objs=[user1], source=user2, nullable=False)
    assert set(result) == {user1}
    assert user1 in collector.data[User]
    assert user2 in collector.dependencies[user2._meta.concrete_model]

def test_add_with_reverse_dependency(collector):
    user1 = User(username='testuser1')
    user2 = User(username='testuser2')
    user1.save()
    user2.save()
    
    result = collector.add(objs=[user1], source=user2, nullable=False, reverse_dependency=True)
    assert set(result) == {user1}
    assert user1 in collector.data[User]
    assert user2 in collector.dependencies[user1._meta.concrete_model]