import pytest
from collections import Counter
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import signals
from django.db.models.deletion import Collector


@pytest.fixture
def user_instance():
    return User.objects.create(username='testuser', password='testpass')


def test_delete_single_instance(user_instance):
    collector = Collector(using='default')
    collector.data = {User: {user_instance}}

    count, deleted_counter = collector.delete()
    
    assert count == 1
    assert deleted_counter == {User._meta.label: 1}
    assert User.objects.filter(pk=user_instance.pk).count() == 0


def test_delete_multiple_instances(user_instance):
    user_instance_2 = User.objects.create(username='testuser2', password='testpass2')
    collector = Collector(using='default')
    collector.data = {User: {user_instance, user_instance_2}}

    count, deleted_counter = collector.delete()

    assert count == 2
    assert deleted_counter == {User._meta.label: 2}
    assert User.objects.filter(pk__in=[user_instance.pk, user_instance_2.pk]).count() == 0


def test_delete_with_pre_delete_signal(user_instance):
    pre_delete_called = []

    def pre_delete_handler(sender, instance, using, **kwargs):
        pre_delete_called.append(instance)

    signals.pre_delete.connect(pre_delete_handler)

    collector = Collector(using='default')
    collector.data = {User: {user_instance}}

    count, deleted_counter = collector.delete()

    assert count == 1
    assert len(pre_delete_called) == 1
    assert pre_delete_called[0] == user_instance

    signals.pre_delete.disconnect(pre_delete_handler)


def test_delete_with_post_delete_signal(user_instance):
    post_delete_called = []

    def post_delete_handler(sender, instance, using, **kwargs):
        post_delete_called.append(instance)

    signals.post_delete.connect(post_delete_handler)

    collector = Collector(using='default')
    collector.data = {User: {user_instance}}

    count, deleted_counter = collector.delete()

    assert count == 1
    assert len(post_delete_called) == 1
    assert post_delete_called[0] == user_instance

    signals.post_delete.disconnect(post_delete_handler)


def test_fast_delete(user_instance):
    collector = Collector(using='default')
    collector.data = {User: {user_instance}}

    collector.can_fast_delete = lambda obj: True

    count, deleted_counter = collector.delete()

    assert count == 1
    assert deleted_counter == {User._meta.label: 1}
    assert User.objects.filter(pk=user_instance.pk).count() == 0