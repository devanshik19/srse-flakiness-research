import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import Field

class TestFieldContribution:

    def test_contribute_to_class_creates_field(self):
        # Arrange
        class TestModel(models.Model):
            pass

        field = Field()

        # Act
        field.contribute_to_class(TestModel, 'test_field')

        # Assert
        assert 'test_field' in TestModel._meta.get_fields()
        assert isinstance(getattr(TestModel, 'test_field'), Field)

    def test_contribute_to_class_private_only_creates_separate_field(self):
        # Arrange
        class BaseModel(models.Model):
            pass

        class SubModel(BaseModel):
            pass

        field = Field()
        field.attname = 'test_field'

        # Act
        field.contribute_to_class(BaseModel, 'test_field', private_only=True)
        field.contribute_to_class(SubModel, 'test_field', private_only=True)

        # Assert
        assert len(BaseModel._meta.get_fields()) == 1
        assert len(SubModel._meta.get_fields()) == 1
        assert hasattr(BaseModel, 'test_field')
        assert hasattr(SubModel, 'test_field')

    def test_contribute_to_class_sets_descriptor_class(self):
        # Arrange
        class TestModel(models.Model):
            pass

        field = Field()
        field.attname = 'test_field'
        field.descriptor_class = Field  # Set to be the same for testing

        # Act
        field.contribute_to_class(TestModel, 'test_field')

        # Assert
        assert isinstance(getattr(TestModel, 'test_field'), Field)

    def test_contribute_to_class_with_choices(self):
        # Arrange
        class TestModel(models.Model):
            pass

        field = Field()
        field.name = 'test_field'
        field.choices = [(1, 'One'), (2, 'Two')]
        
        # Act
        field.contribute_to_class(TestModel, 'test_field')

        # Assert
        assert hasattr(TestModel, 'get_test_field_display')
        assert callable(getattr(TestModel, 'get_test_field_display'))