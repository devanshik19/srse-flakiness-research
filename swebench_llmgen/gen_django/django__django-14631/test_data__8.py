import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpassword')

    @pytest.fixture
    def form(self, user):
        class TestForm(forms.Form):
            username = forms.CharField()
            password = forms.CharField(widget=forms.PasswordInput)

        form_instance = TestForm(data={'username': user.username, 'password': 'testpassword'})
        form_instance.is_bound = True
        return form_instance

    def test_data(self, form):
        bound_field = BoundField(form, form.fields['username'], 'username')

        # Test that data returns the correct value when the form is bound
        assert bound_field.data() == 'testuser'

        # Test that data returns None if the field is not part of the form data
        bound_field_empty = BoundField(form, form.fields['password'], 'password')
        assert bound_field_empty.data() is None

        # Test with unbound form (data should be None)
        unbound_form = form.__class__()
        unbound_bound_field = BoundField(unbound_form, unbound_form.fields['username'], 'username')
        assert unbound_bound_field.data() is None