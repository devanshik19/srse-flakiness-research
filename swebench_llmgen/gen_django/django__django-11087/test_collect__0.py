import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def user_instances():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    return [user1, user2]

def test_collect_fast_delete(user_instances):
    collector = Collector(using='default')
    collector.fast_deletes = []
    
    # Simulating a condition where fast_delete can be used
    assert collector.can_fast_delete(user_instances)
    
    collector.collect(user_instances)
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == user_instances

def test_collect_with_parents(user_instances):
    collector = Collector(using='default')
    collector.fast_deletes = []
    
    # Testing collect without keeping parents
    collector.collect(user_instances, keep_parents=False)
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == user_instances

def test_collect_with_keep_parents(user_instances):
    collector = Collector(using='default')
    collector.fast_deletes = []
    
    # Testing collect with keeping parents
    collector.collect(user_instances, keep_parents=True)
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == user_instances

def test_collect_reverse_dependency(user_instances):
    collector = Collector(using='default')
    collector.fast_deletes = []
    
    # Here, we test with reverse dependencies
    collector.collect(user_instances, reverse_dependency=True)
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == user_instances

def test_collect_nullable(user_instances):
    collector = Collector(using='default')
    collector.fast_deletes = []

    # Collecting with nullable set to True, there are 'no' model dependencies here
    collector.collect(user_instances, nullable=True)
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == user_instances