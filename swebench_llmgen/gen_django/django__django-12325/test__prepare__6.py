import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db import models
from django.db.models import Manager
from django.db.models.fields.proxy import OrderWrt

class TestOptions:
    
    class TestModel(models.Model):
        pass

    def setup_method(self):
        self.options = self.TestModel._meta
        self.options.ordering = None
        self.options.order_with_respect_to = None

    def test_prepare_with_order_with_respect_to_and_existing_field(self):
        self.options.order_with_respect_to = 'username'
        self.options.add_field(models.CharField('username', max_length=30, null=True, blank=True), None)
        
        # Invoke _prepare
        self.options._prepare(self.TestModel)

        assert self.options.ordering == ('_order',)
        assert isinstance(self.TestModel._meta.local_fields[-1], OrderWrt)

    def test_prepare_with_order_with_respect_to_and_non_existing_field(self):
        self.options.order_with_respect_to = 'non_existent_field'

        with pytest.raises(FieldDoesNotExist):
            self.options._prepare(self.TestModel)

    def test_prepare_without_order_with_respect_to_should_not_add_order_field(self):
        self.options._prepare(self.TestModel)
        
        assert self.options.order_with_respect_to is None
        assert '_order' not in [field.name for field in self.TestModel._meta.local_fields]

    def test_prepare_without_primary_key_and_parents_should_add_auto_id_field(self):
        self.options.pk = None
        self.options.parents = {}
        
        self.options._prepare(self.TestModel)

        assert self.TestModel._meta.local_fields[-1].primary_key is True
        assert isinstance(self.TestModel._meta.get_field('id'), models.AutoField)

    def test_prepare_with_primary_key_from_parent(self):
        parent_model = self.TestModel(name='parent')
        parent_model.save()
        self.options.parents = {parent_model.__class__.__name__: parent_model}
        self.options.pk = None

        self.options._prepare(self.TestModel)

        assert self.TestModel._meta.local_fields[-1].primary_key is True
        assert isinstance(self.TestModel._meta.get_field('id'), models.AutoField)