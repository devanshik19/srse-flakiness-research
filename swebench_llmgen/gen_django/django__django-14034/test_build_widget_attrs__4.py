import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import TextInput

class TestBoundField:

    class TestField(forms.Field):
        widget = TextInput()
        required = False
        disabled = False

    class TestForm(forms.Form):
        test_field = TestField()

    def setup_method(self):
        # Initialize a form and field for testing
        self.user = User(username='testuser')
        self.user.save()
        self.form = self.TestForm()
        self.field = self.TestField()
        self.bound_field = forms.BoundField(self.form, self.field, 'test_field')

    def test_build_widget_attrs_with_required_attribute(self):
        # Set field required and form use_required_attribute
        self.field.required = True
        self.form.use_required_attribute = True
        attrs = self.bound_field.build_widget_attrs({}, self.field.widget)

        assert attrs.get('required') is True
        assert attrs.get('disabled') is None

    def test_build_widget_attrs_without_required_attribute(self):
        # Set field not required and form use_required_attribute False
        self.field.required = False
        self.form.use_required_attribute = False
        attrs = self.bound_field.build_widget_attrs({}, self.field.widget)

        assert attrs.get('required') is None
        assert attrs.get('disabled') is None

    def test_build_widget_attrs_with_disabled_field(self):
        # Set field as disabled
        self.field.disabled = True
        attrs = self.bound_field.build_widget_attrs({}, self.field.widget)

        assert attrs.get('disabled') is True

    def test_build_widget_attrs_with_initial_value_and_required(self):
        # Test when initial value is present and field is required
        self.bound_field.initial = 'some value'
        self.field.required = True
        self.form.use_required_attribute = True
        attrs = self.bound_field.build_widget_attrs({}, self.field.widget)

        assert attrs.get('required') is True
        assert attrs.get('disabled') is None