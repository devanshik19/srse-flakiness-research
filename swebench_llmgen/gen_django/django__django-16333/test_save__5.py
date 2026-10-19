import pytest
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


@pytest.mark.django_db
def test_user_creation_form_save():
    # Create an instance of the UserCreationForm with valid input
    form_data = {
        'username': 'testuser',
        'password1': 'secure_password',
        'password2': 'secure_password',
    }
    form = UserCreationForm(data=form_data)

    # Check if the form is valid
    assert form.is_valid()

    # Save the user instance
    user = form.save(commit=True)

    # Validate that the user was created in the database
    assert User.objects.filter(username='testuser').exists()
    
    # Retrieve the created user and check password
    created_user = User.objects.get(username='testuser')
    assert created_user.check_password('secure_password')

    # Test the case where passwords do not match
    form_data_invalid = {
        'username': 'testuser2',
        'password1': 'password1',
        'password2': 'password2',
    }
    form_invalid = UserCreationForm(data=form_data_invalid)

    # Check if the form is invalid
    assert not form_invalid.is_valid()

    # Attempt to save the user instance should not create a new user
    with pytest.raises(ValidationError):
        form_invalid.save(commit=True)

    # Confirm the user count remains the same
    assert User.objects.count() == 1