import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:
    
    class TestWidget(forms.Widget):
        def use_required_attribute(self, initial):
            return True

    @pytest.fixture
    def bound_field(self):
        form = forms.Form()
        field = forms.CharField(required=True, widget=self.TestWidget())
        return BoundField(form, field, 'test_field')

    def test_build_widget_attrs_with_required(self, bound_field):
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert result['required'] is True

    def test_build_widget_attrs_without_required(self, bound_field):
        bound_field.field.required = False
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert 'required' not in result

    def test_build_widget_attrs_disabled(self, bound_field):
        bound_field.field.disabled = True
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert result['disabled'] is True

    def test_build_widget_attrs_no_changes(self, bound_field):
        attrs = {'class': 'test-class'}
        result = bound_field.build_widget_attrs(attrs)
        assert result['class'] == 'test-class'
        assert 'required' not in result
        assert 'disabled' not in result

    def test_build_widget_attrs_with_custom_widget(self, bound_field):
        widget = forms.TextInput()
        attrs = {}
        result = bound_field.build_widget_attrs(attrs, widget)
        assert 'required' not in result  # Assuming default behavior for TextInput