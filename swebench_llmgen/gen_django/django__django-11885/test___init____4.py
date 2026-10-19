import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError

def test_protected_error_init():
    # Prepare test data
    msg = "Attempted to delete protected objects."
    protected_user = User(username="protected_user")
    
    # Act
    protected_error = ProtectedError(msg, [protected_user])
    
    # Assert
    assert protected_error.protected_objects == [protected_user]
    assert str(protected_error) == msg