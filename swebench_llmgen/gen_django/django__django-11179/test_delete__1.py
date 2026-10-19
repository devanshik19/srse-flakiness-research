import pytest
from collections import Counter
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import signals
from django.db.models.deletion import Collector

@pytest.fixture
def user_instance():
    return User.objects.create(username='testuser', password='testpass')

@pytest.fixture
def collector(using):
    return Collector(using=using)

def test_delete_single_instance(collector, user_instance):
    collector.add([user_instance], source=None, nullable=False, reverse_dependency=None)
    
    initial_count = User.objects.count()
    deleted_count, deleted = collector.delete()
    
    assert deleted_count == 1
    assert User.objects.count() == initial_count - 1
    assert deleted[User._meta.label] == 1

def test_delete_multiple_instances(collector, user_instance):
    user_instance2 = User.objects.create(username='testuser2', password='testpass')
    collector.add([user_instance, user_instance2], source=None, nullable=False, reverse_dependency=None)

    initial_count = User.objects.count()
    deleted_count, deleted = collector.delete()
    
    assert deleted_count == 2
    assert User.objects.count() == initial_count - 2
    assert deleted[User._meta.label] == 2

def test_delete_with_field_updates(collector, user_instance):
    user_instance2 = User.objects.create(username='testuser2', password='testpass')
    collector.add([user_instance, user_instance2], source=None, nullable=False, reverse_dependency=None)
    collector.add_field_update('username', 'updated_username', [user_instance])

    collector.delete()

    assert User.objects.get(pk=user_instance.pk).username == 'updated_username'
    assert User.objects.filter(pk=user_instance2.pk).first() is None

def test_delete_signals(collector, user_instance):
    signals.pre_delete_received = []
    signals.post_delete_received = []

    def pre_delete_receiver(sender, instance, **kwargs):
        signals.pre_delete_received.append(instance.username)

    def post_delete_receiver(sender, instance, **kwargs):
        signals.post_delete_received.append(instance.username)

    signals.pre_delete.connect(pre_delete_receiver)
    signals.post_delete.connect(post_delete_receiver)

    collector.add([user_instance], source=None, nullable=False, reverse_dependency=None)
    collector.delete()

    assert user_instance.username in signals.pre_delete_received
    assert user_instance.username in signals.post_delete_received

def test_can_fast_delete(collector, user_instance):
    collector.add([user_instance], source=None, nullable=False, reverse_dependency=None)

    collector.can_fast_delete = lambda instance: True 
    deleted_count, deleted = collector.delete()

    assert deleted_count == 1
    assert User.objects.filter(pk=user_instance.pk).count() == 0