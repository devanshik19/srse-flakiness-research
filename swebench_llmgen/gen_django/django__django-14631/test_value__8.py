import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.boundfield import BoundField


class TestBoundField:

    @pytest.fixture
    def setup(self):
        # Create a form for testing
        class TestForm(forms.Form):
            username = forms.CharField(initial='testuser')

        form = TestForm(data={'username': 'newuser'})
        bound_field = BoundField(form, form.fields['username'], 'username')
        return bound_field, form

    def test_value_bound_with_data(self, setup):
        bound_field, form = setup
        form.is_bound = True
        assert bound_field.value() == 'newuser'

    def test_value_unbound_with_initial(self, setup):
        bound_field, form = setup
        form.is_bound = False
        assert bound_field.value() == 'testuser'

    def test_value_bound_with_initial(self, setup):
        bound_field, form = setup
        form.is_bound = True
        form.data['username'] = 'updateduser'
        assert bound_field.value() == 'updateduser'

    def test_value_prepares_value(self, setup):
        bound_field, form = setup
        bound_field.field.prepare_value = lambda value: f"Prepared: {value}"
        form.is_bound = True
        form.data['username'] = 'user'
        assert bound_field.value() == 'Prepared: user'