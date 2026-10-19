import pytest
from django.db.models.base import ModelBase
from django.contrib.auth.models import User
from django.core.exceptions import FieldError


class Meta:
    pass


class CustomModel(metaclass=ModelBase):
    Meta = Meta


def test_new_creates_class_with_valid_attributes():
    """Test that __new__ method creates a class with valid attributes."""
    model_class = CustomModel
    assert model_class.__name__ == 'CustomModel'
    assert model_class.__module__ == __name__


def test_new_class_without_meta_raises_runtime_error():
    """Test that __new__ raises RuntimeError if no Meta and not in INSTALLED_APPS."""
    with pytest.raises(RuntimeError):
        class InvalidModel(metaclass=ModelBase):
            pass


def test_new_abstract_class_creates_successfully():
    """Test that abstract classes are created successfully."""
    class AbstractModel(metaclass=ModelBase):
        class Meta:
            abstract = True

    abstract_model_class = AbstractModel
    assert abstract_model_class._meta.abstract is True


def test_new_class_with_duplicate_field_raises_field_error():
    """Test that __new__ raises FieldError if there is a field name clash."""
    class BaseModel(metaclass=ModelBase):
        name = None
        
    class ConflictModel(BaseModel):
        name = None

    with pytest.raises(FieldError):
        ConflictModel()


def test_new_class_with_proxy_model_setup():
    """Test that proxy models get setup correctly."""
    class BaseModel(metaclass=ModelBase):
        pass

    class ProxyModel(BaseModel):
        class Meta:
            proxy = True

    proxy_model_class = ProxyModel
    assert proxy_model_class._meta.proxy is True
    assert proxy_model_class._meta.concrete_model is BaseModel


def test_new_class_inherits_fields_from_parent():
    """Test that non-abstract child classes inherit attributes from parent classes."""
    class ParentModel(metaclass=ModelBase):
        field1 = None

    class ChildModel(ParentModel):
        pass

    assert 'field1' in ChildModel.__dict__


def test_new_class_with_invalid_proxy_model_setup():
    """Test that creating invalid proxy models raises TypeError."""
    class AbstractModel(metaclass=ModelBase):
        class Meta:
            abstract = True

    class InvalidProxy(AbstractModel):
        class Meta:
            proxy = True

    with pytest.raises(TypeError):
        InvalidProxy()