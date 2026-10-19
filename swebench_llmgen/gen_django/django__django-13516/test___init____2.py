import pytest
from django.core.management.base import CommandError

def test_command_error_init():
    # Test with default returncode
    error = CommandError("An error occurred")
    assert error.returncode == 1
    assert str(error) == "An error occurred"

    # Test with custom returncode
    error = CommandError("Custom error message", returncode=2)
    assert error.returncode == 2
    assert str(error) == "Custom error message"

    # Test with no arguments
    error = CommandError()
    assert error.returncode == 1
    assert str(error) == ""