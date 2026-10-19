import pytest
from django.db.models import Model
from django.db import models
from django.core.exceptions import FieldError, ObjectDoesNotExist, MultipleObjectsReturned

class TestModelBase(Model):
    class Meta:
        app_label = 'test_app'

class ConcreteModel(TestModelBase):
    pass

class AbstractModel(TestModelBase):
    class Meta:
        abstract = True

class ProxyModel(ConcreteModel):
    class Meta:
        proxy = True

def test_model_base_new_creates_concrete_class():
    assert isinstance(ConcreteModel, type)
    assert ConcreteModel._meta.model_name == 'concretemodel'

def test_model_base_new_creates_abstract_class():
    with pytest.raises(TypeError):
        AbstractModel()

def test_model_base_new_creates_proxy_class():
    assert isinstance(ProxyModel, type)
    assert ProxyModel._meta.proxy is True

def test_model_base_new_raises_runtime_error_without_app_label():
    error_message = ("Model class test_app.AbstractModel doesn't declare an explicit "
                     "app_label and isn't in an application in "
                     "INSTALLED_APPS.")
    with pytest.raises(RuntimeError, match=error_message):
        AbstractModel()

def test_model_base_new_raises_field_error_on_field_clash():
    class AnotherConcreteModel(TestModelBase):
        field1 = models.CharField(max_length=100)

    class ClashModel(AnotherConcreteModel):
        field1 = models.CharField(max_length=100)

    error_message = 'Local field "field1" in class "ClashModel" clashes with field of the same name from base class "AnotherConcreteModel".'
    with pytest.raises(FieldError, match=error_message):
        ClashModel()

def test_model_base_new_raises_type_error_on_invalid_proxy():
    with pytest.raises(TypeError, match="Proxy model 'ProxyModel' cannot proxy the swapped model"):
        class SwappedModel(TestModelBase):
            class Meta:
                swap = True
        class InvalidProxy(SwappedModel):
            class Meta:
                proxy = True