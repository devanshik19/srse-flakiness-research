import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError

def test_protected_error_initialization():
    protected_user = User(username="protected_user")
    protected_user.save()

    # Initialize ProtectedError with a message and the protected objects
    error_msg = "Cannot delete the user because it is protected."
    protected_objects = [protected_user]

    # Create an instance of ProtectedError
    protected_error = ProtectedError(error_msg, protected_objects)

    # Assert that the message is set correctly
    assert str(protected_error) == error_msg

    # Assert that the protected_objects are set correctly
    assert protected_error.protected_objects == protected_objects

    # Check the type of the protected_objects
    assert isinstance(protected_error.protected_objects, list)
    assert len(protected_error.protected_objects) == 1
    assert protected_error.protected_objects[0] == protected_user