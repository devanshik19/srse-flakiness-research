import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:
    
    @pytest.fixture
    def user_form(self):
        class UserForm(forms.ModelForm):
            class Meta:
                model = User
                fields = ['username']
        
        return UserForm()

    @pytest.fixture
    def bound_field(self, user_form):
        user_form.instance = User(username='testuser')
        user_form.is_bound = True
        user_form.full_clean()
        field = user_form['username']  # This creates a BoundField instance
        return field

    def test_data_returns_correct_value(self, bound_field):
        # Test case where the data exists
        assert bound_field.data == 'testuser'

    def test_data_returns_none_when_no_value(self):
        class EmptyForm(forms.Form):
            username = forms.CharField(required=False)

        empty_form = EmptyForm()
        bound_field = empty_form['username']
        
        # Test case where the data does not exist
        assert bound_field.data is None