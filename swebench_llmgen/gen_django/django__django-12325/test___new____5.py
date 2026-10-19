import pytest
from django.db.models import Model
from django.db import models
from django.core.exceptions import FieldError, MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.models import User
from django.apps import apps

class CustomModel(Model):
    class Meta:
        app_label = 'test_app'

# Test class to validate the ModelBase's __new__ method
class TestModelBase:

    def test_create_model_without_abstract(self):
        class TestModel(CustomModel):
            name = models.CharField(max_length=100)

        assert TestModel._meta.model_name == 'testmodel'
        assert TestModel._meta.app_label == 'test_app'

    def test_create_abstract_model(self):
        class AbstractModel(CustomModel):
            class Meta:
                abstract = True

        class ConcreteModel(AbstractModel):
            age = models.IntegerField()

        assert ConcreteModel._meta.abstract is False
        assert ConcreteModel._meta.model_name == 'concretemodel'

    def test_create_proxy_model(self):
        class BaseModel(CustomModel):
            name = models.CharField(max_length=100)

        class ProxyModel(BaseModel):
            class Meta:
                proxy = True

        assert ProxyModel._meta.proxy is True
        assert ProxyModel._meta.concrete_model is BaseModel

    def test_create_model_with_unique_fields(self):
        class TestUser(CustomModel):
            username = models.CharField(max_length=150, unique=True)

        assert TestUser._meta.unique_together == {('username',)}

    def test_field_clash_error(self):
        class BaseModel(CustomModel):
            username = models.CharField(max_length=100)

        with pytest.raises(FieldError):
            class TestModel(BaseModel):
                username = models.CharField(max_length=200)  # This should raise error due to clash

    def test_missing_app_label_error(self):
        class NoAppLabelModel(CustomModel):
            class Meta:
                app_label = None

        with pytest.raises(RuntimeError):
            NoAppLabelModel()

    def test_multiple_inherited_field_error(self):
        class AbstractBase(CustomModel):
            email = models.EmailField()

            class Meta:
                abstract = True

        class FirstConcreteModel(AbstractBase):
            email = models.EmailField()  # This should raise error due to clash

        with pytest.raises(FieldError):
            FirstConcreteModel()