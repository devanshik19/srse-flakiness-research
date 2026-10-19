import pytest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

@pytest.fixture
def user_creation_form():
    form_data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }
    return UserCreationForm(data=form_data)

def test_save_creates_user(user_creation_form):
    assert user_creation_form.is_valid()
    user = user_creation_form.save()
    assert isinstance(user, User)
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
    assert User.objects.filter(username='testuser').exists()

def test_save_with_commit(user_creation_form):
    assert user_creation_form.is_valid()
    user = user_creation_form.save(commit=True)
    assert user.pk is not None
    assert User.objects.filter(pk=user.pk).exists()

def test_save_without_commit(user_creation_form):
    assert user_creation_form.is_valid()
    user = user_creation_form.save(commit=False)
    assert user.pk is None
    assert not User.objects.filter(username='testuser').exists()

def test_password_set(user_creation_form):
    assert user_creation_form.is_valid()
    user = user_creation_form.save()
    assert user.password.startswith('pbkdf2_sha256$')  # Check for the hashed password format