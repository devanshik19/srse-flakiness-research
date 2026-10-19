import pytest
from django import forms
from django.contrib.auth.models import User

class Field(forms.Field):
    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        return data

def test_bound_data_with_data():
    field = Field()
    data = "sample data"
    initial = "initial data"
    result = field.bound_data(data, initial)
    assert result == data

def test_bound_data_with_disabled_field():
    field = Field()
    field.disabled = True
    data = "sample data"
    initial = "initial data"
    result = field.bound_data(data, initial)
    assert result == initial

def test_bound_data_with_empty_data():
    field = Field()
    data = ""
    initial = "initial data"
    result = field.bound_data(data, initial)
    assert result == data

def test_bound_data_with_none_data():
    field = Field()
    data = None
    initial = "initial data"
    result = field.bound_data(data, initial)
    assert result == data