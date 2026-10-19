import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError

def test_protected_error_init():
    # Create a sample protected object
    protected_user = User(username='protected_user')
    
    # Create the instance of ProtectedError
    error_message = "You cannot delete this object because it's protected."
    protected_error = ProtectedError(error_message, [protected_user])

    # Assertions to verify the properties
    assert protected_error.protected_objects == [protected_user]
    assert str(protected_error) == error_message  # This will utilize the base Exception's str method