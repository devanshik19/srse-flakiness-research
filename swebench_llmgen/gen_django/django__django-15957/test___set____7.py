import pytest
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.db import models

class ForeignKeyDeferredAttribute:
    def __init__(self, field):
        self.field = field

    def __set__(self, instance, value):
        if instance.__dict__.get(self.field.attname) != value and self.field.is_cached(
            instance
        ):
            self.field.delete_cached_value(instance)
        instance.__dict__[self.field.attname] = value

class TestModel(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)

def test_foreign_key_deferred_attribute_set():
    user = User.objects.create(username='test_user')
    test_instance = TestModel()
    field = TestModel._meta.get_field('user')
    deferred_attr = ForeignKeyDeferredAttribute(field)

    # Test setting a new value when it's not cached
    deferred_attr.__set__(test_instance, user)
    assert test_instance.user == user

    # Test setting the same value
    deferred_attr.__set__(test_instance, user)
    assert test_instance.user == user

    # Test setting a different value, verifying cached value deletion
    user2 = User.objects.create(username='test_user_2')
    deferred_attr.__set__(test_instance, user2)
    assert test_instance.user == user2