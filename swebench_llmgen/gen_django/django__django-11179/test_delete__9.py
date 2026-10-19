import pytest
from collections import Counter
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import signals
from django.db.models.deletion import Collector


@pytest.fixture
def user():
    return User.objects.create(username='testuser', password='testpass')


def test_delete_single_instance(user):
    collector = Collector(using='default')
    collector.add([user], source=None, nullable=False, reverse_dependency=None)
    
    deleted_count, deleted_models = collector.delete()
    
    assert deleted_count == 1
    assert deleted_models == {User._meta.label: 1}
    assert not User.objects.filter(pk=user.pk).exists()


def test_delete_multiple_instances(user):
    user2 = User.objects.create(username='testuser2', password='testpass2')
    collector = Collector(using='default')
    collector.add([user, user2], source=None, nullable=False, reverse_dependency=None)
    
    deleted_count, deleted_models = collector.delete()
    
    assert deleted_count == 2
    assert deleted_models == {User._meta.label: 2}
    assert not User.objects.filter(pk__in=[user.pk, user2.pk]).exists()


def test_delete_fast_delete(user):
    collector = Collector(using='default')
    collector.add([user], source=None, nullable=False, reverse_dependency=None)
    
    def can_fast_delete_patch(instance):
        return True

    collector.can_fast_delete = can_fast_delete_patch

    deleted_count, deleted_models = collector.delete()

    assert deleted_count == 1
    assert deleted_models == {User._meta.label: 1}
    assert not User.objects.filter(pk=user.pk).exists()


def test_delete_with_field_updates(user):
    user2 = User.objects.create(username='testuser2', password='testpass2')
    collector = Collector(using='default')
    collector.add([user, user2], source=None, nullable=False, reverse_dependency=None)
    collector.add_field_update('username', 'updated_user', [user])

    deleted_count, deleted_models = collector.delete()
    
    assert deleted_count == 2
    assert deleted_models == {User._meta.label: 2}
    assert not User.objects.filter(pk__in=[user.pk, user2.pk]).exists()
    user.refresh_from_db()
    assert user.username == 'updated_user'