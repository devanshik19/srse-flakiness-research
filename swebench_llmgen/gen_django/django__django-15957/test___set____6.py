import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db import transaction
from django.db.models import ForeignKey, Model
from django.db.models.fields.related_descriptors import ForeignKeyDeferredAttribute


class TestForeignKeyDeferredAttribute(Model):
    related = ForeignKey(User, on_delete=models.CASCADE)


def test_foreign_key_deferred_attribute_set():
    user = User.objects.create(username='testuser', password='testpass')
    instance = TestForeignKeyDeferredAttribute()
    deferred_attr = ForeignKeyDeferredAttribute(TestForeignKeyDeferredAttribute._meta.get_field('related'))

    # Setting the value for the first time
    deferred_attr.__set__(instance, user)
    assert instance.__dict__[deferred_attr.field.attname] == user

    # Changing the value should delete the cached value
    instance.__dict__[deferred_attr.field.attname] = 'some_other_value'  # Simulate cached value
    deferred_attr.__set__(instance, user)
    assert instance.__dict__[deferred_attr.field.attname] == user

    # Setting it to the same value should not delete the cached value
    deferred_attr.__set__(instance, user)
    assert instance.__dict__[deferred_attr.field.attname] == user

    # Setting to None should be allowed
    deferred_attr.__set__(instance, None)
    assert instance.__dict__[deferred_attr.field.attname] is None