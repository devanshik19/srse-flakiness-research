import pytest
from django.db import models
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.contrib.auth.models import User
from django.db.models import OrderWrt
from django.db.models.options import Options

class TestOptions:

    def setup_method(self):
        self.model_meta = models.options.Options(self.model_meta_class, 'auth')
    
    @pytest.fixture
    def model_meta_class(self):
        class ModelMeta:
            object_name = "TestModel"
            order_with_respect_to = "related_field"
            parents = {}
            local_fields = []

            def add_to_class(self, name, value):
                setattr(self, name, value)

            def _get_fields(self, reverse):
                return [models.Field(name='related_field', attname='related_field')]

        return ModelMeta()

    def test_prepare_with_ordering(self, model_meta_class):
        self.model_meta = Options(model_meta_class, 'auth')
        self.model_meta.order_with_respect_to = "related_field"
        
        self.model_meta._prepare(User)

        assert self.model_meta.order_with_respect_to.name == "related_field"
        assert self.model_meta.ordering == ('_order',)
        assert isinstance(User._meta.local_fields[0], OrderWrt)

    def test_prepare_without_ordering(self, model_meta_class):
        self.model_meta = Options(model_meta_class, 'auth')
        self.model_meta.order_with_respect_to = None
        
        self.model_meta._prepare(User)

        assert self.model_meta.order_with_respect_to is None
        
    def test_prepare_field_does_not_exist(self, model_meta_class):
        self.model_meta = Options(model_meta_class, 'auth')
        self.model_meta.order_with_respect_to = "non_existent_field"
        
        with pytest.raises(FieldDoesNotExist):
            self.model_meta._prepare(User)

    def test_prepare_improperly_configured(self, model_meta_class):
        self.model_meta = Options(model_meta_class, 'auth')
        self.model_meta.parents = {'parent': models.Field(name='parent_field')}

        with pytest.raises(ImproperlyConfigured):
            self.model_meta._prepare(User)