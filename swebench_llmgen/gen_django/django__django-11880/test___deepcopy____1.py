import copy
import pytest
from django.forms import Field
from django.contrib.auth.models import User

class TestFieldDeepCopy:
    
    @pytest.fixture
    def field_instance(self):
        # Create an instance of Field with minimal dependencies
        field = Field()
        field.widget = TextInput()  # Assign a widget
        field.validators = []  # Assign empty validators list
        return field
    
    def test_deepcopy_creates_new_instance(self, field_instance):
        # Perform deepcopy
        copied_field = copy.deepcopy(field_instance)

        # Assertions to check if the new instance is created and is a different object
        assert copied_field is not field_instance
        assert copied_field.widget is not field_instance.widget  # Widget should be a new instance
        assert copied_field.validators is field_instance.validators  # Validators should be the same list

    def test_deepcopy_preserves_attributes(self, field_instance):
        field_instance.widget = TextInput(attrs={'placeholder': 'Enter text'})
        field_instance.validators = [lambda x: x]

        # Perform deepcopy
        copied_field = copy.deepcopy(field_instance)

        # Assert copied attributes match the original
        assert copied_field.widget.attrs == field_instance.widget.attrs
        assert copied_field.validators == field_instance.validators