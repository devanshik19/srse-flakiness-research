import pytest
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.contrib.auth.models import User
from django.db import models

class Options:
    def __init__(self, meta, app_label):
        self.order_with_respect_to = meta.get('order_with_respect_to', None)
        self.object_name = meta.get('object_name', 'Model')
        self.local_fields = []
        self.pk = None
        self.parents = {}
        self.ordering = []

    def _get_fields(self, reverse=False):
        return self.local_fields

    def add_to_class(self, name, field):
        self.local_fields.append(field)

    def setup_pk(self, field):
        self.pk = field

class OrderWrt(models.Field):
    pass

def test_prepare_order_with_respect_to_field():
    meta = {'order_with_respect_to': 'user', 'object_name': 'TestModel'}
    options = Options(meta, 'app_label')
    model = User  # Using Django's built-in User model

    # Add a field to simulate the test case
    options.local_fields.append(models.CharField(name='user', max_length=255))
    
    options._prepare(model)

    assert options.order_with_respect_to.name == 'user'
    assert options.ordering == ['_order']
    assert isinstance(model._meta.local_fields[-1], OrderWrt)

def test_prepare_field_does_not_exist():
    meta = {'order_with_respect_to': 'non_existent_field', 'object_name': 'TestModel'}
    options = Options(meta, 'app_label')
    model = User

    with pytest.raises(FieldDoesNotExist) as excinfo:
        options._prepare(model)
    assert str(excinfo.value) == "TestModel has no field named 'non_existent_field'"

def test_prepare_improperly_configured():
    meta = {'order_with_respect_to': None, 'object_name': 'TestModel'}
    options = Options(meta, 'app_label')
    model = User

    # Test with a parent link, but missing parent_link=True
    options.parents = {'parent': User}

    with pytest.raises(ImproperlyConfigured) as excinfo:
        options._prepare(model)
    assert 'Add parent_link=True to' in str(excinfo.value)