import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models import ForeignKey, Model

class ForeignKeyDeferredAttribute:
    def __init__(self, field):
        self.field = field

    def __set__(self, instance, value):
        if instance.__dict__.get(self.field.attname) != value and self.field.is_cached(
            instance
        ):
            self.field.delete_cached_value(instance)
        instance.__dict__[self.field.attname] = value

class TestForeignKeyDeferredAttribute:
    class DummyModel(Model):
        username = ForeignKey(User, on_delete=models.CASCADE)
        
    def test_set_new_value(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        field = DummyModel._meta.get_field('username')
        deferred_attr = ForeignKeyDeferredAttribute(field)
        
        instance = self.DummyModel()
        deferred_attr.__set__(instance, user1)
        
        assert instance.__dict__[field.attname] == user1
        
        deferred_attr.__set__(instance, user2)
        assert instance.__dict__[field.attname] == user2

    def test_set_same_value(self):
        user1 = User.objects.create(username='user1')
        field = DummyModel._meta.get_field('username')
        deferred_attr = ForeignKeyDeferredAttribute(field)
        
        instance = self.DummyModel()
        deferred_attr.__set__(instance, user1)
        
        initial_value = instance.__dict__[field.attname]
        deferred_attr.__set__(instance, user1)
        
        assert instance.__dict__[field.attname] == initial_value # value should not change

    def test_delete_cached_value_called(self, monkeypatch):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        field = DummyModel._meta.get_field('username')
        deferred_attr = ForeignKeyDeferredAttribute(field)
        
        instance = self.DummyModel()
        deferred_attr.__set__(instance, user1)
        
        # Mock the delete_cached_value method
        delete_cached_value_mock = monkeypatch.setattr(field, 'delete_cached_value', lambda inst: None)
        
        # Set a new value, should delete cached value
        deferred_attr.__set__(instance, user2)
        delete_cached_value_mock.assert_called_once_with(instance)