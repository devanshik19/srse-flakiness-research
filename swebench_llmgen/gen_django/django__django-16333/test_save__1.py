import pytest
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class TestUserCreationForm:

    @pytest.fixture
    def user_creation_form(self):
        data = {
            'username': 'testuser',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        form = UserCreationForm(data=data)
        return form

    def test_valid_form_saves_user(self, user_creation_form):
        user_creation_form.is_valid()
        user = user_creation_form.save(commit=True)
        assert User.objects.filter(username='testuser').exists()
        assert user.username == 'testuser'
        assert user.check_password('SecurePass123!')

    def test_invalid_form_does_not_save_user(self, user_creation_form):
        user_creation_form.cleaned_data['password1'] = 'short'
        user_creation_form.cleaned_data['password2'] = 'short'
        with pytest.raises(ValidationError):
            user_creation_form.save(commit=False)

    def test_password_mismatch(self, user_creation_form):
        user_creation_form.cleaned_data['password1'] = 'SecurePass123!'
        user_creation_form.cleaned_data['password2'] = 'DifferentPass123!'
        with pytest.raises(ValidationError):
            user_creation_form.clean_password2()