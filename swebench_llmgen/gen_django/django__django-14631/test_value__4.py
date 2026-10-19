import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundFieldValue:

    class TestForm(forms.Form):
        username = forms.CharField()

    @pytest.fixture
    def setup_bound_field(self):
        user = User.objects.create_user(username='testuser', password='12345')
        form = self.TestForm(data={'username': 'testuser'})
        form.is_bound = True
        field = form.fields['username']
        bound_field = BoundField(form, field, 'username', user.username)
        return bound_field

    def test_value_when_bound(self, setup_bound_field):
        bound_field = setup_bound_field
        assert bound_field.value() == 'testuser'

    def test_value_when_not_bound(self):
        form = self.TestForm()
        field = form.fields['username']
        bound_field = BoundField(form, field, 'username', 'initial_value')
        assert bound_field.value() == 'initial_value'

    def test_value_when_data_empty(self):
        form = self.TestForm(data={})
        form.is_bound = True
        field = form.fields['username']
        bound_field = BoundField(form, field, 'username', 'initial_value')
        assert bound_field.value() == 'initial_value'