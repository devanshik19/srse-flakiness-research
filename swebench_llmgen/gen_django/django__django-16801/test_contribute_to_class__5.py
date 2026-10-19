import pytest
from django.contrib.auth.models import User
from django.db import models

class TestFileField(models.Field):
    descriptor_class = None
    attname = 'test_file_field'

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.attname, self.descriptor_class(self))

class TestDescriptor:
    def __init__(self, field):
        self.field = field

class TestModel:
    test_file_field = TestFileField()

def test_contribute_to_class():
    field = TestFileField()
    field.descriptor_class = TestDescriptor

    # Simulating a model class
    model_cls = type('TestModel', (models.Model,), {})
    field.contribute_to_class(model_cls, 'test_file_field')

    # Check if the attribute was set on the model class
    assert hasattr(model_cls, field.attname)
    assert isinstance(getattr(model_cls, field.attname), TestDescriptor)