import pytest
from collections import Counter
from operator import attrgetter
from django.db import IntegrityError, transaction
from django.db.models import signals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    collector_instance = Collector(using='default')
    return collector_instance

def test_delete_single_instance(collector):
    user = User.objects.create(username='testuser')
    collector.add([user], 'source', nullable=False, reverse_dependency=None)
    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter[User._meta.label] == 1
    assert User.objects.filter(pk=user.pk).count() == 0

def test_delete_multiple_instances(collector):
    users = [User.objects.create(username=f'testuser{i}') for i in range(3)]
    collector.add(users, 'source', nullable=False, reverse_dependency=None)
    count, deleted_counter = collector.delete()

    assert count == 3
    assert deleted_counter[User._meta.label] == 3
    assert User.objects.filter(pk__in=[user.pk for user in users]).count() == 0

def test_delete_with_field_updates(collector):
    user = User.objects.create(username='testuser', is_active=True)
    collector.add([user], 'source', nullable=False, reverse_dependency=None)
    collector.add_field_update('is_active', False, [user])
    
    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter[User._meta.label] == 1
    assert User.objects.filter(pk=user.pk).count() == 0

def test_fast_delete(collector):
    user = User.objects.create(username='testuser')
    collector.add([user], 'source', nullable=False, reverse_dependency=None)

    # Simulating a condition that allows fast delete
    collector.can_fast_delete = lambda x: True
    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter[User._meta.label] == 1
    assert User.objects.filter(pk=user.pk).count() == 0

def test_delete_with_pre_post_signals(collector, monkeypatch):
    pre_delete_called = []

    def pre_delete(sender, instance, using, **kwargs):
        pre_delete_called.append(instance)

    signals.pre_delete.connect(pre_delete)
    
    post_delete_called = []

    def post_delete(sender, instance, using, **kwargs):
        post_delete_called.append(instance)

    signals.post_delete.connect(post_delete)

    user = User.objects.create(username='testuser')
    collector.add([user], 'source', nullable=False, reverse_dependency=None)

    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter[User._meta.label] == 1
    assert pre_delete_called == [user]
    assert post_delete_called == [user]
    assert User.objects.filter(pk=user.pk).count() == 0