import pytest
from django.contrib.auth.models import User
from django.forms import BoundField, Form, CharField, TextInput

class TestBuildWidgetAttrs:
    
    class TestForm(Form):
        username = CharField(widget=TextInput(attrs={'class': 'username'}))

    @pytest.fixture
    def setup_fields(self):
        user = User(username='testuser')
        form = self.TestForm()
        field = form.fields['username']
        bound_field = BoundField(form, field, 'username')
        return bound_field, field, form

    def test_build_widget_attrs_required(self, setup_fields):
        bound_field, field, form = setup_fields
        field.required = True
        field.widget.use_required_attribute = lambda initial: True
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert result['required'] is True

    def test_build_widget_attrs_disabled(self, setup_fields):
        bound_field, field, form = setup_fields
        field.disabled = True
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert result['disabled'] is True

    def test_build_widget_attrs_no_required(self, setup_fields):
        bound_field, field, form = setup_fields
        field.required = False
        field.widget.use_required_attribute = lambda initial: True
        attrs = {}
        result = bound_field.build_widget_attrs(attrs)
        assert 'required' not in result

    def test_build_widget_attrs_no_attrs(self, setup_fields):
        bound_field, field, form = setup_fields
        attrs = None
        result = bound_field.build_widget_attrs(attrs)
        assert result == {}

    def test_build_widget_attrs_custom_attrs(self, setup_fields):
        bound_field, field, form = setup_fields
        field.required = True
        field.widget.use_required_attribute = lambda initial: True
        attrs = {'class': 'custom-class'}
        result = bound_field.build_widget_attrs(attrs)
        assert result['class'] == 'custom-class'
        assert result['required'] is True