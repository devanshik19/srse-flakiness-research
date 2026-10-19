import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError

class TestBoundField:
    class TestForm(forms.Form):
        username = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'Enter username'}))

    @pytest.fixture
    def form_with_user(self):
        user = User(username='testuser')
        user.save()
        return self.TestForm(data={'username': 'testuser'})

    def test_build_widget_attrs_required(self, form_with_user):
        field = form_with_user.fields['username']
        bound_field = forms.boundfield.BoundField(form_with_user, field, 'username')
        attrs = {'class': 'input-field'}
        result = bound_field.build_widget_attrs(attrs)
        assert result['required'] is True

    def test_build_widget_attrs_disabled(self, form_with_user):
        field = form_with_user.fields['username']
        field.disabled = True
        bound_field = forms.boundfield.BoundField(form_with_user, field, 'username')
        attrs = {'class': 'input-field'}
        result = bound_field.build_widget_attrs(attrs)
        assert result['disabled'] is True

    def test_build_widget_attrs_no_attrs(self, form_with_user):
        field = form_with_user.fields['username']
        bound_field = forms.boundfield.BoundField(form_with_user, field, 'username')
        result = bound_field.build_widget_attrs(None)
        assert 'required' not in result
        assert 'disabled' not in result

    def test_build_widget_attrs_custom_widget(self, form_with_user):
        field = form_with_user.fields['username']
        custom_widget = TextInput(attrs={'class': 'custom-input'})
        bound_field = forms.boundfield.BoundField(form_with_user, field, 'username')
        attrs = {'class': 'input-field'}
        result = bound_field.build_widget_attrs(attrs, widget=custom_widget)
        assert result['class'] == 'input-field'