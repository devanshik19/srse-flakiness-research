import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_collect_with_fast_delete(collector):
    user = User.objects.create(username='testuser')
    collector.fast_deletes = []
    
    # Prepare a list of user objects to collect
    objs = [user]
    
    # Test fast delete
    collector.collect(objs)
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == objs

def test_collect_with_no_fast_delete(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    # Test collect without fast delete
    collector.fast_deletes = []
    collector.can_fast_delete = lambda objs: False  # Simulate no fast delete
    
    collector.collect([user1, user2])
    
    assert len(collector.fast_deletes) == 0

def test_collect_with_keep_parents(collector):
    parent_user = User.objects.create(username='parent_user')
    child_user = User.objects.create(username='child_user', username=parent_user)
    
    collector.fast_deletes = []
    
    collector.collect([child_user], keep_parents=True)
    
    assert len(collector.fast_deletes) == 0  # Parents should not be deleted

def test_collect_with_related_objects(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2', username=user1)
    
    collector.fast_deletes = []
    collector.collect([user2], collect_related=True)
    
    # Expect related user1 to not be deleted
    assert len(collector.fast_deletes) == 0  # As we don't have a real on_delete scenario

def test_collect_without_collect_related(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2', username=user1)
    
    collector.fast_deletes = []
    collector.collect([user2], collect_related=False)
    
    assert len(collector.fast_deletes) == 0  # Related shouldn't be collected

def test_collect_with_reverse_dependency(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2', username=user1)
    
    collector.fast_deletes = []
    collector.collect([user2], reverse_dependency=True)
    
    # Since it's a reverse dependency, we'd have to check the parent's handling.
    # Not easily verifiable without a full test environment but keeping logic consistent.
    
    assert len(collector.fast_deletes) == 0  # As we don't have a real on_delete scenario