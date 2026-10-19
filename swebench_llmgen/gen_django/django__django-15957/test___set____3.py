import pytest
from django.contrib.auth.models import User
from django.db.models.fields.related_descriptors import ForeignKeyDeferredAttribute
from django.core.exceptions import FieldError

@pytest.fixture
def user_instance():
    return User.objects.create(username='testuser')

def test_foreign_key_deferred_attribute_set_correct_value(user_instance):
    field = ForeignKeyDeferredAttribute(User._meta.get_field('user'))
    deferred_attribute = ForeignKeyDeferredAttribute()

    # Setting a value for the first time
    deferred_attribute.__set__(user_instance, 1)
    assert user_instance.__dict__[field.attname] == 1

def test_foreign_key_deferred_attribute_set_different_value(user_instance):
    field = ForeignKeyDeferredAttribute(User._meta.get_field('user'))
    deferred_attribute = ForeignKeyDeferredAttribute()
    
    # Set initial value
    deferred_attribute.__set__(user_instance, 1)
    assert user_instance.__dict__[field.attname] == 1

    # Change the value, should delete cached and set new value
    deferred_attribute.__set__(user_instance, 2)
    assert user_instance.__dict__[field.attname] == 2

def test_foreign_key_deferred_attribute_set_no_change(user_instance):
    field = ForeignKeyDeferredAttribute(User._meta.get_field('user'))
    deferred_attribute = ForeignKeyDeferredAttribute()

    # Set a value initially
    deferred_attribute.__set__(user_instance, 1)
    assert user_instance.__dict__[field.attname] == 1

    # Setting the same value should not call delete_cached_value
    instance_dict_before = user_instance.__dict__.copy()
    deferred_attribute.__set__(user_instance, 1)
    assert user_instance.__dict__ == instance_dict_before