import pytest
from django.db.models.base import ModelBase
from django.core.exceptions import FieldError, MultipleObjectsReturned, ObjectDoesNotExist


class BaseModel(metaclass=ModelBase):
    pass


class DerivedModel(BaseModel):
    pass


class ProxyModel(DerivedModel):
    class Meta:
        proxy = True


class AbstractModel(BaseModel):
    class Meta:
        abstract = True


def test_new_creates_regular_model():
    model = BaseModel.__new__(BaseModel, 'TestModel', (BaseModel,), {})
    assert model.__name__ == 'TestModel'
    assert not model._meta.abstract


def test_new_creates_abstract_model():
    model = AbstractModel.__new__(AbstractModel, 'TestAbstractModel', (BaseModel,), {})
    assert model.__name__ == 'TestAbstractModel'
    assert model._meta.abstract


def test_new_creates_proxy_model():
    model = ProxyModel.__new__(ProxyModel, 'TestProxyModel', (DerivedModel,), {})
    assert model.__name__ == 'TestProxyModel'
    assert model._meta.proxy


def test_new_raises_runtime_error_for_model_without_app_label():
    with pytest.raises(RuntimeError):
        ModelBase.__new__(BaseModel, 'NoAppLabelModel', (BaseModel,), {'Meta': type('Meta', (), {})})


def test_new_raises_field_error_on_clashing_field_names():
    class AnotherBaseModel(metaclass=ModelBase):
        field1 = None

    class ClashingFieldModel(AnotherBaseModel):
        field1 = None

    with pytest.raises(FieldError):
        ClashingFieldModel.__new__(ClashingFieldModel, 'ClashingFieldModel', (AnotherBaseModel,), {})


def test_new_raises_multiple_objects_returned_for_clashing_meta():
    class ConflictingBaseModel(metaclass=ModelBase):
        class Meta:
            ordering = ['field1']

    class ConflictModel(ConflictingBaseModel):
        class Meta:
            ordering = ['field1']  # This will clash

    with pytest.raises(MultipleObjectsReturned):
        ConflictModel.__new__(ConflictModel, 'ConflictModel', (ConflictingBaseModel,), {})