import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError

def test_protected_error_initialization():
    msg = "Cannot delete protected objects."
    protected_objects = [User(username='user1'), User(username='user2')]
    
    # Create instances to ensure they are saved
    for user in protected_objects:
        user.save()
    
    error = ProtectedError(msg, protected_objects)
    
    assert error.protected_objects == protected_objects
    assert str(error) == msg  # Also the base class should be initialized properly