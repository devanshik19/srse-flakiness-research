import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db.models import CASCADE, DO_NOTHING

@pytest.fixture
def collector():
    return Collector(using='default')

def test_can_fast_delete_no_cascade(collector):
    user = User.objects.create(username='testuser')
    
    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_with_cascade(collector):
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    
    # Simulate a foreign key relationship with CASCADE behavior
    user1.profile_set.create(bio='Test Bio')  # Assuming a profile relation exists

    assert collector.can_fast_delete(user1) is False

def test_can_fast_delete_with_do_nothing(collector):
    user = User.objects.create(username='testuser')
    
    # Simulate a foreign key relationship with DO_NOTHING behavior
    user.profile_set.create(bio='Test Bio', on_delete=DO_NOTHING)  # Assuming a mechanism for this

    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_with_signal_listeners(collector):
    user = User.objects.create(username='testuser')

    # Simulate the presence of signal listeners
    collector._has_signal_listeners = lambda model: True

    assert collector.can_fast_delete(user) is False

def test_can_fast_delete_with_private_fields(collector):
    user = User.objects.create(username='testuser')

    # Simulate having private fields that would obstruct fast deleting
    collector._meta = type('Meta', (), {'private_fields': [object()]})

    assert collector.can_fast_delete(user) is False

def test_can_fast_delete_inheritance(collector):
    user = User.objects.create(username='testuser')
    
    # Simulate user instance related to non-CASCADE field
    assert collector.can_fast_delete(user, from_field=None) is True