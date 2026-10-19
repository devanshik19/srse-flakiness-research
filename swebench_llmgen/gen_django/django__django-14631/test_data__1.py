import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import Field
from django.forms.boundfield import BoundField

class TestBoundField:
    class TestForm(forms.Form):
        username = Field()

        def _field_data_value(self, field, name):
            if name == 'username':
                return 'testuser'
            return None

    @pytest.fixture
    def setup_form(self):
        form = self.TestForm(data={'username': 'testuser'})
        return form

    @pytest.fixture
    def bound_field(self, setup_form):
        return BoundField(setup_form, setup_form.fields['username'], 'username')

    def test_data_returns_value_when_provided(self, bound_field):
        assert bound_field.data == 'testuser'

    def test_data_returns_none_when_not_provided(self):
        from django import forms

        class EmptyForm(forms.Form):
            email = Field()

            def _field_data_value(self, field, name):
                if name == 'email':
                    return None
                return None

        empty_form = EmptyForm(data={})
        bound_field_empty = BoundField(empty_form, empty_form.fields['email'], 'email')
        assert bound_field_empty.data is None