import pytest
from collections import Counter
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models.deletion import Collector, CASCADE, DO_NOTHING

@pytest.fixture
def collector():
    return Collector(using='default')

def test_can_fast_delete_no_relations(collector):
    user = User.objects.create(username='testuser')
    result = collector.can_fast_delete(user)
    assert result is True

def test_can_fast_delete_with_on_delete_do_nothing(collector):
    # Simulating a scenario where related models have `on_delete=DO_NOTHING`
    user = User.objects.create(username='testuser')
    # Assume we have a ForeignKey with DO_NOTHING (not shown in the Collector class)
    from django.db import models

    class RelatedModel(models.Model):
        user = models.ForeignKey(User, on_delete=DO_NOTHING)

    related_instance = RelatedModel.objects.create(user=user)

    result = collector.can_fast_delete(user)
    assert result is True

def test_can_fast_delete_with_on_delete_cascade(collector):
    # Simulating a ForeignKey with CASCADE (not shown in the Collector class)
    user = User.objects.create(username='testuser')

    class RelatedModel(models.Model):
        user = models.ForeignKey(User, on_delete=CASCADE)

    related_instance = RelatedModel.objects.create(user=user)

    result = collector.can_fast_delete(user)
    assert result is False

def test_can_fast_delete_has_signal_listeners(collector):
    user = User.objects.create(username='testuser')

    # Create a signal listener (not shown in the Collector class)
    from django.db.models.signals import pre_delete

    def dummy_listener(sender, instance, **kwargs):
        pass

    pre_delete.connect(dummy_listener, sender=User)

    result = collector.can_fast_delete(user)
    assert result is False

def test_can_fast_delete_with_from_field(collector):
    user = User.objects.create(username='testuser')
    
    # Simulate a scenario where the from_field allows fast deletion
    from_field = None  # For testing, assume no field constraints

    result = collector.can_fast_delete(user, from_field=from_field)
    assert result is True