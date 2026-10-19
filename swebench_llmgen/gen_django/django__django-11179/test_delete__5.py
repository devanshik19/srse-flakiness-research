import pytest
from collections import Counter
from operator import attrgetter
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import signals, sql
from django.db.models.deletion import Collector

@pytest.fixture
def user_data():
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    return user1, user2

def test_delete_single_instance(user_data):
    user1, _ = user_data
    collector = Collector(using='default')
    collector.add([user1], "user", nullable=False, reverse_dependency=None)

    count, deleted = collector.delete()
    
    assert count == 1
    assert User.objects.count() == 1
    assert deleted == {User._meta.label: 1}

def test_delete_multiple_instances(user_data):
    user1, user2 = user_data
    collector = Collector(using='default')
    collector.add([user1, user2], "user", nullable=False, reverse_dependency=None)

    count, deleted = collector.delete()

    assert count == 2
    assert User.objects.count() == 0
    assert deleted == {User._meta.label: 2}

def test_delete_with_field_updates(user_data):
    user1, user2 = user_data
    collector = Collector(using='default')
    collector.add([user1, user2], "user", nullable=False, reverse_dependency=None)
    collector.add_field_update('is_active', False, [user1, user2])

    count, deleted = collector.delete()

    assert count == 2
    assert User.objects.count() == 0
    assert deleted == {User._meta.label: 2}
    assert not User.objects.filter(username='testuser1').exists()
    assert not User.objects.filter(username='testuser2').exists()

def test_delete_with_fast_delete(user_data):
    user1, _ = user_data
    collector = Collector(using='default')
    collector.add([user1], "user", nullable=False, reverse_dependency=None)

    # Assume can_fast_delete returns True for this test
    collector.can_fast_delete = lambda x: True

    count, deleted = collector.delete()

    assert count == 1
    assert User.objects.count() == 0
    assert deleted == {User._meta.label: 1}