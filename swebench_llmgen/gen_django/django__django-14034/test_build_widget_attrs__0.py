import pytest
from django.contrib.auth.models import User
from django.forms import BoundField, CharField, Form
from django.forms.widgets import TextInput

class TestBuildWidgetAttrs:

    class TestForm(Form):
        name = CharField(required=True)

    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.form = self.TestForm()
        self.field = self.form.fields['name']
        self.bound_field = BoundField(self.form, self.field, 'name')

    def test_build_widget_attrs_with_required_attribute(self):
        attrs = {}
        result = self.bound_field.build_widget_attrs(attrs)
        assert 'required' in result
        assert result['required'] is True

    def test_build_widget_attrs_without_required_attribute(self):
        attrs = {}
        self.field.required = False
        result = self.bound_field.build_widget_attrs(attrs)
        assert 'required' not in result

    def test_build_widget_attrs_with_disabled_field(self):
        attrs = {}
        self.field.disabled = True
        result = self.bound_field.build_widget_attrs(attrs)
        assert 'disabled' in result
        assert result['disabled'] is True

    def test_build_widget_attrs_with_custom_attrs(self):
        attrs = {'class': 'custom-class'}
        result = self.bound_field.build_widget_attrs(attrs)
        assert result['class'] == 'custom-class'

    def test_build_widget_attrs_with_no_widget_provided(self):
        attrs = {}
        result = self.bound_field.build_widget_attrs(attrs)
        assert 'required' in result
        assert result['required'] is True