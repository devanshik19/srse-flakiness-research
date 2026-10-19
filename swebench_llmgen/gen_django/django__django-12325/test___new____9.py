import pytest
from django.db.models import Model
from django.urls import path
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, FieldError

class TestModelBase(Model):
    class Meta:
        abstract = True

class ConcreteModel(TestModelBase):
    name = str

def test_new_method_with_valid_model():
    class MyModel(ConcreteModel):
        pass

    assert MyModel._meta is not None

def test_new_method_with_invalid_model_no_app_label():
    with pytest.raises(RuntimeError):
        class MyInvalidModel(Model):
            pass

def test_new_method_with_proxy_model():
    class BaseModel(TestModelBase):
        pass

    class ProxyModel(BaseModel):
        class Meta:
            proxy = True

    assert ProxyModel._meta.proxy is True

def test_new_method_with_local_field_clash():
    class ParentModel(ConcreteModel):
        field1 = str

    with pytest.raises(FieldError):
        class ChildModel(ParentModel):
            field1 = int

def test_new_method_inherits_fields():
    class ParentModel(ConcreteModel):
        field1 = str

    class ChildModel(ParentModel):
        pass

    assert 'field1' in ChildModel.__dict__

def test_new_method_with_non_abstract_child():
    class AbstractModel(TestModelBase):
        class Meta:
            abstract = True
            
    class NonAbstractModel(AbstractModel):
        pass

    assert NonAbstractModel._meta is not None