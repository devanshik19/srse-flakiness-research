import pytest
from django.contrib.auth.models import User
from django.db.models import Model, AutoField
from django.db.models.fields.proxy import OrderWrt
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db import models

class TestOptions(Model):
    order_with_respect_to = None
    _meta = None
    parents = {}
    local_fields = []
    ordering = None
    pk = None

    def __init__(self, *args, **kwargs):
        self._get_fields_called = False
        self.local_fields = []
        self.pk = None
        super().__init__(*args, **kwargs)

    def _get_fields(self, reverse=False):
        self._get_fields_called = True
        return self.local_fields

    def add_to_class(self, name, value):
        setattr(self, name, value)

    def setup_pk(self, field):
        self.pk = field

@pytest.fixture
def options():
    return TestOptions()

def test_prepare_with_ordering(options):
    # Set up a field that should be used for 'order_with_respect_to'
    order_field = AutoField(name='order_field')
    options.local_fields = [order_field]
    
    options.order_with_respect_to = 'order_field'
    options._prepare(User)

    assert options.order_with_respect_to == order_field
    assert options.ordering == ('_order',)
    assert isinstance(User._meta.local_fields[-1], OrderWrt)

def test_prepare_without_ordering(options):
    options._prepare(User)

    assert options.order_with_respect_to is None
    assert options.pk is None

def test_prepare_with_parents(options):
    parent_field = AutoField(name='parent_field')
    options.parents = {'parent': parent_field}
    options.local_fields = [parent_field]

    options._prepare(User)

    assert options.pk == parent_field
    assert isinstance(User._meta.local_fields[-1], AutoField)

def test_prepare_raises_field_does_not_exist(options):
    options.order_with_respect_to = 'non_existing_field'
    with pytest.raises(FieldDoesNotExist):
        options._prepare(User)

def test_prepare_raises_improperly_configured(options):
    options.parents = {}  # No parents
    options.local_fields = [AutoField(name='existing_field')]
    
    with pytest.raises(ImproperlyConfigured):
        options._prepare(User)