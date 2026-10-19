import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db.models.deletion import DO_NOTHING

@pytest.fixture
def user_instances():
    return [User.objects.create(username=f'user{i}') for i in range(3)]

def test_collect_fast_delete(user_instances):
    collector = Collector(using='default')
    collector.fast_deletes = []
    
    collector.collect(user_instances)
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == user_instances

def test_collect_with_parents(user_instances):
    # Create a parent User and related User instance
    parent = User.objects.create(username='parent_user')
    user_with_relation = User.objects.create(username='user_with_parent', parent=parent)
    
    collector = Collector(using='default')
    collector.fast_deletes = []
    
    collector.collect([user_with_relation], keep_parents=False)

    # Since collect_related is True by default, it should not fast delete parents.
    assert len(collector.fast_deletes) == 1  # Only user_with_parent should be fast deleted.
    assert collector.fast_deletes[0] == [user_with_relation]

def test_collect_with_keep_parents(user_instances):
    collector = Collector(using='default')
    collector.fast_deletes = []
    
    collector.collect(user_instances, keep_parents=True)
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == user_instances  # Users should still be collected.
    
def test_collect_related_objects(user_instances):
    collector = Collector(using='default')
    collector.fast_deletes = []
    
    # Assuming users might have related objects (e.g., profiles), simulate this
    collector.collect(user_instances, collect_related=True)

    # This will need actual related objects and the on_delete behavior to test correctly.
    assert len(collector.fast_deletes) == 1  # Check that it at least adds user instances.
    assert collector.fast_deletes[0] == user_instances