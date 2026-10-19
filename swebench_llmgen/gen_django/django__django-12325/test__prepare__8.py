import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db import models
from django.db.models.options import Options

class TestOptions:

    def test_prepare_with_order_with_respect_to(self):
        class TestModel(models.Model):
            name = models.CharField(max_length=100)
            order = models.IntegerField()

        # Create an Options instance for the TestModel
        options = Options(meta=TestModel._meta, app_label='app')

        # Set order_with_respect_to to an existing field name
        options.order_with_respect_to = 'order'
        
        # Prepare the options
        options._prepare(TestModel)

        assert options.order_with_respect_to.attname == 'order'
        assert options.ordering == ('_order',)
        assert '_order' in TestModel._meta.local_fields

    def test_prepare_field_does_not_exist(self):
        class TestModel(models.Model):
            name = models.CharField(max_length=100)

        options = Options(meta=TestModel._meta, app_label='app')

        options.order_with_respect_to = 'non_existent_field'

        with pytest.raises(FieldDoesNotExist):
            options._prepare(TestModel)

    def test_prepare_improperly_configured(self):
        class ParentModel(models.Model):
            name = models.CharField(max_length=100)

        class TestModel(models.Model):
            parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)

        options = Options(meta=TestModel._meta, app_label='app')

        options.parents = { 'parent': ParentModel }
        options.local_fields = [models.Field(name='non_parent_field')]
        
        with pytest.raises(ImproperlyConfigured):
            options._prepare(TestModel)

    def test_prepare_primary_key_assignment(self):
        class TestModel(models.Model):
            name = models.CharField(max_length=100)

        options = Options(meta=TestModel._meta, app_label='app')
        options.pk = None
        options.parents = {}

        options._prepare(TestModel)

        assert TestModel._meta.pk.name == 'id'
        assert isinstance(TestModel._meta.pk, models.AutoField)