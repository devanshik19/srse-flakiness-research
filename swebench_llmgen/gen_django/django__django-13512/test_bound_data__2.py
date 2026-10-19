import pytest
from django.forms import BoundField
from django.contrib.auth.models import User
from django.forms.fields import Field

class TestField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disabled = False

def test_bound_data_with_disabled_field():
    field = TestField()
    initial_data = "initial_value"
    result = field.bound_data(None, initial_data)
    assert result == initial_data

def test_bound_data_with_enabled_field():
    field = TestField()
    field.disabled = False
    submitted_data = "submitted_value"
    result = field.bound_data(submitted_data, None)
    assert result == submitted_data

def test_bound_data_with_none_data():
    field = TestField()
    initial_data = "initial_value"
    result = field.bound_data(None, initial_data)
    assert result == initial_data