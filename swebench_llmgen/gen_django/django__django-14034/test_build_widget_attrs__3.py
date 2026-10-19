import pytest
from django import forms
from django.contrib.auth.models import User

class TestBoundField:

    class TestWidget(forms.Widget):
        def use_required_attribute(self, initial):
            return True

    class TestField(forms.Field):
        def __init__(self, required=False, disabled=False, *args, **kwargs):
            self.required = required
            self.disabled = disabled
            super().__init__(*args, **kwargs)
        widget = TestWidget()

    class TestForm(forms.Form):
        test_field = TestField(required=True)

    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.form = self.TestForm()
        self.bound_field = forms.BoundField(self.form, self.form.fields['test_field'], 'test_field')

    def test_build_widget_attrs_with_required(self):
        attrs = {}
        result = self.bound_field.build_widget_attrs(attrs)
        assert result['required'] is True

    def test_build_widget_attrs_with_disabled(self):
        self.bound_field.field.disabled = True
        attrs = {}
        result = self.bound_field.build_widget_attrs(attrs)
        assert result['disabled'] is True

    def test_build_widget_attrs_without_required_or_disabled(self):
        self.bound_field.field.disabled = False
        attrs = {}
        result = self.bound_field.build_widget_attrs(attrs)
        assert 'required' not in result
        assert 'disabled' not in result