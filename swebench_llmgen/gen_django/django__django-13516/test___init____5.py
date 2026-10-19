import pytest
from django.core.management.base import CommandError

def test_command_error_init():
    # Test default returncode
    error = CommandError("An error occurred")
    assert error.returncode == 1
    assert str(error) == "An error occurred"

    # Test custom returncode
    error_with_custom_code = CommandError("Another error occurred", returncode=2)
    assert error_with_custom_code.returncode == 2
    assert str(error_with_custom_code) == "Another error occurred"

    # Test with additional arguments
    error_with_args = CommandError("Error with extra args", returncode=3, extra='value')
    assert error_with_args.returncode == 3
    assert str(error_with_args) == "Error with extra args"