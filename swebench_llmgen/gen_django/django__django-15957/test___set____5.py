import pytest
from django.contrib.auth.models import User
from django.db models.fields.related_descriptors import ForeignKeyDeferredAttribute
from django.core.exceptions import FieldError

def test_foreign_key_deferred_attribute_set():
    # Arrange
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    # Create the ForeignKeyDeferredAttribute with a mock field
    field = type('MockField', (), {
        'attname': 'related_user_id',
        'is_cached': lambda self, instance: instance.__dict__.get('related_user_id') is not None,
        'delete_cached_value': lambda self, instance: instance.__dict__.pop('related_user_id', None),
    })()

    deferred_attribute = ForeignKeyDeferredAttribute()
    deferred_attribute.field = field

    # Create a mock instance with a property to simulate __dict__
    class MockInstance:
        pass

    instance = MockInstance()

    # Act: set first value
    deferred_attribute.__set__(instance, user1.id)
    
    # Assert: value is set correctly
    assert instance.__dict__['related_user_id'] == user1.id

    # Act: set second value (should trigger cache deletion)
    deferred_attribute.__set__(instance, user2.id)
    
    # Assert: previous value should be deleted and new value set
    assert 'related_user_id' not in instance.__dict__  # Cached value deleted
    assert instance.__dict__['related_user_id'] == user2.id