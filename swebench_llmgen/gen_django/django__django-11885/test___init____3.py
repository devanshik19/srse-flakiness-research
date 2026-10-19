import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError

def test_protected_error_initialization():
    msg = "This action is prohibited due to protected objects."
    protected_objects = [User(username='user1'), User(username='user2')]

    # Creating an instance of ProtectedError
    error = ProtectedError(msg, protected_objects)

    # Asserting that the message is correctly set
    assert str(error) == msg

    # Asserting that protected_objects is correctly set
    assert error.protected_objects == protected_objects
    
    # Asserting the type of protected_objects is correct
    assert isinstance(error.protected_objects, list)
    assert all(isinstance(obj, User) for obj in error.protected_objects)