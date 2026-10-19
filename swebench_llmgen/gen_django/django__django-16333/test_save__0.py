import pytest
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class TestUserCreationForm:

    @pytest.fixture
    def user_data(self):
        return {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }

    def test_save_creates_user_with_commit(self, user_data):
        form = UserCreationForm(user_data)
        assert form.is_valid(), form.errors
        user = form.save(commit=True)
        assert isinstance(user, User)
        assert user.username == user_data['username']
        assert user.email == user_data['email']
        assert user.check_password(user_data['password1']) is True

    def test_save_does_not_commit_user_without_commit(self, user_data):
        form = UserCreationForm(user_data)
        assert form.is_valid(), form.errors
        user = form.save(commit=False)
        assert user.username == user_data['username']
        assert user.email == user_data['email']
        assert user.check_password(user_data['password1']) is False  # Password should not be set yet
        user.save()
        assert User.objects.filter(username=user_data['username']).exists()