import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db.models import CASCADE, DO_NOTHING
from django.db.models import signals

@pytest.fixture
def collector():
    return Collector(using='default')

def test_can_fast_delete_no_signals(collector):
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_with_signals(collector):
    def signal_handler(sender, **kwargs):
        pass

    signals.pre_delete.connect(signal_handler, sender=User)

    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is False

    signals.pre_delete.disconnect(signal_handler, sender=User)

def test_can_fast_delete_with_cascade_relationship(collector):
    class Parent(models.Model):
        child = models.ForeignKey(User, on_delete=CASCADE)

    parent = Parent.objects.create()
    user = User.objects.create(username='testuser')
    parent.child = user
    parent.save()

    assert collector.can_fast_delete(user, from_field=parent.child.field) is False

def test_can_fast_delete_with_no_cascade(collector):
    class Child(models.Model):
        parent = models.ForeignKey(User, on_delete=DO_NOTHING)

    user = User.objects.create(username='testuser')
    child = Child.objects.create(parent=user)

    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_with_invalid_obj(collector):
    assert collector.can_fast_delete("not_a_user_instance") is False