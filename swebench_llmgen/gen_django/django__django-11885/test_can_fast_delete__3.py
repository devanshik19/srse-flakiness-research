import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db.models.deletion import DO_NOTHING, CASCADE

def test_can_fast_delete_no_cascade():
    collector = Collector(using='default')
    user = User.objects.create(username='testuser')
    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_with_cascade():
    collector = Collector(using='default')
    user = User.objects.create(username='testuser')
    
    # Create a related model with CASCADE
    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=CASCADE)
    
    profile = Profile.objects.create(user=user)
    
    assert collector.can_fast_delete(user) is False

def test_can_fast_delete_with_do_nothing():
    collector = Collector(using='default')
    user = User.objects.create(username='testuser')

    # Create a related model with DO_NOTHING
    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=DO_NOTHING)
    
    profile = Profile.objects.create(user=user)

    assert collector.can_fast_delete(user) is True

def test_can_fast_delete_has_signal_listeners():
    from django.db.models.signals import pre_delete
    collector = Collector(using='default')
    user = User.objects.create(username='testuser')

    def signal_handler(sender, **kwargs):
        pass
    
    pre_delete.connect(signal_handler, sender=User)

    assert collector.can_fast_delete(user) is False
    
    pre_delete.disconnect(signal_handler, sender=User)

def test_can_fast_delete_with_private_fields():
    collector = Collector(using='default')
    user = User.objects.create(username='testuser')

    # Create a model with a generic foreign key (simulate private fields)
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    
    class Comment(models.Model):
        content_type = models.ForeignKey(ContentType, on_delete=DO_NOTHING)
        object_id = models.PositiveIntegerField()
        content_object = GenericForeignKey('content_type', 'object_id')
    
    Comment.objects.create(content_type=ContentType.objects.get_for_model(User), object_id=user.id)

    assert collector.can_fast_delete(user) is False