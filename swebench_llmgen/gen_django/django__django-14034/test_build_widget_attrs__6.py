import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.utils import flatatt
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError

class TestBoundField:

    @pytest.fixture
    def user_form(self):
        class UserForm(forms.ModelForm):
            class Meta:
                model = User
                fields = ['username', 'email']

        return UserForm

    @pytest.fixture
    def bound_field(self, user_form):
        form = user_form()
        field = form.fields['username']
        return forms.BoundField(form, field, 'username')

    def test_build_widget_attrs_with_required(self, bound_field):
        bound_field.field.required = True
        bound_field.form.use_required_attribute = True
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)

        assert 'required' in result
        assert result['required'] is True

    def test_build_widget_attrs_without_required(self, bound_field):
        bound_field.field.required = False
        bound_field.form.use_required_attribute = True
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)

        assert 'required' not in result

    def test_build_widget_attrs_with_disabled(self, bound_field):
        bound_field.field.disabled = True
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)

        assert 'disabled' in result
        assert result['disabled'] is True

    def test_build_widget_attrs_with_initial_value_required(self, bound_field):
        bound_field.field.required = True
        bound_field.form.use_required_attribute = False
        bound_field.initial = 'test'
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)

        assert 'required' not in result

    def test_build_widget_attrs_no_widget(self, bound_field):
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)

        assert isinstance(result, dict)
        assert 'required' not in result
        assert 'disabled' not in result