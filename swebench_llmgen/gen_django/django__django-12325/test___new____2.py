import pytest
from django.db.models.base import ModelBase
from django.core.exceptions import FieldError, MultipleObjectsReturned, ObjectDoesNotExist

class Meta:
    abstract = False
    app_label = 'test_app'

def test_model_base_new_creates_model_class():
    attrs = {
        '__module__': 'test_app.models',
        'Meta': Meta,
    }
    model_class = ModelBase.__new__(ModelBase, 'TestModel', (ModelBase,), attrs)

    assert model_class.__name__ == 'TestModel'
    assert hasattr(model_class, '_meta')
    assert model_class._meta.app_label == 'test_app'

def test_model_base_new_raises_error_without_app_label():
    attrs_no_app = {
        '__module__': 'test_app.models',
        'Meta': type('Meta', (), {'abstract': False}),
    }
    
    with pytest.raises(RuntimeError, match="doesn't declare an explicit app_label"):
        ModelBase.__new__(ModelBase, 'TestModelNoApp', (ModelBase,), attrs_no_app)

def test_model_base_new_raises_field_error_if_field_clashes():
    class ParentModel(ModelBase):
        field1 = 'some_field'

    attrs_clash = {
        '__module__': 'test_app.models',
        'field1': 'clashing_field',
        'Meta': Meta,
    }
    
    with pytest.raises(FieldError, match="clashes with field of the same name from base class"):
        ModelBase.__new__(ModelBase, 'TestModelWithClash', (ParentModel,), attrs_clash)

def test_model_base_new_raises_multiple_objects_error_for_superclass():
    class ParentModel(ModelBase):
        class DoesNotExist(Exception):
            pass
    
    attrs_super = {
        '__module__': 'test_app.models',
        'Meta': Meta,
    }
    
    model_class = ModelBase.__new__(ModelBase, 'TestModelWithSuperclass', (ParentModel,), attrs_super)
    
    assert hasattr(model_class, 'DoesNotExist')
    assert issubclass(model_class.DoesNotExist, ParentModel.DoesNotExist)

def test_model_base_new_raises_type_error_on_proxy_model_with_swapped_base():
    class SwappedModel(ModelBase):
        _meta = type('Meta', (), {'abstract': False, 'swapped': 'AnotherModel'})
    
    attrs_proxy = {
        '__module__': 'test_app.models',
        'Meta': type('Meta', (), {'abstract': True}),
    }
    
    with pytest.raises(TypeError, match="cannot proxy the swapped model"):
        ModelBase.__new__(ModelBase, 'ProxyModel', (SwappedModel,), attrs_proxy)