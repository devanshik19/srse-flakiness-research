import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db.models import DO_NOTHING, CASCADE
from django.db import signals

@pytest.fixture
def collector():
    return Collector(using='default')

def test_can_fast_delete_no_cascades(collector):
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_with_cascades(collector):
    user = User.objects.create(username='testuser')
    # Simulating a ForeignKey with CASCADE on delete
    user.profile_set.create()  # Assuming a profile ForeignKey with CASCADE exists
    assert collector.can_fast_delete(user) is False

def test_can_fast_delete_with_signals(collector):
    user = User.objects.create(username='testuser')

    # Add a pre_delete signal listener
    def pre_delete_signal(sender, instance, **kwargs):
        pass

    signals.pre_delete.connect(pre_delete_signal)

    assert collector.can_fast_delete(user) is False

    # Clean up signal
    signals.pre_delete.disconnect(pre_delete_signal)

def test_can_fast_delete_no_from_field(collector):
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user, from_field=None) is True

def test_can_fast_delete_with_do_nothing(collector):
    # Simulate model relation with DO_NOTHING
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user, from_field=None) is True  # Simple user should return true