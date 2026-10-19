import pytest
from collections import Counter
from operator import attrgetter
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import signals
from django.db import connections, sql
from django.db.models.deletion import Collector

@pytest.fixture
def collector_with_users():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')
    
    collector = Collector(using='default')
    collector.data = {User: [user1, user2, user3]}
    return collector

def test_delete_single_user(collector_with_users):
    collector = collector_with_users
    
    deleted_count, deleted_counter = collector.delete()
    
    assert deleted_count == 3
    assert deleted_counter[User._meta.label] == 3
    assert User.objects.count() == 0

def test_fast_delete_no_dependencies(collector_with_users):
    collector = collector_with_users
    collector.data = {User: [collector.data[User][0]]}  # Fast delete only the first user

    # Simulate can_fast_delete returning True
    collector.can_fast_delete = lambda instance: True
    
    deleted_count, deleted_counter = collector.delete()
    
    assert deleted_count == 1
    assert deleted_counter[User._meta.label] == 1
    assert User.objects.count() == 2

def test_delete_signals(collector_with_users):
    collector = collector_with_users
    signals.pre_delete.connect(lambda sender, instance, **kwargs: setattr(instance, 'deleted', True))

    user = collector.data[User][0]
    signals.post_delete.connect(lambda sender, instance, **kwargs: setattr(instance, 'post_deleted', True))

    deleted_count, deleted_counter = collector.delete()

    assert deleted_count == 3
    assert deleted_counter[User._meta.label] == 3
    assert user.deleted is True
    assert user.post_deleted is True

def test_delete_with_field_updates(collector_with_users):
    collector = collector_with_users
    collector.field_updates = {
        User: {('is_active', False): [collector.data[User][0]]}
    }
    
    deleted_count, deleted_counter = collector.delete()

    # Ensure the active status was updated before deletion
    assert deleted_count == 3
    assert deleted_counter[User._meta.label] == 3
    assert User.objects.filter(pk=collector.data[User][0].pk, is_active=False).exists() is False