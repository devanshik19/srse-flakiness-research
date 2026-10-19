import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector, DO_NOTHING, CASCADE
from django.db.models import ForeignKey, Model, signals


class Parent(Model):
    pass


class Child(Model):
    parent = ForeignKey(Parent, on_delete=CASCADE)


class AnotherChild(Model):
    parent = ForeignKey(Parent, on_delete=DO_NOTHING)


def test_can_fast_delete_no_parents_and_signals():
    collector = Collector(using='default')
    user = User.objects.create(username='testuser')
    
    result = collector.can_fast_delete(user)
    
    assert result is True


def test_can_fast_delete_with_cascade_parent():
    collector = Collector(using='default')
    parent = Parent.objects.create()
    child = Child.objects.create(parent=parent)
    
    result = collector.can_fast_delete(child, from_field=child.parent.field)
    
    assert result is False


def test_can_fast_delete_with_do_nothing_parent():
    collector = Collector(using='default')
    parent = Parent.objects.create()
    another_child = AnotherChild.objects.create(parent=parent)

    result = collector.can_fast_delete(another_child, from_field=another_child.parent.field)
    
    assert result is True


def test_can_fast_delete_with_signal_listeners():
    collector = Collector(using='default')

    def signal_handler(sender, **kwargs):
        pass

    signals.pre_delete.connect(signal_handler, sender=User)
    
    user = User.objects.create(username='testuser')
    
    result = collector.can_fast_delete(user)
    
    assert result is False
    
    # Cleanup
    signals.pre_delete.disconnect(signal_handler, sender=User)