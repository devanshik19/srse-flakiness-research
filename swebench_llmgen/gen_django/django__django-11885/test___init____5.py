import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError

def test_protected_error_initialization():
    # Arrange
    protected_objects = [User(username="test_user")]
    msg = "This object is protected."

    # Act
    error = ProtectedError(msg, protected_objects)

    # Assert
    assert error.protected_objects == protected_objects
    assert str(error) == f"{msg}, {protected_objects}"