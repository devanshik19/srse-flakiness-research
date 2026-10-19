import pytest
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db.models import Manager
from django.db.models.fields.proxy import OrderWrt

class Options:
    FORWARD_PROPERTIES = []
    REVERSE_PROPERTIES = []
    default_apps = None

    def __init__(self, meta, app_label):
        self.meta = meta
        self.app_label = app_label
        self.order_with_respect_to = None
        self.ordering = []
        self.pk = None
        self.parents = {}
        self.local_fields = []
    
    def _get_fields(self, reverse=False):
        return self.local_fields

    def setup_pk(self, field):
        self.pk = field

    def add_to_class(self, name, value):
        setattr(self.meta, name, value)

def test_prepare_order_with_respect_to_existing_field():
    class ModelWithOrder(models.Model):
        order = models.IntegerField()
    
    options = Options(ModelWithOrder, 'app_label')
    options.order_with_respect_to = 'order'
    options.local_fields = [models.IntegerField(name='order')] # Mimicking local fields
    
    options._prepare(ModelWithOrder)

    assert options.ordering == ('_order',)
    assert '_order' in ModelWithOrder._meta.get_fields()

def test_prepare_order_with_respect_to_invalid_field():
    options = Options(User, 'auth')
    options.order_with_respect_to = 'invalid_field'
    options.local_fields = [models.CharField(name='username', max_length=150)]

    with pytest.raises(FieldDoesNotExist):
        options._prepare(User)

def test_prepare_without_order_with_respect_to():
    class ModelWithoutOrder(models.Model):
        name = models.CharField(max_length=100)

    options = Options(ModelWithoutOrder, 'app_label')
    
    options._prepare(ModelWithoutOrder)

    assert options.order_with_respect_to is None
    assert options.pk is None

def test_prepare_with_parent_link_promoted():
    class Parent(models.Model):
        pass

    class Child(models.Model):
        parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    
    options = Options(Child, 'app_label')
    options.parents = {'parent': Child._meta.get_field('parent')}
    options.local_fields = []

    options._prepare(Child)

    assert options.pk.name == 'parent'
    
def test_prepare_with_auto_field_as_pk():
    class ModelWithAutoField(models.Model):
        pass
    
    options = Options(ModelWithAutoField, 'app_label')
    
    options._prepare(ModelWithAutoField)

    assert isinstance(options.pk, models.AutoField)