import pytest
from collections import Counter
from django.db import IntegrityError, transaction
from django.db.models import signals
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from unittest.mock import MagicMock


@pytest.fixture
def collector():
    return Collector(using='default')


def test_delete_single_instance(collector):
    user = User.objects.create(username='testuser')
    collector.add([user], source=None, nullable=False, reverse_dependency=None)
    
    count, deleted = collector.delete()
    
    assert count == 1
    assert deleted == {User._meta.label: 1}
    assert not User.objects.filter(pk=user.pk).exists()


def test_delete_multiple_instances(collector):
    users = User.objects.bulk_create([User(username=f'testuser{i}') for i in range(3)])
    collector.add(users, source=None, nullable=False, reverse_dependency=None)

    count, deleted = collector.delete()

    assert count == 3
    assert deleted == {User._meta.label: 3}
    for user in users:
        assert not User.objects.filter(pk=user.pk).exists()


def test_delete_with_field_updates(collector):
    user1 = User.objects.create(username='testuser1', first_name='OldName')
    user2 = User.objects.create(username='testuser2', first_name='OldName')
    collector.add([user1, user2], source=None, nullable=False, reverse_dependency=None)
    collector.add_field_update('first_name', 'NewName', [user1])
    collector.add_field_update('first_name', 'NewName', [user2])

    count, deleted = collector.delete()

    assert count == 2
    assert deleted == {User._meta.label: 2}
    assert User.objects.filter(pk=user1.pk).exists()
    assert user1.first_name == 'NewName'
    assert user2.first_name == 'NewName'

    assert not User.objects.filter(pk=user1.pk).exists()
    assert not User.objects.filter(pk=user2.pk).exists()


def test_delete_with_signals(collector, monkeypatch):
    pre_delete_signal_called = False
    post_delete_signal_called = False

    def pre_delete(sender, instance, **kwargs):
        nonlocal pre_delete_signal_called
        pre_delete_signal_called = True

    def post_delete(sender, instance, **kwargs):
        nonlocal post_delete_signal_called
        post_delete_signal_called = True

    signals.pre_delete.connect(pre_delete)
    signals.post_delete.connect(post_delete)

    user = User.objects.create(username='testuser')
    collector.add([user], source=None, nullable=False, reverse_dependency=None)

    collector.delete()

    assert pre_delete_signal_called
    assert post_delete_signal_called
    assert not User.objects.filter(pk=user.pk).exists()


def test_delete_with_fast_delete(collector):
    user = User.objects.create(username='testuser')
    collector.add([user], source=None, nullable=False, reverse_dependency=None)

    collector.can_fast_delete = MagicMock(return_value=True)

    count, deleted = collector.delete()

    assert count == 1
    assert deleted == {User._meta.label: 1}
    assert not User.objects.filter(pk=user.pk).exists()