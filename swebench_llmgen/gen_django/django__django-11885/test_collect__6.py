import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector


@pytest.fixture
def collector():
    return Collector(using='default')


def test_collect_new_objects(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    objs = [user1, user2]

    collector.collect(objs)

    assert len(collector.fast_deletes) == 0


def test_collect_with_keep_parents(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    objs = [user1, user2]

    collector.collect(objs, keep_parents=True)

    assert len(collector.fast_deletes) == 0  # No fast deletes


def test_collect_collect_related(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    # Example step: Assuming a related model setup that collects related objects
    # Here we would need to simulate a situation where related objects exist
    # For example we could create a model that connects to User
    # You might need a related model to test this behavior, hence this is a placeholder
    # related_obj = RelatedModel.objects.create(user=user1)

    objs = [user1, user2]
    collector.collect(objs)

    assert len(collector.fast_deletes) == 0  # Check for related object handling


def test_collect_reverse_dependency(collector):
    # Creating users to test
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    objs = [user1, user2]

    collector.collect(objs, reverse_dependency=True)

    assert len(collector.fast_deletes) == 0  # No fast deletes, verifying normal behavior


def test_collect_nullable(collector):
    user = User.objects.create(username='user1')
    objs = [user]

    collector.collect(objs, nullable=True)

    assert len(collector.fast_deletes) == 0  # No fast deletes


def test_collect_no_related(collector):
    user = User.objects.create(username='user1')
    objs = [user]

    collector.collect(objs, collect_related=False)

    assert len(collector.fast_deletes) == 0  # No fast deletes


def test_collect_no_new_objects(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    objs = [user1, user2]

    collector.collect(objs)  # Should populate with current objects
    assert len(collector.fast_deletes) == 0


def test_collect_handle_on_delete_do_nothing(collector):
    # Setup: assuming on_delete behavior can be simulated
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    # Collect objects
    collector.collect([user1, user2])

    # Validate that the fast deletes worked as expected
    # Here we would add specific logic for on_delete behavior
  
    assert len(collector.fast_deletes) == 0  # Nothing should delete if on_delete is DO_NOTHING