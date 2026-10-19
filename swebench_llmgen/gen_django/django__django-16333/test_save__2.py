import pytest
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

@pytest.mark.django_db
def test_user_creation_form_save():
    # Prepare the data for the user creation
    data = {
        'username': 'testuser',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
    }

    # Instantiate the form
    form = UserCreationForm(data)

    # Test form validation
    assert form.is_valid()

    # Save the user and check if it is created
    user = form.save()

    # Assertions to confirm the user was created and the password is set correctly
    assert user.username == 'testuser'
    assert user.check_password('securepassword123')
    
    # Check if the user is saved in the database
    assert User.objects.filter(username='testuser').exists()

    # Test the "commit" functionality
    assert User.objects.count() == 1

    # Now we will test the behavior when `commit` is False
    form_no_commit = UserCreationForm(data)

    assert form_no_commit.is_valid()
    
    user_no_commit = form_no_commit.save(commit=False)
    
    # Make sure the user is not saved in the database
    assert not User.objects.filter(username='testuser').exists()
    
    # Set the password and verify it is set
    user_no_commit.set_password('anothersecurepassword')
    assert user_no_commit.check_password('anothersecurepassword')
    
    # Now, explicitly save the user
    user_no_commit.save()
    
    # Now it should be in the database
    assert User.objects.filter(username='testuser').exists()