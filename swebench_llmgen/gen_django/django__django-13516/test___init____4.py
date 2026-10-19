import pytest
from django.core.management.base import CommandError

def test_command_error_init():
    # Test default initialization
    error = CommandError("An error occurred")
    assert error.returncode == 1
    assert str(error) == "An error occurred"

    # Test custom return code
    error_with_code = CommandError("Another error occurred", returncode=2)
    assert error_with_code.returncode == 2
    assert str(error_with_code) == "Another error occurred"

    # Test with multiple positional arguments
    error_with_multiple_args = CommandError("Error happened", "Additional info", returncode=3)
    assert error_with_multiple_args.returncode == 3
    assert str(error_with_multiple_args) == "Error happened"