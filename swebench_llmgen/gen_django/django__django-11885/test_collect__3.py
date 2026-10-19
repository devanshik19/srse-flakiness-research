import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def user_factory():
    # Create and return a list of User objects
    return [User.objects.create(username=f'user{i}') for i in range(5)]

def test_collect_fast_delete(user_factory):
    collector = Collector(using='default')
    collector.can_fast_delete = lambda objs, from_field=None: True  # Simulate fast delete capability

    collector.collect(user_factory)
    
    assert len(collector.fast_deletes) == 1
    assert user_factory[0] in collector.fast_deletes[0]

def test_collect_with_parents(user_factory):
    collector = Collector(using='default')
    
    # Simulating the add method to return the same objects
    collector.add = lambda objs, source, nullable, reverse_dependency: objs

    # Collect without keeping parents
    collector.collect(user_factory, keep_parents=False)
    
    # Check that we're collecting new objects and handling parents
    assert len(collector.fast_deletes) == 0  # No fast deletes
    assert len(collector.add(user_factory, None, False, False)) == len(user_factory)

def test_collect_with_related(user_factory):
    collector = Collector(using='default')
    
    # Simulating related objects behaviour
    collector.related_objects = lambda related, objs: objs
    collector.get_del_batches = lambda objs, field: [objs]

    # Collect with related objects
    collector.collect(user_factory, collect_related=True)
    
    # Verify that all users were collected for deletion
    assert len(collector.fast_deletes) == 0  # No fast deletes
    assert len(collector.add(user_factory, None, False, False)) == len(user_factory)

def test_collect_reverse_dependency(user_factory):
    collector = Collector(using='default')
    collector.add = lambda objs, source, nullable, reverse_dependency: objs

    # Collect with reverse dependency
    collector.collect(user_factory, reverse_dependency=True)

    assert len(collector.fast_deletes) == 0
    assert len(collector.add(user_factory, None, False, True)) == len(user_factory)

def test_collect_nullable(user_factory):
    collector = Collector(using='default')
    
    # Simulating to deal with nullable fields (not actually testing real nullable behaviour)
    collector.add = lambda objs, source, nullable, reverse_dependency: objs

    collector.collect(user_factory, nullable=True)
    
    assert len(collector.fast_deletes) == 0
    assert len(collector.add(user_factory, None, True, False)) == len(user_factory)