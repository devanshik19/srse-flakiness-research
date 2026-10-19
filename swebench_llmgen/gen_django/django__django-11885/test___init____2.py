import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError

def test_protected_error_init():
    protected_objects = [User(username='test_user')]
    msg = "This object is protected and cannot be deleted."
    
    error = ProtectedError(msg, protected_objects)
    
    assert error.protected_objects == protected_objects
    assert str(error) == msg  # Check if the message is correctly set