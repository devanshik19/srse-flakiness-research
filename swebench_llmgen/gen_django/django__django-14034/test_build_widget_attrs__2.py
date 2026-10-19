import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError

class TestBoundField:
    
    @pytest.fixture
    def setup_field(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'test-class'}))

        form = TestForm()
        field = form.fields['name']
        return form, field

    def test_build_widget_attrs_with_required(self, setup_field):
        form, field = setup_field
        bound_field = forms.BoundField(form, field, 'name')
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert result.get('required') is True

    def test_build_widget_attrs_without_required(self, setup_field):
        form, field = setup_field
        field.required = False
        bound_field = forms.BoundField(form, field, 'name')
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert 'required' not in result

    def test_build_widget_attrs_with_disabled(self, setup_field):
        form, field = setup_field
        field.disabled = True
        bound_field = forms.BoundField(form, field, 'name')
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert result.get('disabled') is True

    def test_build_widget_attrs_with_initial(self, setup_field):
        form, field = setup_field
        bound_field = forms.BoundField(form, field, 'name')
        bound_field.initial = 'Initial Value'
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)

        assert 'required' in result
        assert result['disabled'] is False

    def test_build_widget_attrs_custom_widget(self, setup_field):
        form, field = setup_field
        custom_widget = TextInput(attrs={'class': 'custom-widget'})
        bound_field = forms.BoundField(form, field, 'name')
        attrs = {'class': 'initial-class'}
        result = bound_field.build_widget_attrs(attrs, widget=custom_widget)

        assert result['class'] == 'initial-class'
        assert 'required' in result