import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestFieldContributeToClass:
    
    def test_contribute_to_class_registers_field_with_model(self):
        field = Field()
        user = User  # Using existing User model

        field.contribute_to_class(user, 'test_field')
        
        assert hasattr(user, 'test_field')
        assert isinstance(getattr(user, 'test_field'), Field)

    def test_contribute_to_class_private_only_creates_separate_instance(self):
        field = Field()
        user = User  # Using existing User model
        
        field.contribute_to_class(user, 'private_field', private_only=True)
        
        assert hasattr(user, 'private_field')
        assert isinstance(getattr(user, 'private_field'), Field)

        subclass_user = type('SubClassUser', (user,), {})
        field.contribute_to_class(subclass_user, 'private_field', private_only=True)
        
        assert hasattr(subclass_user, 'private_field')
        assert isinstance(getattr(subclass_user, 'private_field'), Field)
        assert getattr(user, 'private_field') is not getattr(subclass_user, 'private_field')

    def test_contribute_to_class_without_column_sets_descriptor(self):
        field = Field()
        field.attname = 'test_field'
        field.column = None
        user = User  # Using existing User model

        field.contribute_to_class(user, 'test_field')

        assert isinstance(getattr(user, 'test_field'), Field.descriptor_class)

    def test_contribute_to_class_with_choices_registers_display_method(self):
        field = Field()
        field.name = 'test_field'
        field.attname = 'test_field'
        field.choices = [(1, 'Choice 1'), (2, 'Choice 2')]
        user = User  # Using existing User model
        
        field.contribute_to_class(user, 'test_field')

        assert hasattr(user, 'get_test_field_display')
        assert callable(getattr(user, 'get_test_field_display'))