import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals, DO_NOTHING
from django.db.models.deletion import Collector

class DummyRelatedModel(models.Model):
    user = models.ForeignKey(User, on_delete=DO_NOTHING)

@pytest.fixture
def collector():
    return Collector(using='default')

def test_can_fast_delete_no_cascade(collector):
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_with_pre_delete_signal(collector):
    def pre_delete_listener(sender, **kwargs):
        pass
    signals.pre_delete.connect(pre_delete_listener, sender=User)

    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is False

    signals.pre_delete.disconnect(pre_delete_listener, sender=User)

def test_can_fast_delete_with_parent_reference(collector):
    related_instance = DummyRelatedModel.objects.create()
    user = User.objects.create(username='testuser')
    related_instance.user = user
    related_instance.save()

    assert collector.can_fast_delete(related_instance) is False

def test_can_fast_delete_with_invalid_from_field(collector):
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user, from_field=DummyRelatedModel._meta.get_field('user')) is False