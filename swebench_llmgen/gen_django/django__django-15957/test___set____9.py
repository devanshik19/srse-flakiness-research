import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models.fields.related_descriptors import ForeignKeyDeferredAttribute

@pytest.fixture
def user_instance():
    return User(username='testuser')

def test_foreign_key_deferred_attribute_set_value(user_instance):
    attr = ForeignKeyDeferredAttribute(field=user_instance._meta.get_field('groups'))

    # Initial set
    attr.__set__(user_instance, None)
    assert user_instance.groups.count() == 0

    # Set a new value
    attr.__set__(user_instance, user_instance.groups.model.objects.create(name='group1'))
    assert user_instance.groups.count() == 1

    # Changing value, should delete cached
    group2 = user_instance.groups.model.objects.create(name='group2')
    attr.__set__(user_instance, group2)
    
    # Check if cached value is deleted and new value is set
    assert user_instance.groups.count() == 1
    assert user_instance.groups.first().name == 'group2'

    # Set the same value, no changes expected
    attr.__set__(user_instance, group2)
    assert user_instance.groups.count() == 1  # Still should be 1

    # Setting to None should clear the group
    attr.__set__(user_instance, None)
    assert user_instance.groups.count() == 0

def test_foreign_key_deferred_attribute_check_cached_value(user_instance):
    attr = ForeignKeyDeferredAttribute(field=user_instance._meta.get_field('groups'))
    
    # Initial set
    user_instance.groups.add(user_instance.groups.model.objects.create(name='group1'))
    assert user_instance.groups.count() == 1

    # Check if the value is cached
    assert user_instance.groups.model.objects.filter(user=user_instance).exists()

    # Remove group
    attr.__set__(user_instance, None)
    assert not user_instance.groups.model.objects.filter(user=user_instance).exists()