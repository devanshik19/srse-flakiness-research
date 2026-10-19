import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import DO_NOTHING, signals
from django.db.models.deletion import Collector
from django.db.models.deletion import CASCADE

@pytest.mark.parametrize("from_field, expect_fast_delete", [
    (None, False),  # No from_field specified
    ("not_cascade", False),  # `from_field.remote_field.on_delete` is not CASCADE
])
def test_can_fast_delete_no_cascade(from_field, expect_fast_delete):
    user = User.objects.create(username='testuser', password='password')
    collector = Collector(using='default')
    assert collector.can_fast_delete(user, from_field) is expect_fast_delete

@pytest.mark.parametrize("pre_delete_listeners, post_delete_listeners, m2m_changed_listeners, expect_fast_delete", [
    (0, 0, 0, True),  # No listeners
    (1, 0, 0, False),  # pre_delete listener present
    (0, 1, 0, False),  # post_delete listener present
    (0, 0, 1, False),  # m2m_changed listener present
])
def test_can_fast_delete_with_signal_listeners(pre_delete_listeners, post_delete_listeners, m2m_changed_listeners, expect_fast_delete):
    user = User.objects.create(username='testuser', password='password')
    
    # Add signal listeners based on parameters
    if pre_delete_listeners > 0:
        signals.pre_delete.connect(lambda sender, **kwargs: None, sender=User)
    if post_delete_listeners > 0:
        signals.post_delete.connect(lambda sender, **kwargs: None, sender=User)
    if m2m_changed_listeners > 0:
        signals.m2m_changed.connect(lambda sender, **kwargs: None, sender=User)
    
    collector = Collector(using='default')
    assert collector.can_fast_delete(user) is expect_fast_delete
    
    # Disconnect the signals after the test
    if pre_delete_listeners > 0:
        signals.pre_delete.disconnect(lambda sender, **kwargs: None, sender=User)
    if post_delete_listeners > 0:
        signals.post_delete.disconnect(lambda sender, **kwargs: None, sender=User)
    if m2m_changed_listeners > 0:
        signals.m2m_changed.disconnect(lambda sender, **kwargs: None, sender=User)

def test_can_fast_delete_with_candidates():
    user = User.objects.create(username='testuser', password='password')
    collector = Collector(using='default')
    
    # Simulate conditions for fast delete
    collector.can_fast_delete(user)  # Should be true if no foreign keys or listeners

    # Check against actual expected behavior based on User model
    assert collector.can_fast_delete(user, from_field=None) is True