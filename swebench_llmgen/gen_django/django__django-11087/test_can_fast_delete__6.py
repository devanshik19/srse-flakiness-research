import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import Collector
from django.db.models.deletion import CASCADE, DO_NOTHING

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=CASCADE)

def test_can_fast_delete_no_cascade():
    # Setting up the objects with no cascades
    user = User.objects.create(username='testuser')
    parent = Parent.objects.create(user=user)
    
    collector = Collector(using='default')
    
    assert collector.can_fast_delete([parent]) is True

def test_can_fast_delete_with_cascade():
    user = User.objects.create(username='testuser')
    parent = Parent.objects.create(user=user)
    child = Child.objects.create(parent=parent)
    
    collector = Collector(using='default')
    
    assert collector.can_fast_delete([child]) is False

def test_can_fast_delete_with_signal_listener():
    user = User.objects.create(username='testuser')
    parent = Parent.objects.create(user=user)

    def pre_delete_listener(sender, **kwargs):
        pass

    from django.db.models import signals
    signals.pre_delete.connect(pre_delete_listener, sender=Parent)

    collector = Collector(using='default')
    
    assert collector.can_fast_delete([parent]) is False
    
    signals.pre_delete.disconnect(pre_delete_listener, sender=Parent)

def test_can_fast_delete_no_relation_fields():
    user = User.objects.create(username='testuser')
    parent = Parent.objects.create(user=user)
    
    collector = Collector(using='default')
    
    assert collector.can_fast_delete([parent], from_field=None) is True

def test_can_fast_delete_with_DO_NOTHING():
    user = User.objects.create(username='testuser')
    parent = Parent.objects.create(user=user)

    class RelatedModel(models.Model):
        reference = models.ForeignKey(Parent, on_delete=DO_NOTHING)

    collector = Collector(using='default')

    assert collector.can_fast_delete([parent]) is True