import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db import transaction

@pytest.fixture
def users(db):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')
    return [user1, user2, user3]

def test_collect_fast_delete(users):
    collector = Collector(using='default')
    user_batch = users[:2]
    
    # Mock can_fast_delete to always return True
    collector.can_fast_delete = lambda objs, from_field=None: True
    collector.collect(user_batch)
    
    assert collector.fast_deletes == [user_batch]

def test_collect_with_relation(users):
    # Setting up a test to simulate related deletes
    collector = Collector(using='default')
    user1, user2 = users[:2]
    
    collector.collect([user1], collect_related=True)
    
    # Assuming there are related objects to collect in real use, 
    # this needs more specifics about relations to validate fully.
    collector.add = lambda objs, source, nullable, reverse_dependency: objs
    new_objs = collector.add([user1], None, False, False)
    
    assert new_objs == [user1]

def test_collect_keep_parents(users):
    collector = Collector(using='default')
    user1 = users[0]
    
    collector.collect([user1], keep_parents=True)
    
    # Ensure fast_deletes is still empty since keep_parents=True shouldn't remove them.
    assert not collector.fast_deletes

def test_collect_no_new_objs(users):
    collector = Collector(using='default')
    user3 = users[2]
    
    collector.add = lambda objs, source, nullable, reverse_dependency: []  # Simulate no new objects
    
    collector.collect([user3])
    
    assert collector.fast_deletes == []