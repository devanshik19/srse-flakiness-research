import pytest
from django.db.models import DO_NOTHING, CASCADE
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_can_fast_delete_no_cascade(collector):
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete([user]) is True

def test_can_fast_delete_with_cascade(collector):
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    user1.profile.user = user2  # Assuming a one-to-one relationship exists
    user1.profile.save()
    
    # Here we simulate the condition of having a cascade relationship
    assert collector.can_fast_delete([user1], from_field=user1.profile._meta.fields[0]) is False

def test_can_fast_delete_with_signal_listeners(collector):
    # Simulating a model with signal listeners by creating a new user
    user = User.objects.create(username='testuser')
    
    def signal_listener(sender, **kwargs):
        pass

    from django.db.models import signals
    signals.post_delete.connect(signal_listener, sender=User)
    
    assert collector.can_fast_delete([user]) is False
    
    # Disconnect signal listener for cleanup
    signals.post_delete.disconnect(signal_listener, sender=User)

def test_can_fast_delete_private_fields(collector):
    class ModelWithGenericFK:
        _meta = type('Meta', (), {'parents': {}, 'private_fields': [1]})

    assert collector.can_fast_delete(ModelWithGenericFK()) is False

def test_can_fast_delete_multiple_no_conditions(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    assert collector.can_fast_delete([user1, user2]) is True

def test_can_fast_delete_without_from_field(collector):
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is True