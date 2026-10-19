import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.db.models.deletion import Collector


def test_can_fast_delete_no_listeners():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    collector = Collector(using='default')
    assert collector.can_fast_delete(user1)  # No cascades, no listeners, should return True
    assert collector.can_fast_delete([user1, user2])  # List of users should also return True


def test_can_fast_delete_with_pre_delete_listener():
    user1 = User.objects.create(username='user1')

    def pre_delete_listener(**kwargs):
        pass

    signals.pre_delete.connect(pre_delete_listener, sender=User)

    collector = Collector(using='default')
    assert not collector.can_fast_delete(user1)  # with listener, should return False

    signals.pre_delete.disconnect(pre_delete_listener, sender=User)


def test_can_fast_delete_with_cascade_from_field():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    class Parent(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)

    parent = Parent.objects.create(user=user1)

    collector = Collector(using='default')
    assert not collector.can_fast_delete(user1, from_field=Parent._meta.get_field('user'))  # Cascade on delete

    # Verify it still returns True for user2 without cascade and without listeners
    assert collector.can_fast_delete(user2)


def test_can_fast_delete_with_do_nothing_on_relationship():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    class Parent(models.Model):
        user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    parent = Parent.objects.create(user=user1)

    collector = Collector(using='default')
    assert collector.can_fast_delete(user1, from_field=Parent._meta.get_field('user'))  # Should return True, DO_NOTHING

    # Verify it still returns True for user2 without cascades or listeners
    assert collector.can_fast_delete(user2)