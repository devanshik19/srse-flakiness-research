import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError

def test_protected_error_initialization():
    protected_users = [User(username=f'user{i}') for i in range(3)]
    for user in protected_users:
        user.save()  # Ensure the users are saved in the database

    msg = "You cannot delete these users because they are protected."
    
    # Create a ProtectedError instance
    error = ProtectedError(msg, protected_users)

    # Assert that the message is set correctly
    assert str(error) == msg

    # Assert that protected_objects are set correctly
    assert error.protected_objects == protected_users
    assert len(error.protected_objects) == 3
    
    # Check if the protected_objects are indeed User instances
    assert all(isinstance(obj, User) for obj in error.protected_objects)