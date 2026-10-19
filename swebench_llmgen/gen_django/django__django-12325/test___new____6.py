import pytest
from django.db.models import Model
from django.core.exceptions import FieldError, MultipleObjectsReturned, ObjectDoesNotExist

class TestModelBase(ModelBase):
    class Meta:
        app_label = 'test_app'

def test_new_creates_model_with_valid_attrs():
    class MyModel(TestModelBase):
        pass

    assert MyModel._meta.app_label == 'test_app'
    assert MyModel._meta.abstract is False

def test_new_raises_runtime_error_if_no_app_label_and_not_in_installed_apps():
    with pytest.raises(RuntimeError, match="doesn't declare an explicit app_label"):
        class InvalidModel(ModelBase):
            class Meta:
                abstract = False

        InvalidModel()

def test_new_raises_type_error_for_proxy_model_with_swapped_model():
    class BaseModel(TestModelBase):
        pass

    class SwappedModel(BaseModel):
        class Meta:
            abstract = True

    with pytest.raises(TypeError, match="cannot proxy the swapped model"):
        class ProxyModel(BaseModel):
            class Meta:
                proxy = True

        ProxyModel()

def test_new_raises_field_error_on_local_field_clash():
    class ParentModel(TestModelBase):
        name = ModelField()

    class ChildModel(ParentModel):
        name = ModelField()

    with pytest.raises(FieldError, match="Local field 'name' in class 'ChildModel' clashes with field of the same name from base class 'ParentModel'"):
        ChildModel()

def test_new_creates_multiple_objects_returned_exception():
    class MyModel(TestModelBase):
        class Meta:
            abstract = True

    MyModel.add_to_class('MultipleObjectsReturned', subclass_exception(
        'MultipleObjectsReturned',
        (MultipleObjectsReturned,),
        MyModel.__module__,
        attached_to=MyModel
    ))
    assert MyModel.MultipleObjectsReturned == MultipleObjectsReturned

def test_new_creates_does_not_exist_exception():
    class MyModel(TestModelBase):
        class Meta:
            abstract = True

    MyModel.add_to_class('DoesNotExist', subclass_exception(
        'DoesNotExist',
        (ObjectDoesNotExist,),
        MyModel.__module__,
        attached_to=MyModel
    ))
    assert MyModel.DoesNotExist == ObjectDoesNotExist