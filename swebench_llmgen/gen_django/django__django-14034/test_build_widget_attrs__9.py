import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError

class TestBoundField:
    class DummyForm(forms.Form):
        username = forms.CharField(widget=TextInput(), required=True)

    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.form = self.DummyForm(data={'username': 'testuser'})
        self.field = self.form.fields['username']
        self.bound_field = forms.BoundField(self.form, self.field, 'username')

    def test_build_widget_attrs_required(self):
        attrs = {}
        widget_attrs = self.bound_field.build_widget_attrs(attrs)
        assert widget_attrs['required'] is True
        assert 'disabled' not in widget_attrs

    def test_build_widget_attrs_not_required(self):
        self.field.required = False
        attrs = {}
        widget_attrs = self.bound_field.build_widget_attrs(attrs)
        assert 'required' not in widget_attrs

    def test_build_widget_attrs_disabled(self):
        self.field.disabled = True
        attrs = {}
        widget_attrs = self.bound_field.build_widget_attrs(attrs)
        assert widget_attrs['disabled'] is True

    def test_build_widget_attrs_no_widget(self):
        attrs = {}
        widget_attrs = self.bound_field.build_widget_attrs(attrs, None)
        assert 'required' in widget_attrs
        assert 'disabled' not in widget_attrs

    def test_build_widget_attrs_with_custom_widget(self):
        custom_widget = TextInput(attrs={'class': 'custom-widget'})
        attrs = {}
        widget_attrs = self.bound_field.build_widget_attrs(attrs, custom_widget)
        assert widget_attrs['class'] == 'custom-widget'