import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:
    @pytest.fixture
    def form(self):
        class TestForm(forms.Form):
            name = forms.CharField(initial='John Doe')

        return TestForm()

    @pytest.fixture
    def field(self):
        return forms.CharField()

    @pytest.fixture
    def bound_field(self, form, field):
        return BoundField(form, field, 'name')

    def test_value_initial(self, bound_field):
        # Simulate unbound form to test initial value
        assert bound_field.value() == 'John Doe'

    def test_value_bound(self, bound_field):
        # Simulate bound form
        bound_field.form.is_bound = True
        bound_field.data = 'Jane Doe'
        
        def mock_bound_data(data, initial):
            return data if data else initial
        
        bound_field.field.bound_data = mock_bound_data
        
        assert bound_field.value() == 'Jane Doe'

    def test_value_bound_no_data(self, bound_field):
        # Simulate bound form but no data input
        bound_field.form.is_bound = True
        bound_field.data = ''
        
        def mock_bound_data(data, initial):
            return data if data else initial
        
        bound_field.field.bound_data = mock_bound_data
        
        assert bound_field.value() == 'John Doe'