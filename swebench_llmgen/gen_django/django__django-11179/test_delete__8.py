import pytest
from collections import Counter
from operator import attrgetter
from django.db import IntegrityError, connections, transaction
from django.db.models import signals
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import Collector

@pytest.fixture
def user_instance():
    return User.objects.create(username='testuser', password='password')

def test_delete_single_instance(user_instance):
    collector = Collector(using='default')
    collector.add([user_instance], None, None, False)
    
    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter[User._meta.label] == 1
    with pytest.raises(ObjectDoesNotExist):
        User.objects.get(pk=user_instance.pk)

def test_delete_multiple_instances(user_instance):
    user_instance2 = User.objects.create(username='testuser2', password='password')
    collector = Collector(using='default')
    collector.add([user_instance, user_instance2], None, None, False)

    count, deleted_counter = collector.delete()

    assert count == 2
    assert deleted_counter[User._meta.label] == 2
    assert User.objects.filter(pk=user_instance.pk).count() == 0
    assert User.objects.filter(pk=user_instance2.pk).count() == 0

def test_delete_with_fast_delete(user_instance):
    collector = Collector(using='default')
    collector.add([user_instance], None, None, False)

    # Assuming can_fast_delete is always true for this user instance
    collector.can_fast_delete = lambda instance: True

    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter[User._meta.label] == 1
    with pytest.raises(ObjectDoesNotExist):
        User.objects.get(pk=user_instance.pk)

def test_delete_with_pre_delete_signal(user_instance):
    pre_delete_called = []

    def pre_delete_handler(sender, instance, **kwargs):
        pre_delete_called.append(instance)

    signals.pre_delete.connect(pre_delete_handler)

    collector = Collector(using='default')
    collector.add([user_instance], None, None, False)

    count, deleted_counter = collector.delete()

    assert len(pre_delete_called) == 1
    assert pre_delete_called[0] == user_instance
    signals.pre_delete.disconnect(pre_delete_handler)

def test_delete_multiple_times(user_instance):
    collector = Collector(using='default')
    collector.add([user_instance], None, None, False)

    count1, deleted_counter1 = collector.delete()
    assert count1 == 1

    count2, deleted_counter2 = collector.delete()  # Deleting again should not raise error
    assert count2 == 0
    assert deleted_counter2[User._meta.label] == 0