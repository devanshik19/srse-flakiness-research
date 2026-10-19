import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db import IntegrityError, transaction
from django.db.models import signals

def test_can_fast_delete_no_signals():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    collector = Collector(using='default')
    assert collector.can_fast_delete(user1) is True
    assert collector.can_fast_delete([user1, user2]) is True

def test_can_fast_delete_with_cascade_on_delete():
    class Parent:
        remote_field = type('RemoteField', (), {'on_delete': CASCADE})

    collector = Collector(using='default')
    assert collector.can_fast_delete(User.objects.first(), from_field=Parent.remote_field) is False

def test_can_fast_delete_with_do_nothing_on_delete():
    class Parent:
        remote_field = type('RemoteField', (), {'on_delete': DO_NOTHING})

    collector = Collector(using='default')
    assert collector.can_fast_delete(User.objects.first(), from_field=Parent.remote_field) is True

def test_can_fast_delete_with_signal_listeners():
    def pre_delete_handler(sender, **kwargs):
        pass

    signals.pre_delete.connect(pre_delete_handler, sender=User)

    collector = Collector(using='default')
    assert collector.can_fast_delete(User.objects.first()) is False

    # Disconnect the signal to not affect other tests
    signals.pre_delete.disconnect(pre_delete_handler, sender=User)

def test_can_fast_delete_with_generic_foreign_key():
    collector = Collector(using='default')
    user = User.objects.create(username='user')
    
    # Simulate private fields by adding an attribute on the model
    User._meta.private_fields.append(type('Field', (), {'bulk_related_objects': True}))
    
    assert collector.can_fast_delete(user) is False
    
    # Clean up the attribute
    User._meta.private_fields.pop()