import pytest
from django.db.models import Model
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, MultipleObjectsReturned
from django.apps import apps


# Simple subclass to test ModelBase behavior
class TestModel(Model):
    class Meta:
        app_label = 'test_app'


def test_new_method_creates_class_correctly():
    new_class = TestModel.__new__(TestModel, 'TestModel', (Model,), {'__module__': 'test_app', 'Meta': type('Meta', (), {})})
    assert new_class.__name__ == 'TestModel'
    assert new_class._meta is not None
    assert new_class._meta.model_name == 'testmodel'


def test_new_method_raises_on_abstract_model_without_app_label():
    with pytest.raises(RuntimeError, match="doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS."):
        class AbstractModel(Model):
            class Meta:
                abstract = True
                app_label = None
        AbstractModel.__new__(AbstractModel, 'AbstractModel', (Model,), {'__module__': 'test_app'})


def test_new_method_raises_on_field_clash():
    class BaseModel(Model):
        field1 = None

        class Meta:
            app_label = 'test_app'

    class ChildModel(BaseModel):
        field1 = None

        class Meta:
            app_label = 'test_app'

    with pytest.raises(FieldError, match="Local field 'field1' in class 'ChildModel' clashes with field of the same name from base class 'BaseModel'."):
        ChildModel.__new__(ChildModel, 'ChildModel', (BaseModel,), {'__module__': 'test_app'})


def test_new_method_raises_on_proxy_model_swapped_base():
    class BaseModel(Model):
        class Meta:
            app_label = 'test_app'

    class ProxyModel(BaseModel):
        class Meta:
            app_label = 'test_app'
            proxy = True

    with pytest.raises(TypeError, match="cannot proxy the swapped model"):
        ProxyModel.__new__(ProxyModel, 'ProxyModel', (BaseModel,), {'__module__': 'test_app'})