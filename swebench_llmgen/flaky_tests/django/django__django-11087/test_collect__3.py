import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector


@pytest.fixture
def collector():
    return Collector(using='default')


def test_collect_fast_delete(collector):
    user = User.objects.create(username='testuser')
    collector.fast_deletes = []
    
    # Call collect with a single instance where can_fast_delete is expected to be True
    collector.can_fast_delete = lambda objs, from_field=None: True
    collector.collect([user])
    
    assert len(collector.fast_deletes) == 1
    assert collector.fast_deletes[0] == [user]


def test_collect_with_related_objects(collector):
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    collector.fast_deletes = []

    collector.can_fast_delete = lambda objs, from_field=None: False
    collector.add = lambda objs, source, nullable, reverse_dependency: objs
    collector.get_del_batches = lambda objs, field: [objs]

    # Mock related objects function to mimic collecting related objects
    collector.related_objects = lambda related, objs: [obj for obj in objs]

    collector.collect([user1, user2], collect_related=True)

    # Check if the right objects were added to fast deletes
    assert len(collector.fast_deletes) == 0  # No fast deletes expected


def test_collect_no_objects(collector):
    collector.fast_deletes = []

    # Call collect with no objects
    collector.collect([], collect_related=True)

    assert len(collector.fast_deletes) == 0  # Should remain empty


def test_collect_keep_parents(collector):
    user1 = User.objects.create(username='parent_user')
    user2 = User.objects.create(username='child_user')
    
    collector.fast_deletes = []
    collector.can_fast_delete = lambda objs, from_field=None: False
    
    # Simulate add and get_del_batches
    collector.add = lambda objs, source, nullable, reverse_dependency: objs
    collector.get_del_batches = lambda objs, field: [objs]

    # Assume user1 is related as parent to user2, test `keep_parents=True`
    collector.collect([user2], keep_parents=True)
    
    assert len(collector.fast_deletes) == 0  # Parent should not be deleted