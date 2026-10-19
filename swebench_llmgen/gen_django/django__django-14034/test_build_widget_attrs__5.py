import pytest
from django import forms
from django.contrib.auth.models import User
from your_app.forms import BoundField  # replace 'your_app' with your actual app name

class TestBoundField:
    
    @pytest.fixture
    def user_form(self):
        class UserForm(forms.Form):
            username = forms.CharField(required=True)
            email = forms.EmailField(required=False)
        
        return UserForm()

    @pytest.fixture
    def bound_field(self, user_form):
        return BoundField(user_form, user_form.fields['username'], 'username')

    def test_build_widget_attrs_required(self, bound_field):
        attrs = {}
        bound_field.initial = ''
        bound_field.field.required = True
        bound_field.form.use_required_attribute = True

        result = bound_field.build_widget_attrs(attrs)
        assert result['required'] is True

    def test_build_widget_attrs_not_required(self, bound_field):
        attrs = {}
        bound_field.initial = ''
        bound_field.field.required = False
        bound_field.form.use_required_attribute = True

        result = bound_field.build_widget_attrs(attrs)
        assert 'required' not in result

    def test_build_widget_attrs_disabled(self, bound_field):
        attrs = {}
        bound_field.field.disabled = True

        result = bound_field.build_widget_attrs(attrs)
        assert result['disabled'] is True

    def test_build_widget_attrs_no_widget(self, bound_field):
        attrs = {}
        bound_field.field.disabled = False
        bound_field.initial = ''

        result = bound_field.build_widget_attrs(attrs)
        assert 'disabled' not in result

    def test_build_widget_attrs_custom_widget(self, bound_field):
        attrs = {}
        custom_widget = forms.TextInput()  # Use a TextInput widget for example.
        bound_field.field.widget = custom_widget

        result = bound_field.build_widget_attrs(attrs, widget=custom_widget)
        assert result == attrs  # Since no modifications should be made.

    def test_build_widget_attrs_with_initial(self, bound_field):
        attrs = {}
        bound_field.initial = 'test'
        bound_field.field.required = True
        bound_field.form.use_required_attribute = True

        result = bound_field.build_widget_attrs(attrs)
        assert result['required'] is True