import pytest
from collections import Counter
from operator import attrgetter
from django.db import IntegrityError, transaction
from django.db.models import signals
from django.contrib.auth.models import User
from django.db.models.deletion import Collector


@pytest.fixture
def collector() -> Collector:
    return Collector(using='default')


def test_delete_single_instance_no_dependencies(collector):
    user = User.objects.create(username='testuser')
    collector.add([user], source=None, nullable=False, reverse_dependency=False)

    # Perform delete
    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter == {User._meta.label: 1}
    assert User.objects.filter(pk=user.pk).count() == 0


def test_delete_multiple_instances(collector):
    users = [User.objects.create(username=f'user{i}') for i in range(5)]
    collector.add(users, source=None, nullable=False, reverse_dependency=False)

    # Perform delete
    count, deleted_counter = collector.delete()

    assert count == 5
    assert deleted_counter == {User._meta.label: 5}
    for user in users:
        assert User.objects.filter(pk=user.pk).count() == 0


def test_delete_with_field_updates(collector):
    user1 = User.objects.create(username='user1', is_active=True)
    user2 = User.objects.create(username='user2', is_active=True)
    collector.add([user1, user2], source=None, nullable=False, reverse_dependency=False)

    # Update field for one object
    collector.add_field_update('is_active', False, [user1])

    # Perform delete
    count, deleted_counter = collector.delete()

    assert count == 2
    assert deleted_counter == {User._meta.label: 2}
    assert User.objects.filter(pk=user1.pk).count() == 0
    assert User.objects.filter(pk=user2.pk).count() == 0
    
    # Verifying updates affected the instance
    user1.refresh_from_db()
    assert user1.is_active is False


def test_delete_with_fast_delete(collector):
    user = User.objects.create(username='fastdeleteuser')
    collector.add([user], source=None, nullable=False, reverse_dependency=False)

    # Mock fast delete capability
    collector.can_fast_delete = lambda obj: True

    # Perform delete
    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter == {User._meta.label: 1}
    assert User.objects.filter(pk=user.pk).count() == 0