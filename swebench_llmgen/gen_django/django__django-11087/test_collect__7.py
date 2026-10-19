import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db.models import DO_NOTHING

@pytest.fixture
def collector():
    return Collector(using='default')

def test_collect_fast_delete(collector):
    user = User.objects.create(username='testuser')
    collector.fast_deletes = []
    
    # Test fast delete
    collector.collect([user])
    assert len(collector.fast_deletes) == 1
    assert user in collector.fast_deletes[0]

def test_collect_adds_objects(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    # Test that objects are added
    collector.collect([user1, user2])
    assert len(collector.fast_deletes) == 0

def test_collect_with_keep_parents(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    parent_user = User.objects.create(username='parent_user')
    user1.profile.parent = parent_user
    user1.profile.save()
    
    collector.collect([user1], keep_parents=True)
    assert len(collector.fast_deletes) == 0

def test_collect_with_reverse_dependency(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    # Assuming a relation exists, we test with reverse dependency
    collector.collect([user1, user2], reverse_dependency=True)
    
    # Check behavior of reverse dependency (dummy since relation not defined)
    assert len(collector.fast_deletes) == 0  # no actual association in this test

def test_collect_with_nullable(collector):
    user1 = User.objects.create(username='user1')
    
    # Test with nullable
    collector.collect([user1], nullable=True)
    assert len(collector.fast_deletes) == 0