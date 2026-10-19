import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Model

class CustomModelBase(Model):
    class Meta:
        app_label = 'test_app'

def test_new_method_with_abstract_class():
    with pytest.raises(RuntimeError) as excinfo:
        class AbstractModel(CustomModelBase):
            class Meta:
                abstract = True
                app_label = 'test_app'
        AbstractModel.__new__(CustomModelBase, 'AbstractModel', (CustomModelBase,), {})

    assert "doesn't declare an explicit app_label" in str(excinfo.value)

def test_new_method_with_valid_class():
    class ValidModel(CustomModelBase):
        name = "test"

    instance = ValidModel()
    assert isinstance(instance, ValidModel)

def test_new_method_with_field_clash():
    class ParentModel(CustomModelBase):
        name = "parent"

    with pytest.raises(FieldError) as excinfo:
        class ChildModel(ParentModel):
            name = "child"  # Field clash on 'name'

    assert "'Local field 'name' in class 'ChildModel' clashes with field of the same name from base class 'ParentModel'" in str(excinfo.value)

def test_new_method_with_proxy_model():
    class ProxyModel(ParentModel):
        class Meta:
            proxy = True

    instance = ProxyModel()
    assert isinstance(instance, ProxyModel)

def test_new_method_with_multiple_base_classes():
    class FirstBase(CustomModelBase):
        pass

    class SecondBase(CustomModelBase):
        pass

    with pytest.raises(TypeError) as excinfo:
        class MultiBaseModel(FirstBase, SecondBase):
            pass

    assert "has more than one non-abstract model base class" in str(excinfo.value)

def test_new_method_with_non_abstract_parent():
    class NonAbstractParent(CustomModelBase):
        pass

    class ChildModel(NonAbstractParent):
        pass

    instance = ChildModel()
    assert isinstance(instance, ChildModel)