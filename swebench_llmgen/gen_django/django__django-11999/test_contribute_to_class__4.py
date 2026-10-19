import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestFieldContributeToClass:

    def test_contribute_to_class_with_private_only(self):
        field = Field()
        user_model = User
        field.column = 'username'
        field.attname = 'username'
        field.name = 'username'
        field.choices = None
        
        # Act: Contribute the field to the User model
        field.contribute_to_class(user_model, 'username', private_only=True)
        
        # Assert: Check that the field has been added properly
        assert hasattr(user_model, 'username')
        assert isinstance(getattr(user_model, 'username'), Field.descriptor_class)

    def test_contribute_to_class_without_private_only(self):
        field = Field()
        user_model = User
        field.column = 'email'
        field.attname = 'email'
        field.name = 'email'
        field.choices = None
        
        # Act: Contribute the field to the User model
        field.contribute_to_class(user_model, 'email', private_only=False)
        
        # Assert: Check that the field has been added properly
        assert hasattr(user_model, 'email')
        assert isinstance(getattr(user_model, 'email'), Field.descriptor_class)

    def test_contribute_to_class_with_choices(self):
        field = Field()
        user_model = User
        field.column = 'first_name'
        field.attname = 'first_name'
        field.name = 'first_name'
        field.choices = [('John', 'John'), ('Jane', 'Jane')]
        
        # Act: Contribute the field to the User model
        field.contribute_to_class(user_model, 'first_name', private_only=False)
        
        # Assert: Check that the get_first_name_display method is created
        assert hasattr(user_model, 'get_first_name_display')
        assert callable(getattr(user_model, 'get_first_name_display'))

    def test_contribute_to_class_no_override_classmethod(self):
        class CustomUser(User):
            @classmethod
            def username(cls):
                return "Class Method"

        field = Field()
        custom_user_model = CustomUser
        field.column = 'username'
        field.attname = 'username'
        field.name = 'username'
        
        # Act: Contribute the field to the CustomUser model
        field.contribute_to_class(custom_user_model, 'username', private_only=False)
        
        # Assert: Ensure we did not override the classmethod
        assert getattr(custom_user_model, 'username')() == "Class Method"