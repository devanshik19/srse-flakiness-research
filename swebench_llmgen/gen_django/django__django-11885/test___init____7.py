import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError


def test_protected_error_initialization():
    protected_objects = [User(username='testuser1'), User(username='testuser2')]
    error_message = "Cannot delete the user(s). They are protected."

    # Initialize the ProtectedError with a message and protected objects
    protected_error = ProtectedError(error_message, protected_objects)

    # Assert that the error message and protected objects are set correctly
    assert protected_error.args[0] == error_message
    assert protected_error.protected_objects == protected_objects