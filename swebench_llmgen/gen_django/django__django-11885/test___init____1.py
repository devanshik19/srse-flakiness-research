import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError

def test_protected_error_initialization():
    protected_objects = [User(username='user1'), User(username='user2')]
    
    # Ensure that the protected objects are properly initialized
    error_message = "This object cannot be deleted as it is protected."
    exception = ProtectedError(error_message, protected_objects)

    # Verify the exception message and protected objects
    assert str(exception) == error_message
    assert exception.protected_objects == protected_objects