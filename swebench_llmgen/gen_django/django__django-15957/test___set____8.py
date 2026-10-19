import pytest
from django.contrib.auth.models import User
from django.db.models.fields.related_descriptors import ForeignKeyDeferredAttribute


@pytest.mark.django_db
def test_foreign_key_deferred_attribute_set():
    # Setting up
    user = User.objects.create(username='testuser', password='password')
    defer_attr = ForeignKeyDeferredAttribute(field=User._meta.get_field('groups'))

    # Initial set
    defer_attr.__set__(user, None)
    assert user.__dict__[defer_attr.field.attname] is None

    # Change value and ensure cache is cleared
    defer_attr.__set__(user, 'NewValue')
    assert user.__dict__[defer_attr.field.attname] == 'NewValue'
    
    # Check that it clears the cache
    assert not defer_attr.field.is_cached(user)
    
    # Test setting back to original value
    defer_attr.__set__(user, None)
    assert user.__dict__[defer_attr.field.attname] is None