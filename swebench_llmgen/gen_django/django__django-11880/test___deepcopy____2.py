import pytest
from django.forms.fields import Field
from django.contrib.auth.models import User

@pytest.fixture
def field_instance():
    return Field()

def test_deepcopy_widget(field_instance):
    original_widget = field_instance.widget
    new_field = field_instance.__deepcopy__({})
    
    assert new_field is not field_instance
    assert new_field.widget is not original_widget
    assert new_field.widget == original_widget

def test_deepcopy_validators(field_instance):
    original_validators = field_instance.validators
    field_instance.validators.append(lambda x: x)  # Adding a sample validator
    new_field = field_instance.__deepcopy__({})
    
    assert new_field.validators != original_validators
    assert new_field.validators == field_instance.validators

def test_deepcopy_memo(field_instance):
    memo = {}
    new_field = field_instance.__deepcopy__(memo)
    
    assert id(new_field) in memo.values()
    assert id(field_instance) not in memo.values()