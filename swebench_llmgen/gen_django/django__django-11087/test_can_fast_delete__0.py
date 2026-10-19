import pytest
from django.contrib.auth.models import User
from django.db.models import signals
from django.db.models.deletion import Collector
from django.db.models.deletion import CASCADE, DO_NOTHING

@pytest.mark.django_db
def test_can_fast_delete_no_signals():
    user = User.objects.create(username='testuser1')
    collector = Collector(using='default')
    
    assert collector.can_fast_delete(user) is False  # Check single object
    
    # Test with a queryset
    users = User.objects.filter(username='testuser1')
    assert collector.can_fast_delete(users) is False

def test_can_fast_delete_with_cascade():
    user = User.objects.create(username='testuser2')
    # Set up a related object with CASCADE (simulating ForeignKey on_delete=CASCADE here)
    # Assuming a foreign key in some model pointing to User is present.
    
    class RelatedModel(models.Model):
        user = models.ForeignKey(User, on_delete=CASCADE)

    related = RelatedModel.objects.create(user=user)
    collector = Collector(using='default')

    assert collector.can_fast_delete(user) is False  # Check single object
    assert collector.can_fast_delete(related) is False  # Check related object

def test_can_fast_delete_with_no_cascade_and_no_signals():
    user = User.objects.create(username='testuser3')

    def no_signals_receiver(sender, **kwargs):
        pass

    signals.pre_delete.connect(no_signals_receiver, sender=User)
    collector = Collector(using='default')

    assert collector.can_fast_delete(user) is True  # Check single object
    signals.pre_delete.disconnect(no_signals_receiver, sender=User)
    
    users = User.objects.filter(username='testuser3')
    assert collector.can_fast_delete(users) is True  # Test with queryset