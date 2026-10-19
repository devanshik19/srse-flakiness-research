import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db import models
from django.db.models import OrderWrt


class Options:
    def __init__(self, meta, app_label):
        self.meta = meta
        self.app_label = app_label
        self.parents = {}
        self.local_fields = []
        self.order_with_respect_to = None
        self.pk = None

    def _get_fields(self, reverse=False):
        return iter(self.local_fields)

    def add_to_class(self, name, field):
        self.local_fields.append(field)

    def setup_pk(self, field):
        self.pk = field


def test__prepare_with_ordering():
    # Prepare a model with an OrderWrt field
    class ModelWithOrder(models.Model):
        pass

    options = Options(meta=None, app_label='app_label')
    options.local_fields = [OrderWrt('order_field')]
    options.order_with_respect_to = 'order_field'
    
    options._prepare(ModelWithOrder)

    assert options.ordering == ('_order',)


def test__prepare_without_ordering():
    # Prepare a model without an OrderWrt field
    class SimpleModel(models.Model):
        pass

    options = Options(meta=None, app_label='app_label')
    options.local_fields = []
    options.order_with_respect_to = None

    options._prepare(SimpleModel)

    assert options.order_with_respect_to is None


def test__prepare_with_field_does_not_exist():
    class TestModel(models.Model):
        name = models.CharField(max_length=100)

    options = Options(meta=None, app_label='app_label')
    options.local_fields = [User._meta.get_field('id')]
    options.order_with_respect_to = 'non_existing_field'

    with pytest.raises(FieldDoesNotExist):
        options._prepare(TestModel)


def test__prepare_improperly_configured():
    class ParentModel(models.Model):
        pass

    class TestModel(models.Model):
        parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)

    options = Options(meta=None, app_label='app_label')
    options.parents['parent'] = options.local_fields.append(TestModel._meta.get_field('parent'))

    with pytest.raises(ImproperlyConfigured):
        options._prepare(TestModel)