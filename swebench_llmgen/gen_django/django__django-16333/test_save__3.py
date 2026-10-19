import pytest
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

class TestUserCreationForm:

    @pytest.fixture
    def form_data(self):
        return {
            'username': 'testuser',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }

    @pytest.fixture
    def form(self, form_data):
        return UserCreationForm(data=form_data)

    def test_save_creates_user(self, form):
        assert form.is_valid()
        user = form.save()
        assert user.username == 'testuser'
        assert user.check_password('SecurePass123!')

    def test_save_without_commit(self, form):
        assert form.is_valid()
        user = form.save(commit=False)
        assert user.username == 'testuser'
        assert not User.objects.filter(username='testuser').exists()

    def test_save_with_invalid_password(self, form_data):
        form_data['password2'] = 'DifferentPass123!'
        form = UserCreationForm(data=form_data)
        with pytest.raises(ValidationError):
            assert form.is_valid() is False
            form.save()

    def test_save_with_unusable_password(self, form_data):
        form_data['password1'] = form_data['password2'] = ' '
        form = UserCreationForm(data=form_data)
        assert form.is_valid() is False
        with pytest.raises(ValidationError):
            form.save()