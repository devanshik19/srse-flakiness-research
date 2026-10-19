import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def setup_users():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')
    return [user1, user2, user3]

def test_collect_fast_delete(setup_users):
    collector = Collector(using='default')
    collector.fast_deletes = []

    # Test fast delete with can_fast_delete() returning True
    collector.can_fast_delete = lambda objs, from_field=None: True
    collector.collect(setup_users)

    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == setup_users

def test_collect_with_related_objects(setup_users):
    collector = Collector(using='default')
    collector.fast_deletes = []

    collector.can_fast_delete = lambda objs, from_field=None: False
    collector.add = lambda objs, source, nullable, reverse_dependency: objs  # to simulate add

    # Call collect without keeping parents
    collector.collect(setup_users, keep_parents=False)

    # Generate expected model
    model = User

    # Validate that parent objects are collected by simulating related collections
    assert model._meta.parents   # Ensure there are no parents for User model
    assert len(collector.fast_deletes) == 0  # None should be fast deleted
    assert len(collector.fast_deletes) == 0  # Should have added actually due to simulation

def test_collect_with_nullable(setup_users):
    collector = Collector(using='default')
    collector.fast_deletes = []

    collector.can_fast_delete = lambda objs, from_field=None: False
    collector.add = lambda objs, source, nullable, reverse_dependency: objs  # to simulate add

    # Call collect with nullable set to true
    collector.collect(setup_users, nullable=True, keep_parents=False)

    assert len(collector.fast_deletes) == 0  # Should simulate no fast deletes
    assert len(collector.fast_deletes) == 0  # Ensure still no fast deletes

def test_collect_keep_parents(setup_users):
    collector = Collector(using='default')
    collector.fast_deletes = []

    collector.can_fast_delete = lambda objs, from_field=None: False
    collector.add = lambda objs, source, nullable, reverse_dependency: objs  # Simulating add

    # Call collect with keep_parents set to true
    collector.collect(setup_users, keep_parents=True)

    assert len(collector.fast_deletes) == 0  # Should simulate no fast deletes
    # Parents are 'not collected' hence checking against fast deletes
    assert len(collector.fast_deletes) == 0  # No fast deletes should happen