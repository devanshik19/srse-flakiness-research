import pytest
from django.forms.fields import Field
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError

def test_deepcopy_field():
    field = Field()
    field.widget = TextInput()
    field.validators = [lambda x: x]  # Simple identity validator for testing

    # Perform a deepcopy
    copied_field = field.__deepcopy__({})
    
    # Check that the original and copied fields are different objects
    assert field is not copied_field

    # Check that the copied field has the same widget
    assert isinstance(copied_field.widget, TextInput)
    
    # Check that the widget is a deep copy
    assert field.widget is not copied_field.widget
    
    # Check that the validators list is a copy
    assert field.validators is not copied_field.validators
    assert field.validators == copied_field.validators

    # Modify validators in the copied field and ensure it doesn't affect the original
    copied_field.validators.append(lambda x: ValidationError("Error!"))
    with pytest.raises(ValidationError):
        for validator in copied_field.validators:
            if callable(validator):
                validator("invalid")

    # Original should still have its validators intact
    assert len(field.validators) == 1